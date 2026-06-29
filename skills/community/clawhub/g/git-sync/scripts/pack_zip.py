#!/usr/bin/env python3
"""
pack_zip.py — 将 skill 目录打包为 ZIP 安装包
用法: python pack_zip.py <source_dir> <output_zip_path>
"""
import sys
import os
import zipfile
import fnmatch
from pathlib import Path

# ── 路径集中管理 ─────────────────────────────────────────
from _paths import (
    _data_dir_abs, DEFAULT_DATA_DIR_RAW, SKILL_DIR,
)

# UTF-8 输出（Windows 终端兼容）
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def pack_zip(source_dir, output_zip):
    """将 source_dir 打包为 output_zip，应用标准排除规则。"""
    source = os.path.normpath(source_dir)
    output = os.path.normpath(output_zip)

    if not os.path.isdir(source):
        print(f"❌ 源目录不存在: {source}")
        sys.exit(1)

    # 标准排除规则（与 git-sync.sh / sync_with_exclude.py 保持一致）
    exclude_dirs = {
        "__pycache__", ".git", ".eggs", "eggs", "dist", "build",
        ".eggs-info", ".pytest_cache", ".mypy_cache", "node_modules",
        ".dist", ".standardization",
    }
    exclude_file_patterns = [
        ".gitignore", ".ds_store", "thumbs.db",
        "*.bat",
        "test_sensitive.py",
        ".gitkeep",
        "*.bak*",
        "fix_*.py", "force_*.py", "patch_*.py", "insert_*.py",
        "implement_*.py", "apply_*.py", "*_fixed.py",
        "settings.py", "skill_extractor.py",
    ]
    exclude_extensions = {".pyc", ".pyo", ".pyd", ".bak", ".tmp", ".bak*"}

    empty_file_whitelist = {".gitkeep", ".keep", ".gitignore", "readme"}

    parent_dir = os.path.dirname(source)
    skill_name = os.path.basename(source)
    arc_root = skill_name

    print(f"📦 打包: {source}")
    print(f"   输出: {output}")

    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
        file_count = 0
        skipped_empty = 0
        for root, dirs, files in os.walk(source):
            dirs[:] = [
                d for d in dirs
                if d not in exclude_dirs
                and not d.startswith(".")
            ]

            for fname in files:
                if any(fnmatch.fnmatch(fname, pat) for pat in exclude_file_patterns):
                    continue
                if os.path.splitext(fname)[1].lower() in exclude_extensions:
                    continue

                file_path = os.path.join(root, fname)

                if os.path.getsize(file_path) == 0:
                    if fname.lower() not in {w.lower() for w in empty_file_whitelist}:
                        skipped_empty += 1
                        continue

                rel_path = os.path.relpath(file_path, parent_dir)
                arc_name = rel_path.replace(os.sep, "/")

                zf.write(file_path, arc_name)
                file_count += 1

        print(f"  ✅ 已写入 {file_count} 个文件")
        if skipped_empty > 0:
            print(f"  ℹ️  跳过 {skipped_empty} 个空文件（0 KB）")

    size_kb = os.path.getsize(output) / 1024
    print(f"  ✅ ZIP 生成完毕: {output}")
    print(f"     大小: {size_kb:.1f} KB，文件数: {file_count}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python pack_zip.py <source_dir> <output_zip_path>")
        sys.exit(1)

    src = sys.argv[1]
    dst = sys.argv[2]
    pack_zip(src, dst)
