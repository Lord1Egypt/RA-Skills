"""Module entry point: allows ``python -m iterate_cli``."""

import sys

from iterate_cli.cli import main

if __name__ == "__main__":
    sys.exit(main())
