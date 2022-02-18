import shutil
from collections import Counter
from distutils import extension
from pathlib import Path
from typing import Union

from loguro import logger

from src.data import Dir_path
from src.utils.io import read_json


class OrganiseDir:
    """
    This class is used to organise files in a directory by moving files into
    directories based on extension
    """

    def __init__(self, dir: Union[str, Path]) -> None:
        self.dir = Path(dir)
        if not self.dir.exists():
            raise FileNotFoundError(f"{self.dir} does not exist")

        ext_dirs = read_json(Dir_path / 'extensionsFile.json')
        self.extensions = {}
        for dir_name, ext_list in ext_dirs.items():
            for ext in ext_list:
                self.extensions[ext] = dir_name

    def __call__(self):
        logger.info(f'Organising files in {self.dir}')
        for file_path in self.dir.iterdir():
            if file_path.name.startswith('.'):
                continue

            if file_path.is_file():
                if file_path.suffix in self.extensions:
                    Dest_dir = self.dir / self.extensions[file_path.suffix]
                else:
                    Dest_dir = self.dir / 'other'

                Dest_dir.mkdir(exist_ok=True)
                logger.info(f'Moving {file_path} to {Dest_dir} ')
                shutil.move(str(file_path), str(Dest_dir))


if __name__ == "__main__":
    obj = OrganiseDir('/Users/yasaman/Downloads')
    obj()
    logger.info('Done!')