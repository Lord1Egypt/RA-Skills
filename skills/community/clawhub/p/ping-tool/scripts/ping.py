#!/usr/bin/env python3
import subprocess, sys
if len(sys.argv) < 2: print("Usage: ping.py <host>"); sys.exit(1)
subprocess.run(["ping", "-c", "4", sys.argv[1]])
