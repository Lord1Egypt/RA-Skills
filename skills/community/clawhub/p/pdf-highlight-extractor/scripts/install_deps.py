#!/usr/bin/env python3
"""
install_deps.py - 安装 pdf-highlight-extractor 技能所需依赖

在第一次使用技能时由 WorkBuddy 自动调用。
"""
import subprocess
import sys

REQUIRED = ["pymupdf"]

def main():
    print("[INFO] 正在安装依赖: pymupdf ...")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--quiet", *REQUIRED],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        print("[OK] 依赖安装成功。")
    else:
        print("[ERROR] 安装失败:", result.stderr, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
