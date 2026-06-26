#!/usr/bin/env python3
"""
依赖检测模块 — 在各入口脚本开头调用
如果核心依赖缺失，打印友好提醒并退出
"""
import os
import sys
import subprocess

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def check_dependencies(auto_install=False):
    """检测 markitdown 和 jieba 是否已安装"""
    missing = []
    
    try:
        import markitdown
    except ImportError:
        missing.append("markitdown")
    
    try:
        import jieba
    except ImportError:
        missing.append("jieba")
    
    if missing:
        print("=" * 50)
        print("⚠️  依赖缺失，知识库功能无法启动")
        print("=" * 50)
        print(f"\n缺少: {', '.join(missing)}")
        print(f"\n请先运行初始化脚本自动安装依赖：")
        print(f"  cd {SKILL_DIR}")
        print(f"  python3 scripts/init.py")
        print(f"\n或者手动安装：")
        print(f"  pip install markitdown[all] jieba")
        print("=" * 50)
        return False
    return True


def check_kb_ready():
    """检测知识库目录是否已初始化"""
    kb_root = os.path.expanduser("~/.openclaw/workspace/knowledge-base")
    index_file = os.path.join(kb_root, ".index.json")
    if not os.path.exists(index_file):
        print("=" * 50)
        print("⚠️  知识库尚未初始化")
        print("=" * 50)
        print(f"\n请先运行初始化脚本：")
        print(f"  cd {SKILL_DIR}")
        print(f"  python3 scripts/init.py")
        print("=" * 50)
        return False
    return True


if __name__ == "__main__":
    ok = check_dependencies()
    if ok:
        check_kb_ready()
