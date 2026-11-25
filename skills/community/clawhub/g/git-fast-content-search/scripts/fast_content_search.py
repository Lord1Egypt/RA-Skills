#!/usr/bin/env python3
"""Fast, binary-safe literal content search for files and nested Git worktrees."""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

CHUNK_SIZE = 1024 * 1024
SAMPLE_SIZE = 8192


def patterns_for(path, needle):
    with path.open("rb") as handle:
        sample = handle.read(SAMPLE_SIZE)
    if sample.startswith(b"\xff\xfe"):
        return [needle.encode("utf-16-le")]
    if sample.startswith(b"\xfe\xff"):
        return [needle.encode("utf-16-be")]
    if b"\0" in sample:
        return []
    return [needle.encode("utf-8")]


def contains(path, needle):
    try:
        patterns = patterns_for(path, needle)
        if not patterns:
            return False
        overlap = max(map(len, patterns)) - 1
        tail = b""
        with path.open("rb") as handle:
            while block := handle.read(CHUNK_SIZE):
                data = tail + block
                if any(pattern in data for pattern in patterns):
                    return True
                tail = data[-overlap:] if overlap else b""
    except (OSError, UnicodeError):
        pass
    return False


def git_files(root, needle):
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "grep", "-I", "-l", "-z", "-F", "--", needle],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False,
        )
    except OSError:
        return None
    if result.returncode not in (0, 1):
        return None
    return [root / name.decode(sys.getfilesystemencoding(), "surrogateescape")
            for name in result.stdout.split(b"\0") if name]


def git_untracked_files(root):
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "status", "--porcelain=v1", "-z",
             "--untracked-files=all"],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return [root / entry[3:].decode(sys.getfilesystemencoding(), "surrogateescape")
            for entry in result.stdout.split(b"\0") if entry.startswith(b"?? ")]


def emit(path, is_git_project_file, method, output):
    item = {"path": str(path.resolve()), "is_git_project_file": is_git_project_file,
            "search_method": method}
    if output == "json":
        print(json.dumps(item, ensure_ascii=False))
    else:
        print(f"{item['path']}\tgit={str(is_git_project_file).lower()}\tmethod={method}")


def search(root, needle, output):
    if root.is_file():
        if contains(root, needle):
            emit(root, False, "filesystem", output)
        return
    for current, dirs, files in os.walk(root, topdown=True, followlinks=False):
        folder = Path(current)
        if ".git" in dirs or (folder / ".git").is_file():
            matched = git_files(folder, needle)
            if matched is not None:
                for path in matched:
                    emit(path, True, "git-grep", output)
                untracked = git_untracked_files(folder)
                if untracked is not None:
                    for path in untracked:
                        if not path.is_symlink() and path.is_file() and contains(path, needle):
                            emit(path, True, "filesystem-untracked", output)
                dirs[:] = []
                continue
        dirs[:] = [name for name in dirs if name != ".git"]
        for name in files:
            path = folder / name
            if not path.is_symlink() and path.is_file() and contains(path, needle):
                emit(path, False, "filesystem", output)


def main():
    parser = argparse.ArgumentParser(description="Find a literal string in files.")
    parser.add_argument("directory", type=Path)
    parser.add_argument("text")
    parser.add_argument("--format", choices=("json", "lines"), default="json")
    args = parser.parse_args()
    root = args.directory.expanduser().resolve()
    if not args.text:
        parser.error("text must not be empty")
    if not root.exists():
        parser.error(f"path does not exist: {root}")
    search(root, args.text, args.format)


if __name__ == "__main__":
    main()
