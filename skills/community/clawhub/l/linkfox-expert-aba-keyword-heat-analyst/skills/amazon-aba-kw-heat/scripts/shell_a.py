#!/usr/bin/env python3
"""Shell A CLI — amazon-aba-kw-heat"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from aba_common import main_cli
if __name__ == "__main__":
    main_cli("A")
