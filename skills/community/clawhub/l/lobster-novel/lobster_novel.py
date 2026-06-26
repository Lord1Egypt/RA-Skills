#!/usr/bin/env python3
"""
lobster-novel — Self-evolving novel writing engine for OpenClaw

Usage:
    python3 lobster_novel.py --dir <project_dir> <command> [options]

Commands: init, status, context, write, save, review, export, style-template,
          tokens, bible, continuity, foreshadow
"""
import sys
from pathlib import Path

# Add skill directory to path for imports
SKILL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SKILL_DIR))
sys.path.insert(0, str(SKILL_DIR / "core"))
sys.path.insert(0, str(SKILL_DIR / "agents"))
sys.path.insert(0, str(SKILL_DIR / "review"))
sys.path.insert(0, str(SKILL_DIR / "output"))
sys.path.insert(0, str(SKILL_DIR / "memory"))

from tools.novel_cli import main

if __name__ == "__main__":
    main()
