#!/usr/bin/env python3
"""
Git Helper 使用示例
"""

import subprocess

def example_1_status():
    """示例 1: 查看状态"""
    print("=" * 60)
    print("示例 1: git status")
    print("=" * 60)
    
    result = subprocess.run(["git", "status"], capture_output=True, text=True)
    print(result.stdout)

def example_2_log():
    """示例 2: 查看日志"""
    print("=" * 60)
    print("示例 2: git log")
    print("=" * 60)
    
    result = subprocess.run(
        ["git", "log", "--oneline", "-5"],
        capture_output=True, text=True
    )
    print(result.stdout)

def example_3_branch():
    """示例 3: 查看分支"""
    print("=" * 60)
    print("示例 3: git branch")
    print("=" * 60)
    
    result = subprocess.run(["git", "branch"], capture_output=True, text=True)
    print(result.stdout)

if __name__ == "__main__":
    try:
        example_1_status()
        example_2_log()
        example_3_branch()
        print("\n✅ 所有示例运行完成!")
    except Exception as e:
        print(f"错误：{e}")
