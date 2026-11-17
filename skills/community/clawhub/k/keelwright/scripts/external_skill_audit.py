#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""R11 external-skill audit — lightweight enforcer for keelwright.

Does NOT replace a full audit (zip-slip, manifest integrity, license headers,
size/count bounds). Run this BEFORE installing any third-party skill ZIP.
"""
import zipfile, hashlib, os, sys, re
from pathlib import Path

MAX_FILES = 5000
MAX_TOTAL_BYTES = 200 * 1024 * 1024
MAX_SINGLE_FILE = 10 * 1024 * 1024

MIT0_PATTERNS = ["MIT-0", "MIT No Attribution", "SPDX-License-Identifier: MIT-0"]

def check_zip(path: Path) -> list:
    errs = []
    if not path.exists():
        return [f"missing: {path}"]
    if path.stat().st_size == 0:
        return [f"empty archive: {path}"]
    try:
        with zipfile.ZipFile(path) as zf:
            names = zf.namelist()
            total = 0
            for info in zf.infolist():
                if info.is_dir():
                    continue
                if getattr(info, "is_symlink", lambda: False)():
                    errs.append(f"symlink entry: {info.filename}")
                    continue
                size = info.file_size
                if size > MAX_SINGLE_FILE:
                    errs.append(f"file too large: {info.filename} ({size//1024}KB)")
                total += size
                data = zf.read(info.filename)
                text = ""
                try:
                    text = data.decode("utf-8", errors="ignore")
                except Exception:
                    pass
                if info.filename.endswith(".py") and not any(p in text for p in MIT0_PATTERNS):
                    errs.append(f"missing MIT-0 header: {info.filename}")
            if len(names) > MAX_FILES:
                errs.append(f"too many files: {len(names)} > {MAX_FILES}")
            if total > MAX_TOTAL_BYTES:
                errs.append(f"total bytes too large: {total} > {MAX_TOTAL_BYTES}")
            if "_MANIFEST.json" not in names:
                errs.append("missing _MANIFEST.json")
    except Exception as e:
        errs.append(f"zip error: {e}")
    return errs

def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python external_skill_audit.py <zip-or-dir>")
        return 1
    target = Path(sys.argv[1])
    if not target.exists():
        print(f"missing: {target}")
        return 1
    if target.is_file():
        errs = check_zip(target)
    else:
        errs = []
        py_files = list(target.rglob("*.py"))
        for py in py_files[:50]:
            text = py.read_text(encoding="utf-8", errors="ignore")
            if not any(p in text for p in MIT0_PATTERNS):
                errs.append(f"missing MIT-0 header: {py}")
    if errs:
        print("R11 AUDIT FAIL:")
        for e in errs[:20]:
            print(f"  - {e}")
        return 1
    print("R11 AUDIT OK: no obvious supply-chain issues found.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
