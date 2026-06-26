#!/usr/bin/env python3
"""Clone or inspect a GitHub/GitLab repository for paper reproduction workspaces.

Usage:
  python scripts/bootstrap_repo.py <repo-url> [paper-slug] [bucket]

The script is intentionally read-only after clone: it does not install dependencies,
download data, run training, or perform git pull on existing directories.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Iterable

ALLOWED_PREFIXES = (
    "https://github.com/",
    "git@github.com:",
    "https://gitlab.com/",
    "git@gitlab.com:",
)

DEPENDENCY_PATTERNS = (
    "requirements", "environment", "pyproject.toml", "setup.py", "setup.cfg",
    "Pipfile", "Dockerfile", "conda", "poetry.lock", "package.json",
)
ENTRY_RE = re.compile(r"^(train|main|run|eval|test|infer|demo).*\.(py|ipynb|sh|cmd|ps1)$", re.I)


def safe_component(value: str, default: str = "paper") -> str:
    value = value.lower().replace("\\", "/")
    value = re.sub(r"[^a-z0-9._/-]+", "-", value)
    value = re.sub(r"/{2,}", "/", value).strip("/")
    value = re.sub(r"(^|/)-+", r"\1", value)
    value = re.sub(r"-+(/|$)", r"\1", value)
    return value or default


def repo_name_from_url(url: str) -> str:
    name = url.rstrip("/").split("/")[-1]
    if ":" in name and url.startswith("git@"):
        name = name.split(":")[-1]
    if name.endswith(".git"):
        name = name[:-4]
    return re.sub(r"[^A-Za-z0-9._-]+", "-", name) or "repo"


def run(cmd: list[str], cwd: Path | None = None) -> tuple[int, str]:
    try:
        proc = subprocess.run(cmd, cwd=str(cwd) if cwd else None, text=True,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=300)
        return proc.returncode, proc.stdout
    except FileNotFoundError as exc:
        return 127, str(exc)
    except subprocess.TimeoutExpired as exc:
        return 124, (exc.stdout or "") + "\n[timeout] command timed out"


def rel_files(root: Path, max_depth: int = 2) -> list[str]:
    out: list[str] = []
    if not root.exists():
        return out
    for path in root.rglob("*"):
        try:
            rel = path.relative_to(root)
        except ValueError:
            continue
        if len(rel.parts) > max_depth:
            continue
        if any(part in {".git", "__pycache__", ".venv", "node_modules"} for part in rel.parts):
            continue
        out.append(str(rel).replace("\\", "/") + ("/" if path.is_dir() else ""))
    return sorted(out)


def find_files(root: Path, max_depth: int, predicate) -> list[str]:
    matches: list[str] = []
    if not root.exists():
        return matches
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            rel = path.relative_to(root)
        except ValueError:
            continue
        if len(rel.parts) > max_depth:
            continue
        if any(part in {".git", "__pycache__", ".venv", "node_modules"} for part in rel.parts):
            continue
        if predicate(path):
            matches.append(str(rel).replace("\\", "/"))
    return sorted(matches)


def find_readme(root: Path) -> Path | None:
    for name in ("README.md", "README.rst", "README.txt", "readme.md"):
        candidate = root / name
        if candidate.exists():
            return candidate
    for path in root.rglob("README*"):
        try:
            if len(path.relative_to(root).parts) <= 2 and path.is_file():
                return path
        except ValueError:
            pass
    return None


def read_head(path: Path, max_lines: int = 160) -> str:
    try:
        with path.open("r", encoding="utf-8", errors="replace") as f:
            return "".join(line for _, line in zip(range(max_lines), f))
    except OSError as exc:
        return f"[read failed] {exc}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Clone or inspect repo in paper-repro-workspace")
    parser.add_argument("repo_url")
    parser.add_argument("paper_slug", nargs="?", default="paper")
    parser.add_argument("bucket", nargs="?", default="main-code")
    args = parser.parse_args(argv)

    repo_url = args.repo_url.strip()
    if not repo_url.startswith(ALLOWED_PREFIXES):
        print(f"错误：仓库地址看起来不是 GitHub/GitLab URL：{repo_url}", file=sys.stderr)
        return 2

    safe_slug = safe_component(args.paper_slug, "paper")
    safe_bucket = safe_component(args.bucket, "main-code")
    root_dir = Path("paper-repro-workspace") / safe_slug / safe_bucket
    root_dir.mkdir(parents=True, exist_ok=True)

    repo_name = repo_name_from_url(repo_url)
    target_dir = root_dir / repo_name
    clone_status = "已 clone"
    clone_note = "新克隆仓库。"
    remote_url = ""
    command_summary = ""

    if target_dir.exists():
        clone_status = "已存在，跳过 clone"
        command_summary = "未执行 git clone，只做现有目录检查。"
        if (target_dir / ".git").exists():
            code, origin = run(["git", "-C", str(target_dir), "remote", "get-url", "origin"])
            remote_url = origin.strip() if code == 0 else ""
            if remote_url == repo_url:
                clone_note = "目标目录已存在且 origin 与目标仓库一致；按规则不重复 clone，也不自动 git pull。"
            elif remote_url:
                clone_note = f"目标目录已存在且是 git 仓库，但 origin 与目标仓库不一致：{remote_url}；按规则不覆盖、不重复 clone。"
            else:
                clone_note = "目标目录已存在且是 git 仓库，但没有读取到 origin；按规则不重复 clone。"
        else:
            clone_note = "目标目录已存在但不是 git 仓库；按规则不覆盖、不重复 clone。"
    else:
        command_summary = f"git clone {repo_url} {target_dir}"
        code, output = run(["git", "clone", repo_url, str(target_dir)])
        if code != 0:
            print("=== 执行脚本 ===")
            print("脚本：bootstrap_repo.py")
            print(f"命令：{command_summary}")
            print(output)
            return code

    print("=== 执行脚本 ===")
    print("脚本：bootstrap_repo.py")
    print(f"命令：{command_summary}")
    print("")
    print("=== 克隆结果 ===")
    print(f"仓库状态：{clone_status}")
    print(f"重复目录提醒：{clone_note}")
    print(f"本地路径：{target_dir}")
    print(f"远程地址：{repo_url}")
    if remote_url:
        print(f"现有 origin：{remote_url}")

    print("\n=== 顶层结构 ===")
    for item in rel_files(target_dir, 2)[:120]:
        print(item)

    print("\n=== 常见依赖文件 ===")
    dep_files = find_files(target_dir, 3, lambda p: any(token.lower() in p.name.lower() for token in DEPENDENCY_PATTERNS))
    for item in dep_files:
        print(item)

    print("\n=== 常见入口候选 ===")
    entry_files = find_files(target_dir, 4, lambda p: bool(ENTRY_RE.match(p.name)))
    for item in entry_files[:80]:
        print(item)

    print("\n=== README 摘要候选 ===")
    readme = find_readme(target_dir)
    if readme:
        print(f"README 文件：{readme}")
        print(read_head(readme, 160))
    else:
        print("未在前两层目录找到 README。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
