#!/usr/bin/env python3
"""清理打包源目录中的残留文件（扫描产物、系统隐藏文件）
用法：python clean_zip_source.py <zip_source_dir>
安全策略：只处理临时目录（含 .tmp_zip 路径），源目录只打日志不删除。
"""
import os, sys, fnmatch, shutil

def normalize_path(p):
    """将路径规范化为 Windows 绝对路径（处理 Git Bash /c/... 格式）"""
    p = os.path.expanduser(p)
    if p.startswith("/") and len(p) > 2 and p[1].isalpha() and p[2] == "/":
        p = p[1].upper() + ":" + p[2:].replace("/", "\\")
    return os.path.normpath(p)

EXCLUDE_PATTERNS = [
    ".sensitive_scan_*.json",
    ".decisions.json",
    "._*",
    ".DS_Store",
    "Thumbs.db",
    "__pycache__",
    "*.pyc",
    "*_bak*.py",
    "fix_*.py",
    "force_*.py",
    "patch_*.py",
    "insert_*.py",
    "implement_*.py",
    "apply_*.py",
]

def should_delete(fname):
    for pat in EXCLUDE_PATTERNS:
        if fnmatch.fnmatch(fname, pat):
            return True
    return False

def is_temp_dir(path):
    """判断是否为临时目录（安全可删除）"""
    return ".tmp_zip" in path or "temp" in path.lower() or "tmp" in path.lower()

def main():
    if len(sys.argv) < 2:
        print("用法: python clean_zip_source.py <dir>")
        sys.exit(1)
    target = normalize_path(sys.argv[1])
    if not os.path.isdir(target):
        print(f"目录不存在: {target}")
        sys.exit(1)

    safe = is_temp_dir(target)
    deleted = 0
    skipped_source = 0

    for root, dirs, files in os.walk(target, topdown=True):
        # 清理文件
        for fname in files:
            if should_delete(fname):
                fpath = os.path.join(root, fname)
                if safe:
                    try:
                        os.remove(fpath)
                        deleted += 1
                        print(f"  🗑️  已删除: {os.path.relpath(fpath, target)}")
                    except Exception as e:
                        print(f"  ⚠️  删除失败 {fpath}: {e}")
                else:
                    # 源目录：只记录，不删除
                    skipped_source += 1
                    print(f"  ⚠️  源目录跳过（不删除）: {os.path.relpath(fpath, target)}")
        # 清理 __pycache__ 目录
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        for d in dirs[:]:
            if d.startswith(".") and d in ("__pycache__",):
                dpath = os.path.join(root, d)
                if safe:
                    try:
                        shutil.rmtree(dpath, ignore_errors=True)
                        deleted += 1
                    except Exception:
                        pass
                else:
                    skipped_source += 1
                    print(f"  ⚠️  源目录跳过（不删除目录）: {os.path.relpath(dpath, target)}")

    if safe:
        print(f"  ✅ 清理完成，共删除 {deleted} 项")
    else:
        print(f"  ⚠️  源目录模式：跳过 {skipped_source} 项（不删除），仅打包时排除")
        print(f"  💡 如需清理源目录，请手动删除上述文件")

if __name__ == "__main__":
    main()
