#!/usr/bin/env python3
import os, sys
if len(sys.argv) != 3: print("Usage: ln.py target link"); sys.exit(1)
os.symlink(sys.argv[1], sys.argv[2]); print(f"Linked: {sys.argv[2]} -> {sys.argv[1]}")
