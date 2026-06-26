#!/usr/bin/env python3
"""Thin wrapper — delegates to memory_consolidate package."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from memory_consolidate import main
raise SystemExit(main())
