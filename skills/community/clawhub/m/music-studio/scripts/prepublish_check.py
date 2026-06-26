#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FORBIDDEN_PATTERNS = [
    r"MINIMAX_API_KEY",
    r"sk-[A-Za-z0-9_-]{10,}",
    r"api[_-]?key\s*[=:]\s*['\"](?!YOUR_MINIMAX_API_KEY)([^'\"]{6,})['\"]",
]
IGNORE_DIRS = {".git", "__pycache__", "output", ".pytest_cache", ".mypy_cache"}
IGNORE_FILES = {"config.example.json", "scripts/prepublish_check.py"}


def tracked_files() -> list[Path]:
    out = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True)
    return [ROOT / line.strip() for line in out.splitlines() if line.strip()]


def scan() -> list[tuple[str, int, str]]:
    hits: list[tuple[str, int, str]] = []
    for path in tracked_files():
        rel = path.relative_to(ROOT)
        if any(part in IGNORE_DIRS for part in rel.parts):
            continue
        if rel.name in IGNORE_FILES or str(rel) in IGNORE_FILES:
            continue
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for pat in FORBIDDEN_PATTERNS:
                if re.search(pat, line):
                    hits.append((str(rel), i, line.strip()))
                    break
    return hits


def main() -> int:
    hits = scan()
    if hits:
        print("❌ 发布前检查失败：检测到疑似环境变量引用或敏感 key 痕迹")
        for rel, line_no, line in hits:
            print(f"- {rel}:{line_no}: {line}")
        return 1
    print("✅ 发布前检查通过：未发现环境变量 API Key 引用或明显敏感 key")
    print("ℹ️  请确认真实 API Key 仅存在于本机 ~/.config/music-studio/config.json，不在仓库内")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
