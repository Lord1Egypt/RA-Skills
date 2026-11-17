#!/usr/bin/env python3
"""Shell B CLI — amazon-aba-kw-snapshot"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from aba_common import main_cli
if __name__ == "__main__":
    main_cli("B")
