#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""输出当前项目 bin 目录下文件的 SHA256。"""

from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            chunk = f.read(1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="计算 bin 目录文件 SHA256")
    parser.add_argument("--file", help="仅计算指定文件名（如 healthgateway-darwin-arm64）")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    bin_dir = project_root / "bin"

    if not bin_dir.exists() or not bin_dir.is_dir():
        print(f"[ERROR] bin 目录不存在: {bin_dir}")
        return 1

    files = sorted([p for p in bin_dir.iterdir() if p.is_file()])
    if args.file:
        files = [p for p in files if p.name == args.file]

    if not files:
        print("[ERROR] 未找到符合条件的 healthgateway 可执行文件")
        return 1

    print(f"[INFO] bin 目录: {bin_dir}")
    for f in files:
        digest = sha256_file(f)
        print(f"{f.name}\t{digest}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
