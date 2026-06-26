#!/usr/bin/env python3
"""Lightweight OpenClaw AgentOS diagnostic helper."""
from __future__ import annotations
import json, os, shutil, subprocess
from pathlib import Path

workspace = Path(os.environ.get("OPENCLAW_WORKSPACE", "/Users/mac/.openclaw/workspace")).expanduser()
skills_dir = Path(os.environ.get("OPENCLAW_SKILLS", "/Users/mac/.openclaw/skills")).expanduser()
protected = ["AGENTS.md", "MEMORY.md", "SOUL.md", "TOOLS.md", "USER.md", "DREAMS.md"]

def exists(p: Path): return p.exists()
def count_skills():
    if not skills_dir.exists(): return 0
    return sum(1 for p in skills_dir.iterdir() if p.is_dir())

def cmd_exists(name: str): return shutil.which(name) is not None

report = {
    "workspace": str(workspace),
    "workspace_exists": exists(workspace),
    "skills_dir": str(skills_dir),
    "skills_dir_exists": exists(skills_dir),
    "skill_count": count_skills(),
    "bins": {"clawhub": cmd_exists("clawhub"), "git": cmd_exists("git"), "npm": cmd_exists("npm")},
    "protected_files": {name: exists(workspace / name) for name in protected},
    "memory_dirs": {
        "memory": exists(workspace / "memory"),
        "memory/wiki": exists(workspace / "memory" / "wiki"),
        "memory/projects": exists(workspace / "memory" / "projects"),
        "memory/domains": exists(workspace / "memory" / "domains"),
        "memory/archive": exists(workspace / "memory" / "archive"),
    },
}
print(json.dumps(report, ensure_ascii=False, indent=2))
