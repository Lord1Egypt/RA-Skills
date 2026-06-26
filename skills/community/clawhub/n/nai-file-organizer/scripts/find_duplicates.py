#!/usr/bin/env python3
"""
find_duplicates.py — Find duplicate files in a scan JSON inventory.

Strategy:
    1. Group files by size (fast — no I/O)
    2. For same-size groups, compute content hash (efficient — skips unique sizes)
    3. Report groups of files with identical hashes

Usage:
    python3 find_duplicates.py <scan.json> [--algorithm md5|sha256] [--output <file.json>]
    python3 find_duplicates.py --directory <dir> [--algorithm md5|sha256] [--output <file.json>]

Input: JSON produced by scan.py
Output JSON structure:
    {
        "scan_dir": "/path/to/dir",
        "analyzed_at": "2024-01-01T12:00:00",
        "total_files": 100,
        "duplicate_groups": 3,
        "duplicate_files": 8,
        "wasted_bytes": 204800,
        "groups": [
            {
                "hash": "abc123...",
                "size": 102400,
                "count": 3,
                "wasted_bytes": 204800,
                "files": [
                    {"path": "a/file.jpg", "abs_path": "/..."},
                    ...
                ]
            },
            ...
        ]
    }
"""

import os
import sys
import json
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict


def compute_hash(filepath: str, algorithm: str = "md5", chunk_size: int = 65536) -> str | None:
    """Compute file hash. Returns None on permission/IO errors."""
    try:
        h = hashlib.new(algorithm)
        with open(filepath, "rb") as f:
            while chunk := f.read(chunk_size):
                h.update(chunk)
        return h.hexdigest()
    except (PermissionError, OSError) as e:
        print(f"WARNING: Cannot hash {filepath}: {e}", file=sys.stderr)
        return None


def find_duplicates(files: list[dict], algorithm: str = "md5") -> list[dict]:
    """
    Two-pass duplicate detection:
    Pass 1: Group by size (O(n), no I/O)
    Pass 2: Hash only files sharing a size (efficient)
    """
    # Pass 1: group by size, skip symlinks and zero-byte files
    size_groups: dict[int, list[dict]] = defaultdict(list)
    for f in files:
        if f.get("is_symlink"):
            continue
        size = f.get("size", 0)
        if size == 0:
            continue
        size_groups[size].append(f)

    # Only examine groups with 2+ files (same size = possible duplicates)
    candidate_groups = {size: group for size, group in size_groups.items() if len(group) >= 2}

    total_candidates = sum(len(g) for g in candidate_groups.values())
    if total_candidates > 0:
        print(
            f"Pass 1: {len(candidate_groups)} size groups with {total_candidates} candidate files to hash",
            file=sys.stderr,
        )

    # Pass 2: hash candidates and group by hash
    hash_groups: dict[str, list[dict]] = defaultdict(list)
    hashed = 0
    for size, group in candidate_groups.items():
        for f in group:
            abs_path = f.get("abs_path", f.get("path", ""))
            # Use pre-computed hash if available and algorithm matches
            file_hash = f.get("hash")
            if not file_hash:
                file_hash = compute_hash(abs_path, algorithm)
            if file_hash:
                # Key by (hash, size) to be safe
                key = f"{file_hash}:{size}"
                hash_groups[key].append({**f, "hash": file_hash})
                hashed += 1

    if total_candidates > 0:
        print(f"Pass 2: Hashed {hashed} files", file=sys.stderr)

    # Build duplicate groups (2+ files with same hash+size)
    duplicate_groups = []
    for key, group in hash_groups.items():
        if len(group) >= 2:
            file_hash, size_str = key.rsplit(":", 1)
            size = int(size_str)
            wasted = size * (len(group) - 1)
            duplicate_groups.append(
                {
                    "hash": file_hash,
                    "size": size,
                    "count": len(group),
                    "wasted_bytes": wasted,
                    "files": sorted(group, key=lambda f: f["path"]),
                }
            )

    # Sort by wasted bytes descending (biggest offenders first)
    duplicate_groups.sort(key=lambda g: g["wasted_bytes"], reverse=True)
    return duplicate_groups


def format_bytes(n: int) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"


def main():
    parser = argparse.ArgumentParser(
        description="Find duplicate files from a scan.py JSON inventory."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("scan_json", nargs="?", help="JSON file produced by scan.py")
    group.add_argument(
        "--directory",
        "-d",
        help="Scan this directory directly (runs scan internally)",
    )
    parser.add_argument(
        "--algorithm",
        default="md5",
        choices=["md5", "sha256"],
        help="Hash algorithm (default: md5)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Write JSON output to this file instead of stdout",
    )
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        default=False,
        help="Include hidden files when scanning directly",
    )
    args = parser.parse_args()

    # Load scan data
    if args.directory:
        # Import scan module from same directory
        script_dir = Path(__file__).parent
        sys.path.insert(0, str(script_dir))
        from scan import scan_directory

        target = Path(args.directory).expanduser().resolve()
        print(f"Scanning {target}...", file=sys.stderr)
        scan_data = scan_directory(target, include_hidden=args.include_hidden)
    else:
        scan_path = Path(args.scan_json)
        if not scan_path.exists():
            print(f"ERROR: File not found: {scan_path}", file=sys.stderr)
            sys.exit(1)
        try:
            scan_data = json.loads(scan_path.read_text())
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in {scan_path}: {e}", file=sys.stderr)
            sys.exit(1)

    files = scan_data.get("files", [])
    scan_dir = scan_data.get("scan_dir", "unknown")

    print(f"Analyzing {len(files)} files for duplicates...", file=sys.stderr)
    duplicate_groups = find_duplicates(files, algorithm=args.algorithm)

    total_duplicate_files = sum(g["count"] for g in duplicate_groups)
    total_wasted = sum(g["wasted_bytes"] for g in duplicate_groups)

    result = {
        "scan_dir": scan_dir,
        "analyzed_at": datetime.now().isoformat(),
        "algorithm": args.algorithm,
        "total_files": len(files),
        "duplicate_groups": len(duplicate_groups),
        "duplicate_files": total_duplicate_files,
        "wasted_bytes": total_wasted,
        "groups": duplicate_groups,
    }

    # Human-readable summary to stderr
    print(f"\n--- Duplicate Summary ---", file=sys.stderr)
    print(f"Files scanned:     {len(files)}", file=sys.stderr)
    print(f"Duplicate groups:  {len(duplicate_groups)}", file=sys.stderr)
    print(f"Duplicate files:   {total_duplicate_files}", file=sys.stderr)
    print(f"Wasted space:      {format_bytes(total_wasted)}", file=sys.stderr)

    if duplicate_groups:
        print(f"\nTop duplicates:", file=sys.stderr)
        for g in duplicate_groups[:5]:
            print(
                f"  {format_bytes(g['size'])} × {g['count']} copies = {format_bytes(g['wasted_bytes'])} wasted",
                file=sys.stderr,
            )
            for f in g["files"]:
                print(f"    {f['path']}", file=sys.stderr)

    output_json = json.dumps(result, indent=2)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output_json)
        print(f"\nOutput written to: {out_path}", file=sys.stderr)
    else:
        print(output_json)


if __name__ == "__main__":
    main()
