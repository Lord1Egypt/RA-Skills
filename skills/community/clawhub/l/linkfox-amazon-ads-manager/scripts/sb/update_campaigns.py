#!/usr/bin/env python3
"""Compatibility wrapper: delegates to scripts/sb/v4/update_campaigns.py."""
import runpy
from pathlib import Path

runpy.run_path(str(Path(__file__).resolve().parent / 'v4' / 'update_campaigns.py'), run_name='__main__')
