# lunheng scripts package
# All Python tools for the judgment drafter skill.

import sys
import os

# Ensure this package's directory is on sys.path for intra-package imports
# (e.g., `from config import ...` in sibling modules)
_pkg_dir = os.path.dirname(os.path.abspath(__file__))
if _pkg_dir not in sys.path:
    sys.path.insert(0, _pkg_dir)
