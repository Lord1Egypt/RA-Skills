#!/usr/bin/env python3
"""Changelog 自动生成：从 git log 提取版本变更记录"""

import argparse
import re
import subprocess
from datetime import datetime
from pathlib import Path

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
REPO_DIR = Path(__file__).resolve().parent.parent


def get_git_log(repo_dir: Path, limit: int = 50) -> list[dict]:
    """获取 git log"""
    result = subprocess.run(
        ["git", "log", f"--max-count={limit}", "--pretty=format:%H|%ai|%s"],
        cwd=repo_dir, capture_output=True, text=True, timeout=10
    )
    if result.returncode != 0:
        return []

    commits = []
    for line in result.stdout.strip().split("\n"):
        if "|" not in line:
            continue
        hash_, date, msg = line.split("|", 2)
        commits.append({
            "hash": hash_[:8],
            "date": date[:10],
            "time": date[11:16],
            "message": msg.strip(),
        })
    return commits


def extract_version(message: str) -> str | None:
    """从提交消息提取版本号"""
    match = re.match(r'[vV](\d+(?:\.\d+)*)', message)
    return match.group(1) if match else None


def parse_changes(message: str) -> list[str]:
    """从提交消息提取变更项"""
    changes = []
    for line in message.split("\n"):
        line = line.strip()
        if line.startswith("- "):
            changes.append(line[2:])
        elif line.startswith("* "):
            changes.append(line[2:])
    return changes


def generate_changelog(repo_dir: Path, output_path: Path | None = None) -> str:
    """生成 Changelog"""
    commits = get_git_log(repo_dir)
    if not commits:
        return "无法获取 git 历史"

    sections = []
    current_version = "unreleased"

    for commit in commits:
        version = extract_version(commit["message"])
        if version:
            current_version = f"v{version}"
            sections.append({
                "version": current_version,
                "date": commit["date"],
                "changes": parse_changes(commit["message"]),
            })
        elif sections:
            # 追加到当前版本
            extras = parse_changes(commit["message"])
            sections[-1]["changes"].extend(extras)

    if not sections:
        return "无版本记录"

    # 生成 Markdown
    lines = ["# Changelog\n"]
    lines.append(f"最后更新：{datetime.now().strftime('%Y-%m-%d')}\n")

    for section in sections:
        lines.append(f"## {section['version']} ({section['date']})\n")
        for change in section["changes"]:
            if change:
                lines.append(f"- {change}")
        lines.append("")

    changelog = "\n".join(lines)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(changelog, encoding="utf-8")
        print(f"✅ Changelog 已生成: {output_path}")
    else:
        print(changelog)

    return changelog


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Changelog 自动生成")
    p.add_argument("--output", "-o", default=None)
    p.add_argument("--repo", default=None)
    args = p.parse_args()

    repo = Path(args.repo) if args.repo else REPO_DIR
    out = Path(args.output) if args.output else None
    generate_changelog(repo, out)
