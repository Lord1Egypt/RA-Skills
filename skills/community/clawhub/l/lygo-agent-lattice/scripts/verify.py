#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _stack_invoke import invoke
raise SystemExit(invoke("verify_agent_lattice.py"))
