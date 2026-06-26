#!/usr/bin/env python3
"""
chunk_writer.py — Write large content to files in chunks to prevent crashes.

Usage:
  python3 chunk_writer.py <file_path> <content_file_or_stdin>
  echo "content" | python3 chunk_writer.py <file_path> -
"""

from __future__ import annotations

import sys
import os

CHUNK_SIZE = 20000  # Max characters per chunk

ALLOWED_EXTENSIONS = {'.md', '.json', '.jsonl', '.txt', '.yaml', '.yml'}


def safe_resolve(file_path: str, root: str | None = None) -> str:
    """Resolve file_path and ensure it stays within root. Rejects symlink escapes."""
    resolved = os.path.realpath(os.path.expanduser(file_path))
    if root:
        root_resolved = os.path.realpath(os.path.expanduser(root))
        if not resolved.startswith(root_resolved + os.sep) and resolved != root_resolved:
            raise ValueError(
                f"Path escapes vault boundary: '{file_path}' resolves to '{resolved}', "
                f"which is outside '{root_resolved}'"
            )
    ext = os.path.splitext(resolved)[1].lower()
    if ext and ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"File extension '{ext}' not in allowlist: {ALLOWED_EXTENSIONS}")
    return resolved


def chunk_write(file_path: str, content: str, vault_root: str | None = None) -> dict:
    """Write content to file in chunks, breaking at paragraph boundaries.

    If vault_root is provided, the resolved file_path must stay within it.
    """
    safe_path = safe_resolve(file_path, vault_root)
    os.makedirs(os.path.dirname(safe_path) or '.', exist_ok=True)

    total_chars = len(content)
    chunks = []
    pos = 0

    while pos < total_chars:
        end = min(pos + CHUNK_SIZE, total_chars)
        if end < total_chars:
            newline_pos = content.rfind('\n', pos + CHUNK_SIZE // 2, end)
            if newline_pos > pos:
                end = newline_pos + 1
        chunks.append(content[pos:end])
        pos = end

    with open(safe_path, 'w', encoding='utf-8') as f:
        f.write(chunks[0])

    for chunk in chunks[1:]:
        with open(safe_path, 'a', encoding='utf-8') as f:
            f.write(chunk)

    actual_size = os.path.getsize(safe_path)
    return {
        "file": safe_path,
        "total_chars": total_chars,
        "chunks": len(chunks),
        "file_size_bytes": actual_size,
        "success": True
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: chunk_writer.py <file_path> <content_file_or_->")
        sys.exit(1)

    file_path = sys.argv[1]
    content_source = sys.argv[2]

    if content_source == '-':
        content = sys.stdin.read()
    else:
        with open(content_source, 'r', encoding='utf-8') as f:
            content = f.read()

    result = chunk_write(file_path, content)
    print(f"✅ Written: {result['file']}")
    print(f"   Characters: {result['total_chars']}")
    print(f"   Chunks: {result['chunks']}")
    print(f"   File size: {result['file_size_bytes']} bytes")


if __name__ == '__main__':
    main()
