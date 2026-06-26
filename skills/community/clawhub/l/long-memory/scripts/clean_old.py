#!/usr/bin/env python3
"""清理旧记忆：归档超龄蒸馏文件和对话日志"""

import argparse
from datetime import datetime, timedelta
from pathlib import Path

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"


def parse_date(filename: str) -> datetime | None:
    """从文件名解析日期"""
    import re
    # YYYY-MM-DD 格式
    m = re.match(r"(\d{4}-\d{2}-\d{2})", filename)
    if m:
        try:
            return datetime.strptime(m.group(1), "%Y-%m-%d")
        except ValueError:
            pass
    # YYYY-WXX 格式
    m = re.match(r"(\d{4}-W\d{2})", filename)
    if m:
        # 粗略解析为该周周一
        from datetime import timedelta
        year = int(m.group(1)[:4])
        week = int(m.group(1).split("W")[1])
        jan4 = datetime(year, 1, 4)
        start = jan4 - timedelta(days=jan4.isoweekday() - 1) + timedelta(weeks=week - 1)
        return start
    return None


def clean_old(memory_dir: Path, days: int, dry_run: bool = True):
    archive_dir = memory_dir / "archive"
    cutoff = datetime.now() - timedelta(days=days)

    dirs_to_check = [
        ("conversations", "对话日志"),
        ("distillations", "蒸馏摘要"),
    ]

    moved = []
    for subdir, label in dirs_to_check:
        target_dir = memory_dir / subdir
        if not target_dir.exists():
            continue

        for f in sorted(target_dir.glob("*")):
            if not f.is_file():
                continue
            fdate = parse_date(f.stem)
            if fdate and fdate < cutoff:
                dest = archive_dir / subdir
                dest.mkdir(parents=True, exist_ok=True)
                dest_file = dest / f.name
                if dry_run:
                    moved.append((str(f), str(dest_file), label))
                else:
                    import shutil
                    shutil.move(str(f), str(dest_file))
                    moved.append((str(f), str(dest_file), label))

    if not moved:
        print(f"✅ 没有超过 {days} 天的文件需要清理")
        return

    print(f"{'🔍 [模拟]' if dry_run else '🗑️ [执行]'} 超过 {days} 天的文件清理：\n")
    for src, dest, label in moved:
        print(f"  [{label}] {Path(src).name}")
        print(f"    → archive/{Path(dest).relative_to(archive_dir)}")
    print(f"\n共 {len(moved)} 个文件")

    if dry_run:
        print(f"\n提示: 去掉 --dry-run 参数执行实际清理")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="清理旧记忆")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--days", type=int, default=90, help="保留天数（默认90天）")
    p.add_argument("--dry-run", action="store_true", default=True, help="模拟运行（默认开启）")
    p.add_argument("--execute", action="store_true", help="实际执行清理")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)
    clean_old(md, args.days, dry_run=not args.execute)
