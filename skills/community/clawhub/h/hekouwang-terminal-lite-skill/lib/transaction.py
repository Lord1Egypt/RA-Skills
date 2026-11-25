#!/usr/bin/env python3
"""Small, file-whitelisted transaction store for Hekouwang Terminal managed config."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from pathlib import Path


def store_root() -> Path:
    return Path(os.environ.get("HKW_TRANSACTION_ROOT", "~/.config/hekouwang-terminal/transactions")).expanduser()


# 回滚只允许碰主题切换真正会写的目录/文件；manifest 被篡改也不能越界。
_MANAGED_DIRS = (
    "~/.config/hekouwang-terminal",
    "~/.config/ghostty",
    "~/.config/bat",
    "~/.config/cmux",
    "~/.warp",
    "~/Library/Application Support/iTerm2/DynamicProfiles",
    "~/Library/Application Support/tabby",
)
_MANAGED_FILES = (
    "~/Library/Preferences/com.apple.Terminal.plist",
)


def _managed(path: Path) -> bool:
    try:
        target = path.expanduser().resolve(strict=False)
    except OSError:
        return False
    for raw in _MANAGED_DIRS:
        root = Path(raw).expanduser().resolve(strict=False)
        if target == root or root in target.parents:
            return True
    for raw in _MANAGED_FILES:
        if target == Path(raw).expanduser().resolve(strict=False):
            return True
    return False


def read_paths(path_file: Path) -> list[Path]:
    paths: list[Path] = []
    for raw in path_file.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if raw:
            path = Path(raw).expanduser()
            if _managed(path):
                paths.append(path)
    return paths


def snapshot(label: str, path_file: Path) -> Path:
    root = store_root()
    root.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    tx = root / f"{stamp}-{os.getpid()}"
    data = tx / "data"
    data.mkdir(parents=True)
    entries = []
    for index, path in enumerate(read_paths(path_file)):
        entry = {"path": str(path), "kind": "missing", "copy": None}
        if path.is_symlink():
            entry.update(kind="symlink", target=os.readlink(path))
        elif path.is_file():
            rel = f"{index:03d}"
            shutil.copy2(path, data / rel)
            entry.update(kind="file", copy=rel)
        elif path.is_dir():
            rel = f"{index:03d}"
            shutil.copytree(path, data / rel, symlinks=True)
            entry.update(kind="dir", copy=rel)
        entries.append(entry)
    manifest = {
        "version": 1,
        "label": label,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "entries": entries,
    }
    (tx / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (root / "latest").write_text(tx.name + "\n", encoding="utf-8")
    prune(root, keep=5)
    return tx


def resolve_tx(value: str) -> Path:
    root = store_root()
    if value.startswith("latest-"):
        wanted = value[len("latest-"):]
        candidates = []
        if root.is_dir():
            candidates = sorted((p for p in root.iterdir() if p.is_dir() and (p / "manifest.json").is_file()), reverse=True)
        for candidate in candidates:
            try:
                manifest = json.loads((candidate / "manifest.json").read_text(encoding="utf-8"))
            except (OSError, ValueError):
                continue
            if str(manifest.get("label", "")).startswith(wanted):
                return candidate
        raise SystemExit(f"no {wanted} transaction snapshot")
    if value == "latest":
        marker = root / "latest"
        if not marker.is_file():
            raise SystemExit("no transaction snapshot")
        value = marker.read_text(encoding="utf-8").strip()
    tx = Path(value).expanduser()
    if not tx.is_absolute():
        tx = root / tx
    if not (tx / "manifest.json").is_file():
        raise SystemExit(f"invalid transaction: {tx}")
    return tx


def remove_existing(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def rollback(value: str) -> Path:
    tx = resolve_tx(value)
    manifest = json.loads((tx / "manifest.json").read_text(encoding="utf-8"))
    for entry in reversed(manifest["entries"]):
        path = Path(entry["path"]).expanduser()
        if not _managed(path):
            continue
        remove_existing(path)
        kind = entry["kind"]
        if kind == "missing":
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        if kind == "symlink":
            path.symlink_to(entry["target"])
        elif kind == "file":
            shutil.copy2(tx / "data" / entry["copy"], path)
        elif kind == "dir":
            shutil.copytree(tx / "data" / entry["copy"], path, symlinks=True)
    return tx


def prune(root: Path, keep: int) -> None:
    txs = sorted((p for p in root.iterdir() if p.is_dir() and (p / "manifest.json").is_file()), reverse=True)
    for old in txs[keep:]:
        shutil.rmtree(old)


def history() -> None:
    root = store_root()
    if not root.is_dir():
        return
    for tx in sorted((p for p in root.iterdir() if p.is_dir() and (p / "manifest.json").is_file()), reverse=True):
        try:
            m = json.loads((tx / "manifest.json").read_text(encoding="utf-8"))
            print(f"{tx.name}\t{m.get('created_at', '')}\t{m.get('label', '')}")
        except (OSError, ValueError):
            continue


def plan(path_file: Path) -> None:
    for path in read_paths(path_file):
        state = "existing" if path.exists() or path.is_symlink() else "new"
        print(f"{state}\t{path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("snapshot")
    p.add_argument("--label", required=True)
    p.add_argument("--paths", type=Path, required=True)
    p = sub.add_parser("rollback")
    p.add_argument("transaction", nargs="?", default="latest")
    sub.add_parser("history")
    p = sub.add_parser("plan")
    p.add_argument("--paths", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "snapshot":
        print(snapshot(args.label, args.paths))
    elif args.command == "rollback":
        print(rollback(args.transaction))
    elif args.command == "history":
        history()
    elif args.command == "plan":
        plan(args.paths)


if __name__ == "__main__":
    main()
