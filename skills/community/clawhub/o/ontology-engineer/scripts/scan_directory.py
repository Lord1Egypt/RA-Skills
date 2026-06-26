#!/usr/bin/env python3
"""
scan_directory.py - Directory scanner with priority classification for ontology extraction.

Scans a project directory tree, classifies files by ontology-extraction priority (P1-P7),
and outputs a JSON manifest + statistics report.

Usage:
    python scan_directory.py <directory> [--output scan_result.json]
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path


# ---------------------------------------------------------------------------
# Priority classification rules
# ---------------------------------------------------------------------------

PRIORITY_RULES = [
    {
        "priority": "P1",
        "label": "Database Design Documents",
        "patterns": [
            r"数据库设计", r"表结构", r"db.?design", r"database.?design",
            r"table.?structure", r"数据模型", r"data.?model", r"ER图",
            r"实体关系", r"entity.?relation",
        ],
    },
    {
        "priority": "P2",
        "label": "Data Dictionaries",
        "patterns": [
            r"数据字典", r"字段定义", r"data.?dictionary", r"field.?def",
            r"系统清单", r"字段清单", r"代码表", r"code.?table",
            r"枚举", r"enum",
        ],
    },
    {
        "priority": "P3",
        "label": "Interface Specifications",
        "patterns": [
            r"接口说明", r"接口规格", r"接口文档", r"api.?spec",
            r"interface", r"webservice", r"web.?service", r"报文",
            r"消息格式", r"message.?format",
        ],
    },
    {
        "priority": "P4",
        "label": "Requirements Specifications",
        "patterns": [
            r"需求规格", r"需求说明", r"需求分析", r"srs",
            r"requirement", r"业务需求", r"功能需求",
            r"用例", r"use.?case",
        ],
    },
    {
        "priority": "P5",
        "label": "Architecture Documents",
        "patterns": [
            r"总体方案", r"概要设计", r"系统架构", r"架构设计",
            r"总体设计", r"技术方案", r"system.?architecture",
            r"high.?level.?design", r"hld",
        ],
    },
    {
        "priority": "P6",
        "label": "Data Flow Documents",
        "patterns": [
            r"数据流向", r"数据流转", r"data.?flow", r"数据交换",
            r"数据同步", r"etl", r"数据迁移", r"data.?migration",
        ],
    },
]

# Supported file extensions for ontology extraction
SUPPORTED_EXTENSIONS = {
    ".doc", ".docx", ".xls", ".xlsx",
    ".sql", ".ddl",
    ".json", ".jsonschema", ".yaml", ".yml",
    ".md", ".txt", ".csv",
}


def classify_file(filepath: Path) -> str:
    """Classify a file into priority P1-P7 based on filename patterns."""
    name_lower = filepath.stem.lower()
    # Also check parent directory name for context
    parent_lower = filepath.parent.name.lower()
    search_text = f"{name_lower} {parent_lower}"

    for rule in PRIORITY_RULES:
        for pattern in rule["patterns"]:
            if re.search(pattern, search_text, re.IGNORECASE):
                return rule["priority"]

    return "P7"


def scan_directory(root: Path) -> dict:
    """
    Scan directory tree and classify all supported files.

    Returns a dict with:
      - files: list of {path, extension, size_bytes, priority, priority_label}
      - stats: summary statistics
    """
    files = []
    ext_counter = Counter()
    priority_counter = Counter()
    total_size = 0
    skipped_count = 0

    for filepath in sorted(root.rglob("*")):
        if not filepath.is_file():
            continue

        # Skip macOS resource fork files (._*)
        if filepath.name.startswith("._"):
            skipped_count += 1
            continue

        ext = filepath.suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            skipped_count += 1
            continue

        size = filepath.stat().st_size
        priority = classify_file(filepath)

        # Find label for priority
        priority_label = "Other Documents"
        for rule in PRIORITY_RULES:
            if rule["priority"] == priority:
                priority_label = rule["label"]
                break

        files.append({
            "path": str(filepath),
            "relative_path": str(filepath.relative_to(root)),
            "extension": ext,
            "size_bytes": size,
            "size_mb": round(size / (1024 * 1024), 2),
            "priority": priority,
            "priority_label": priority_label,
        })

        ext_counter[ext] += 1
        priority_counter[priority] += 1
        total_size += size

    # Build statistics
    stats = {
        "root_directory": str(root),
        "total_supported_files": len(files),
        "total_skipped_files": skipped_count,
        "total_size_mb": round(total_size / (1024 * 1024), 2),
        "by_extension": dict(sorted(ext_counter.items())),
        "by_priority": dict(sorted(priority_counter.items())),
        "size_distribution": {
            "small_lt_5mb": sum(1 for f in files if f["size_bytes"] < 5 * 1024 * 1024),
            "medium_5_20mb": sum(1 for f in files if 5 * 1024 * 1024 <= f["size_bytes"] < 20 * 1024 * 1024),
            "large_20_50mb": sum(1 for f in files if 20 * 1024 * 1024 <= f["size_bytes"] < 50 * 1024 * 1024),
            "huge_gt_50mb": sum(1 for f in files if f["size_bytes"] >= 50 * 1024 * 1024),
        },
    }

    return {"files": files, "stats": stats}


def format_report(result: dict) -> str:
    """Format a human-readable statistics report."""
    stats = result["stats"]
    files = result["files"]
    lines = []

    lines.append("=" * 60)
    lines.append("ONTOLOGY ENGINEER - Directory Scan Report")
    lines.append("=" * 60)
    lines.append(f"Root: {stats['root_directory']}")
    lines.append(f"Total supported files: {stats['total_supported_files']}")
    lines.append(f"Total skipped files: {stats['total_skipped_files']}")
    lines.append(f"Total size: {stats['total_size_mb']} MB")
    lines.append("")

    lines.append("--- By Extension ---")
    for ext, count in sorted(stats["by_extension"].items()):
        lines.append(f"  {ext:10s} {count:>5d} files")
    lines.append("")

    lines.append("--- By Priority ---")
    priority_labels = {r["priority"]: r["label"] for r in PRIORITY_RULES}
    priority_labels["P7"] = "Other Documents"
    for p in ["P1", "P2", "P3", "P4", "P5", "P6", "P7"]:
        count = stats["by_priority"].get(p, 0)
        label = priority_labels.get(p, "")
        lines.append(f"  {p} ({label:30s}) {count:>5d} files")
    lines.append("")

    lines.append("--- File Size Distribution ---")
    sd = stats["size_distribution"]
    lines.append(f"  < 5 MB:    {sd['small_lt_5mb']:>5d} files")
    lines.append(f"  5-20 MB:   {sd['medium_5_20mb']:>5d} files")
    lines.append(f"  20-50 MB:  {sd['large_20_50mb']:>5d} files")
    lines.append(f"  > 50 MB:   {sd['huge_gt_50mb']:>5d} files")
    lines.append("")

    # Top 10 largest files
    sorted_by_size = sorted(files, key=lambda f: f["size_bytes"], reverse=True)[:10]
    if sorted_by_size:
        lines.append("--- Top 10 Largest Files ---")
        for f in sorted_by_size:
            lines.append(f"  [{f['priority']}] {f['size_mb']:>8.2f} MB  {f['relative_path']}")
        lines.append("")

    # P1-P3 file listing (high value)
    high_value = [f for f in files if f["priority"] in ("P1", "P2", "P3")]
    if high_value:
        lines.append("--- High-Value Files (P1-P3) ---")
        for f in sorted(high_value, key=lambda x: (x["priority"], x["relative_path"])):
            lines.append(f"  [{f['priority']}] {f['relative_path']}")
        lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Scan directory for ontology extraction")
    parser.add_argument("directory", help="Root directory to scan")
    parser.add_argument("--output", "-o", default="scan_result.json", help="Output JSON file path")
    parser.add_argument("--report", "-r", action="store_true", help="Print human-readable report")
    args = parser.parse_args()

    root = Path(args.directory)
    if not root.is_dir():
        print(f"Error: '{root}' is not a valid directory", file=sys.stderr)
        sys.exit(1)

    result = scan_directory(root)

    # Save JSON
    output_path = Path(args.output)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Scan result saved to: {output_path}")

    # Print report (force UTF-8 on Windows to avoid GBK encoding errors)
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    if args.report:
        print()
        print(format_report(result))
    else:
        # Always print summary
        stats = result["stats"]
        print(f"Found {stats['total_supported_files']} supported files ({stats['total_size_mb']} MB)")
        print(f"Priority distribution: {dict(sorted(stats['by_priority'].items()))}")


if __name__ == "__main__":
    main()
