#!/usr/bin/env python3
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from lib.storage import ensure_storage, REPORTS_PATH

def main():
    ensure_storage()
    print("✓ clawguard storage initialized")
    print(f"  {REPORTS_PATH}")

if __name__ == "__main__":
    main()
