#!/usr/bin/env python3
"""
scan.py — Walk a directory and output a JSON inventory of all files.

Usage:
    python3 scan.py <directory> [--include-hidden] [--output <file.json>]

Output JSON structure:
    {
        "scan_dir": "/path/to/dir",
        "scanned_at": "2024-01-01T12:00:00",
        "file_count": 42,
        "total_bytes": 123456,
        "files": [
            {
                "path": "relative/path/to/file.txt",
                "abs_path": "/absolute/path/to/file.txt",
                "name": "file.txt",
                "ext": ".txt",
                "size": 1024,
                "modified": "2024-01-01T10:00:00",
                "is_symlink": false,
                "hash": null   # populated by find_duplicates.py or --hash flag
            },
            ...
        ]
    }
"""

import os
import sys
import json
import argparse
import hashlib
from pathlib import Path
from datetime import datetime


def compute_hash(filepath: Path, algorithm: str = "md5", chunk_size: int = 65536) -> str | None:
    """Compute file hash. Returns None on permission/IO errors."""
    try:
        h = hashlib.new(algorithm)
        with open(filepath, "rb") as f:
            while chunk := f.read(chunk_size):
                h.update(chunk)
        return h.hexdigest()
    except (PermissionError, OSError):
        return None


def scan_directory(
    target: Path,
    include_hidden: bool = False,
    compute_hashes: bool = False,
    hash_algorithm: str = "md5",
) -> dict:
    """Walk the target directory and collect file metadata."""
    if not target.exists():
        print(f"ERROR: Directory not found: {target}", file=sys.stderr)
        sys.exit(1)
    if not target.is_dir():
        print(f"ERROR: Not a directory: {target}", file=sys.stderr)
        sys.exit(1)

    files = []
    skipped_permission = 0
    skipped_hidden = 0

    for root, dirs, filenames in os.walk(target, followlinks=False):
        root_path = Path(root)

        # Filter hidden directories in-place (prevents descending into them)
        if not include_hidden:
            hidden_dirs = [d for d in dirs if d.startswith(".")]
            skipped_hidden += len(hidden_dirs)
            dirs[:] = [d for d in dirs if not d.startswith(".")]

        for filename in sorted(filenames):
            # Skip hidden files
            if not include_hidden and filename.startswith("."):
                skipped_hidden += 1
                continue

            abs_path = root_path / filename
            rel_path = abs_path.relative_to(target)

            # Skip symlinks (don't follow, just record)
            is_symlink = abs_path.is_symlink()

            try:
                stat = abs_path.stat()
                size = stat.st_size
                modified = datetime.fromtimestamp(stat.st_mtime).isoformat()
            except (PermissionError, OSError) as e:
                print(f"WARNING: Cannot stat {abs_path}: {e}", file=sys.stderr)
                skipped_permission += 1
                continue

            ext = abs_path.suffix.lower()

            # Handle compound extensions like .tar.gz
            name_lower = filename.lower()
            compound_ext = None
            for compound in [".tar.gz", ".tar.bz2", ".tar.xz", ".tar.zst"]:
                if name_lower.endswith(compound):
                    compound_ext = compound
                    break
            if compound_ext:
                ext = compound_ext

            file_hash = None
            if compute_hashes and not is_symlink:
                file_hash = compute_hash(abs_path, hash_algorithm)

            files.append(
                {
                    "path": str(rel_path),
                    "abs_path": str(abs_path),
                    "name": filename,
                    "ext": ext,
                    "size": size,
                    "modified": modified,
                    "is_symlink": is_symlink,
                    "hash": file_hash,
                }
            )

    total_bytes = sum(f["size"] for f in files)

    result = {
        "scan_dir": str(target.resolve()),
        "scanned_at": datetime.now().isoformat(),
        "file_count": len(files),
        "total_bytes": total_bytes,
        "skipped_hidden": skipped_hidden,
        "skipped_permission_errors": skipped_permission,
        "include_hidden": include_hidden,
        "files": files,
    }

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Scan a directory and output a JSON file inventory."
    )
    parser.add_argument("directory", help="Directory to scan")
    parser.add_argument(
        "--include-hidden",
        action="store_true",
        default=False,
        help="Include hidden files and directories (those starting with .)",
    )
    parser.add_argument(
        "--hash",
        action="store_true",
        default=False,
        help="Compute MD5 hash for each file (slower but enables duplicate detection)",
    )
    parser.add_argument(
        "--hash-algorithm",
        default="md5",
        choices=["md5", "sha256"],
        help="Hash algorithm to use (default: md5)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default=None,
        help="Write JSON output to this file instead of stdout",
    )
    args = parser.parse_args()

    target = Path(args.directory).expanduser().resolve()
    result = scan_directory(
        target,
        include_hidden=args.include_hidden,
        compute_hashes=args.hash,
        hash_algorithm=args.hash_algorithm,
    )

    output_json = json.dumps(result, indent=2)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(output_json)
        print(f"Scan complete: {result['file_count']} files ({result['total_bytes']:,} bytes)")
        print(f"Output written to: {out_path}")
    else:
        print(output_json)


if __name__ == "__main__":
    main()
