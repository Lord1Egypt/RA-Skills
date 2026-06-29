#!/usr/bin/env python3
"""同步目录，应用与 pack_zip.py 一致的排除规则。
用法: python sync_with_exclude.py <src_dir> <dst_dir>
设计: 替代 rsync 的排除同步，确保仓库文件与打包排除规则一致。
"""
import os
import sys
import shutil
from pathlib import Path

# ── 路径集中管理 ─────────────────────────────────────────
from _paths import (
    _data_dir_abs, DEFAULT_DATA_DIR_RAW, SKILL_DIR,
)




# ── 排除规则（与 pack_zip.py 保持一致）──────────────────────────
EXCLUDE_DIRS = {
    "__pycache__", ".git", ".eggs", "eggs", "dist", "build",
    ".eggs-info", ".pytest_cache", ".mypy_cache", "node_modules",
    ".standardization", "outputs", "test-outputs",
}
EXCLUDE_FILES_EXACT = {
    ".gitignore", ".ds_store", "thumbs.db",
    "config.json", "manifest.json", "pack_zip.py",
    ".gitkeep",  # 占位空文件，不应同步到仓库
    # config.json / manifest.json 无论在哪一律排除（含敏感信息/本地状态）
}
EXCLUDE_FILES_GLOB = {
    "*.pyc", "*.pyo", "*.log", "*.zip", "*.bak*",
    "*.tmp", "._*", ".decisions.json",
    "*.sensitive_scan_*.json", "zip_out", "preview_server.py",
    "*_fixed.py", "stderr.txt", "stdout.txt",
    "*.bat",  # Windows 批处理文件
    "test_*.py",  # 测试脚本
}
FUNCTIONAL_FILE_WHITELIST = {"settings.html", "preview.html"}

# 空文件白名单（这些空文件需要保留）
EMPTY_FILE_WHITELIST = {".gitkeep", ".keep", ".gitignore", "readme"}

def should_exclude(rel_path, file_path=None):
    """判断相对路径是否应被排除。

    rel_path: 相对于技能源目录的路径（正反斜杠均可），如 "config.json" 或 "scripts/foo.py"
    file_path: 可选，真实文件路径，用于检查文件大小
    returns: True 表示排除，False 表示保留
    """
    import fnmatch

    p = rel_path.replace(os.sep, "/")
    name = os.path.basename(p)
    parent_dir = os.path.dirname(p)  # "" 表示根目录

    # 1. 白名单检查（最先）: 功能性文件跳过所有排除规则
    lower_name = name.lower()
    for w in FUNCTIONAL_FILE_WHITELIST:
        if lower_name == w.lower():
            return False

    # 2. 目录名检查（rel_path 的每个路径成分）
    parts = p.split("/")
    for part in parts[:-1]:  # 最后一个成分是文件名，不算目录
        if part.lower() in (d.lower() for d in EXCLUDE_DIRS):
            return True

    # 3. 精确文件名匹配
    lower_exact = {f.lower() for f in EXCLUDE_FILES_EXACT}
    if name.lower() in lower_exact:
        # config.json / manifest.json 无论在哪一律排除（含敏感信息/本地状态）
        return True

    # 4. glob 模式匹配
    for pat in EXCLUDE_FILES_GLOB:
        if fnmatch.fnmatch(name, pat):
            return True
        if fnmatch.fnmatch(p, pat):
            return True

    # 5. 空文件排除（0 KB）- .gitkeep 等占位文件
    if file_path and os.path.exists(file_path):
        try:
            if os.path.getsize(file_path) == 0:
                # 白名单检查: 少数空文件需要保留
                if name.lower() not in {w.lower() for w in EMPTY_FILE_WHITELIST}:
                    return True
        except OSError:
            pass

    return False

def sync_with_exclude(src, dst):
    """用排除规则同步 src → dst（先清空 dst，再复制）"""
    src = os.path.normpath(src)
    dst = os.path.normpath(dst)

    if not os.path.isdir(src):
        print(f"[X] Source dir not found: {src}")
        sys.exit(1)

    # 安全检查: src 和 dst 不能相同，dst 不能是 src 的父目录
    src_resolved = os.path.realpath(src)
    dst_resolved = os.path.realpath(dst)
    if src_resolved == dst_resolved:
        print(f"[X] Operation refused: Source and destination are the same（{src_resolved}）")
        sys.exit(1)
    if dst_resolved.startswith(src_resolved + os.sep):
        print(f"[X] Operation refused: Destination is inside source（{dst_resolved}）")
        sys.exit(1)

    # 清空目标目录（安全: 已通过 git-sync.sh 路径校验）
    if os.path.isdir(dst):
        shutil.rmtree(dst)
    os.makedirs(dst, exist_ok=True)

    copy_count = 0
    skipped_empty = 0
    for root, dirs, files in os.walk(src):
        # rel_root: 相对于 src 根目录的路径（"" 表示根目录本身）
        rel_root = os.path.relpath(root, src)
        rel_root = "" if rel_root == "." else rel_root

        # 排除目录（原地修改 dirs 以阻止 os.walk 进入）
        if rel_root:
            dirs[:] = [d for d in dirs if not should_exclude(os.path.join(rel_root, d))]
        else:
            dirs[:] = [d for d in dirs if not should_exclude(d)]

        for fname in files:
            rel_path = os.path.join(rel_root, fname) if rel_root else fname
            file_path = os.path.join(root, fname)
            if should_exclude(rel_path, file_path):
                # 统计跳过的空文件数
                try:
                    if os.path.getsize(file_path) == 0:
                        skipped_empty += 1
                except OSError:
                    pass
                continue
            dst_file = os.path.join(dst, rel_path)
            os.makedirs(os.path.dirname(dst_file), exist_ok=True)
            shutil.copy2(file_path, dst_file)
            copy_count += 1

    print(f"  [OK] Python exclude copy completed: {copy_count}  files")
    if skipped_empty > 0:
        print(f"  ℹ️  跳过 {skipped_empty} 个空文件（0 KB）")
    return copy_count

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("用法: python sync_with_exclude.py <src_dir> <dst_dir>")
        sys.exit(1)
    sync_with_exclude(sys.argv[1], sys.argv[2])
