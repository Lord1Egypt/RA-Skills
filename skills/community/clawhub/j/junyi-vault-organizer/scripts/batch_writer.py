#!/usr/bin/env python3
"""
batch_writer.py — Write multiple files from a JSON manifest.

Usage:
  python3 batch_writer.py <manifest.json> [vault_path]

Manifest format:
[
  {"path": "inbox/学习成长/2026-03-13 笔记.md", "content": "# Title\n\nBody..."},
  ...
]

Paths are relative to the vault root.
"""

import sys
import os
import json
from chunk_writer import chunk_write


def batch_write(manifest_path: str, vault_path: str) -> dict:
    with open(manifest_path, 'r', encoding='utf-8') as f:
        entries = json.load(f)

    results = []
    success_count = 0
    fail_count = 0

    vault_real = os.path.realpath(os.path.expanduser(vault_path))

    for i, entry in enumerate(entries):
        rel_path = entry['path']
        content = entry['content']

        # Reject absolute paths and path-traversal attempts
        if os.path.isabs(rel_path):
            results.append({"index": i, "path": rel_path, "status": "error", "error": "absolute path rejected"})
            fail_count += 1
            print(f"  [{i+1}/{len(entries)}] ❌ {rel_path}: absolute path rejected")
            continue
        if '..' in rel_path.split(os.sep):
            results.append({"index": i, "path": rel_path, "status": "error", "error": "path traversal (..) rejected"})
            fail_count += 1
            print(f"  [{i+1}/{len(entries)}] ❌ {rel_path}: path traversal (..) rejected")
            continue

        full_path = os.path.join(vault_path, rel_path)

        try:
            result = chunk_write(full_path, content, vault_root=vault_real)
            results.append({"index": i, "path": rel_path, "status": "ok"})
            success_count += 1
            print(f"  [{i+1}/{len(entries)}] ✅ {rel_path} ({result['total_chars']} chars)")
        except Exception as e:
            results.append({"index": i, "path": rel_path, "status": "error", "error": str(e)})
            fail_count += 1
            print(f"  [{i+1}/{len(entries)}] ❌ {rel_path}: {e}")

    return {"total": len(entries), "success": success_count, "failed": fail_count}


def main():
    if len(sys.argv) < 2:
        print("Usage: batch_writer.py <manifest.json> [vault_path]")
        sys.exit(1)

    manifest_path = sys.argv[1]
    vault_path = sys.argv[2] if len(sys.argv) > 2 else "."

    print(f"📦 Batch writing to: {vault_path}")
    summary = batch_write(manifest_path, vault_path)
    print(f"\nDone: {summary['success']} ok, {summary['failed']} failed, {summary['total']} total")


if __name__ == '__main__':
    main()
