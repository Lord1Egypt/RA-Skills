#!/usr/bin/env python3
# [OC-WM] licensed-to: macmini@MacminideMac-mini | bundle: vendor-suite | ts: 2026-03-09T17:30:16Z
"""
watermark.py — OpenClaw 用户专属水印注入工具
将用户 identifier 注入到已安装的 Python 文件头部，用于溯源追踪。
"""
import os
import sys
import argparse
from datetime import datetime, timezone

WATERMARK_TAG = "OC-WM"
SKIP_DIRS = {"__pycache__", ".git", "node_modules"}


def inject_watermark(filepath: str, identifier: str, bundle: str) -> bool:
    """在 Python 文件第一行（shebang 之后）注入水印注释。返回是否修改了文件。"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except (UnicodeDecodeError, PermissionError):
        return False

    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    watermark_line = f"# [{WATERMARK_TAG}] licensed-to: {identifier} | bundle: {bundle} | ts: {ts}\n"

    # 已有水印则跳过（避免重复）
    if f"[{WATERMARK_TAG}]" in content:
        return False

    lines = content.splitlines(keepends=True)
    insert_pos = 0

    # shebang 行保留在第一行
    if lines and lines[0].startswith("#!"):
        insert_pos = 1

    lines.insert(insert_pos, watermark_line)
    new_content = "".join(lines)

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)
        return True
    except PermissionError:
        return False


def watermark_directory(target_dir: str, identifier: str, bundle: str) -> int:
    """递归处理目录下所有 .py 文件，返回注入数量。"""
    count = 0
    for root, dirs, files in os.walk(target_dir):
        # 跳过不相关目录
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if fname.endswith(".py"):
                fpath = os.path.join(root, fname)
                if inject_watermark(fpath, identifier, bundle):
                    print(f"  [wm] {os.path.relpath(fpath, target_dir)}")
                    count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description="OpenClaw 水印注入工具")
    parser.add_argument("--identifier", required=True, help="用户授权标识（邮箱/用户名@主机名）")
    parser.add_argument("--bundle", required=True, help="套件 ID")
    parser.add_argument("--target", required=True, help="已安装技能的根目录路径")
    args = parser.parse_args()

    if not os.path.isdir(args.target):
        print(f"错误：目标目录不存在: {args.target}", file=sys.stderr)
        sys.exit(1)

    print(f"注入水印: identifier={args.identifier}, bundle={args.bundle}")
    count = watermark_directory(args.target, args.identifier, args.bundle)
    print(f"完成：共注入 {count} 个文件")


if __name__ == "__main__":
    main()
