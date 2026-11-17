"""允许 `python -m memoryguard` 运行 CLI。"""
from .cli import main
import sys

if __name__ == "__main__":
    sys.exit(main())
