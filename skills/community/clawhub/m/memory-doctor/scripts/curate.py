#!/usr/bin/env python3
"""Self-contained entrypoint for the bundled memory-doctor skill.

    python scripts/curate.py report --dir <memory-dir>
    python scripts/curate.py lint   --dir <memory-dir> [--fix]
    python scripts/curate.py undo   --dir <memory-dir>
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from memory_doctor.cli import main

if __name__ == "__main__":
    main()
