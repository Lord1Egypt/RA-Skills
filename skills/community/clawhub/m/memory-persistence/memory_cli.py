#!/usr/bin/env python3
"""
Memory System CLI Entry Point
"""
import sys
import os
from pathlib import Path

# Ensure the memory_system package is importable
script_dir = Path(__file__).parent.resolve()
# Add parent directory (workspace) to path
sys.path.insert(0, str(script_dir.parent))

from memory_system.cli import main

if __name__ == '__main__':
    sys.exit(main())
