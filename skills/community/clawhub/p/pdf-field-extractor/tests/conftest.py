#!/usr/bin/env python3
"""
Pytest configuration for PDF Field Extractor tests.
"""

import os
import sys

# Add parent directory to path so tests can import scripts
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
