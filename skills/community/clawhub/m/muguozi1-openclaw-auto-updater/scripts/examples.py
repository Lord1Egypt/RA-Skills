#!/usr/bin/env python3
"""
Auto Updater 使用示例
"""

import subprocess

def example_1_check_updates():
    """示例 1: 检查更新"""
    print("=" * 60)
    print("示例 1: 检查更新")
    print("=" * 60)
    
    result = subprocess.run(
        ["clawhub", "list"],
        capture_output=True, text=True
    )
    print(result.stdout)

def example_2_update_all():
    """示例 2: 更新所有技能"""
    print("=" * 60)
    print("示例 2: 更新所有技能")
    print("=" * 60)
    
    result = subprocess.run(
        ["clawhub", "update", "--all"],
        capture_output=True, text=True
    )
    print(result.stdout)

def example_3_update_single():
    """示例 3: 更新单个技能"""
    print("=" * 60)
    print("示例 3: 更新单个技能")
    print("=" * 60)
    
    result = subprocess.run(
        ["clawhub", "update", "skill-name"],
        capture_output=True, text=True
    )
    print(result.stdout)

if __name__ == "__main__":
    example_1_check_updates()
    example_2_update_all()
    example_3_update_single()
    print("\n✅ 所有示例运行完成!")
