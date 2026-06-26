#!/usr/bin/env python3
"""
organize_files.py - 本地文件整理核心脚本
用法：python3 organize_files.py <source_dir> [target_dir] [options]
"""

import os
import sys
import json
import shutil
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict

# 默认分类规则
DEFAULT_RULES = {
    "Documents": ["pdf", "doc", "docx", "xls", "xlsx", "ppt", "pptx", "txt", "md", "pages", "numbers", "key", "csv"],
    "Pictures":  ["jpg", "jpeg", "png", "gif", "webp", "bmp", "tiff", "raw", "heic", "svg"],
    "Videos":    ["mp4", "mov", "avi", "mkv", "wmv", "flv", "m4v"],
    "Audio":     ["mp3", "wav", "flac", "aac", "ogg", "m4a", "opus"],
    "Archives":  ["zip", "rar", "7z", "tar", "gz", "bz2", "xz"],
    "Code":      ["py", "js", "ts", "sh", "java", "go", "rs", "cpp", "c", "h", "css", "html", "json", "yaml", "yml"],
    "Temp":      ["tmp", "temp", "log", "bak", "cache"],
}

def get_file_category(ext: str, rules: dict) -> str:
    ext = ext.lower().lstrip(".")
    for category, extensions in rules.items():
        if ext in extensions:
            return category
    return "Others"

def md5_hash(filepath: Path, chunk_size=8192) -> str:
    h = hashlib.md5()
    with open(filepath, "rb") as f:
        while chunk := f.read(chunk_size):
            h.update(chunk)
    return h.hexdigest()

def safe_move(src: Path, dst_dir: Path, dry_run=False) -> Path:
    """移动文件，自动处理命名冲突"""
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    if dst.exists() and dst != src:
        stem, suffix = src.stem, src.suffix
        i = 1
        while dst.exists():
            dst = dst_dir / f"{stem}_{i}{suffix}"
            i += 1
    if not dry_run:
        shutil.move(str(src), str(dst))
    return dst

def scan_directory(source: Path, ignore_hidden=True) -> list:
    files = []
    for p in source.rglob("*"):
        if p.is_file():
            if ignore_hidden and any(part.startswith(".") for part in p.parts):
                continue
            files.append(p)
    return files

def find_duplicates(files: list) -> dict:
    """返回 {hash: [path1, path2, ...]} 只含重复项"""
    size_groups = defaultdict(list)
    for f in files:
        try:
            size_groups[f.stat().st_size].append(f)
        except OSError:
            pass
    
    duplicates = {}
    for size, group in size_groups.items():
        if len(group) < 2:
            continue
        hash_groups = defaultdict(list)
        for f in group:
            try:
                h = md5_hash(f)
                hash_groups[h].append(f)
            except OSError:
                pass
        for h, paths in hash_groups.items():
            if len(paths) > 1:
                duplicates[h] = paths
    return duplicates

def organize(source_dir: str, target_dir: str = None, rules: dict = None,
             dry_run=False, find_dups=False, verbose=True) -> dict:
    source = Path(source_dir).expanduser().resolve()
    target = Path(target_dir).expanduser().resolve() if target_dir else source
    rules = rules or DEFAULT_RULES

    if not source.exists():
        print(f"[ERROR] 源目录不存在: {source}")
        sys.exit(1)

    files = scan_directory(source)
    stats = {"total": len(files), "moved": 0, "skipped": 0, "duplicates": 0, "log": []}

    if verbose:
        print(f"[扫描] 发现 {len(files)} 个文件")

    # 分类移动
    category_counts = defaultdict(int)
    for f in files:
        category = get_file_category(f.suffix, rules)
        dst_dir = target / category
        if f.parent == dst_dir:
            stats["skipped"] += 1
            continue
        dst = safe_move(f, dst_dir, dry_run=dry_run)
        stats["moved"] += 1
        category_counts[category] += 1
        stats["log"].append({"action": "move", "src": str(f), "dst": str(dst), "dry_run": dry_run})

    if verbose:
        for cat, count in sorted(category_counts.items()):
            print(f"  {cat}: {count} 个文件")

    # 重复检测
    if find_dups:
        all_files = scan_directory(target if target_dir else source)
        dups = find_duplicates(all_files)
        stats["duplicates"] = sum(len(v) - 1 for v in dups.values())
        if verbose and dups:
            print(f"\n[重复] 发现 {len(dups)} 组重复文件，共 {stats['duplicates']} 个冗余副本：")
            for h, paths in dups.items():
                print(f"  MD5:{h[:8]}... ({len(paths)} 个)")
                for p in paths:
                    print(f"    {p}")
        stats["duplicate_groups"] = {h: [str(p) for p in paths] for h, paths in dups.items()}

    # 生成报告
    report = {
        "timestamp": datetime.now().isoformat(),
        "source": str(source),
        "target": str(target),
        "dry_run": dry_run,
        "stats": stats,
    }
    report_path = target / f"organize-report-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    if not dry_run:
        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        if verbose:
            print(f"\n[报告] 已保存到 {report_path}")

    print(f"\n[完成] 移动 {stats['moved']} 个，跳过 {stats['skipped']} 个" +
          (f"，发现 {stats['duplicates']} 个冗余副本" if find_dups else "") +
          (" (DRY RUN)" if dry_run else ""))
    return report

def main():
    parser = argparse.ArgumentParser(description="本地文件整理工具")
    parser.add_argument("source", help="源目录路径")
    parser.add_argument("target", nargs="?", help="目标目录（默认与源目录相同）")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际移动文件")
    parser.add_argument("--find-dups", action="store_true", help="检测重复文件")
    parser.add_argument("--rules", help="自定义分类规则 JSON 文件路径")
    parser.add_argument("--quiet", action="store_true", help="静默模式")
    args = parser.parse_args()

    rules = None
    if args.rules:
        with open(args.rules, encoding="utf-8") as f:
            rules = json.load(f)

    organize(
        source_dir=args.source,
        target_dir=args.target,
        rules=rules,
        dry_run=args.dry_run,
        find_dups=args.find_dups,
        verbose=not args.quiet,
    )

if __name__ == "__main__":
    main()
