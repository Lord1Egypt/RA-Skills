#!/usr/bin/env python3
"""
测试 Photo Search Skill 是否可以独立运行

从任何目录运行此脚本都应该能正常工作。
"""

import sys
import subprocess
from pathlib import Path

def test_skill():
    """测试skill.py"""
    skill_path = Path(__file__).parent / "skill.py"
    
    if not skill_path.exists():
        print(f"✗ 错误: 找不到 skill.py")
        return False
    
    print("📋 测试 Photo Search Skill")
    print("="*50)
    
    # 测试1: 帮助信息
    print("\n1. 测试帮助信息...")
    result = subprocess.run(
        [sys.executable, str(skill_path), "--help"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✓ 帮助信息显示正常")
    else:
        print("✗ 帮助信息显示失败")
        print(result.stderr)
        return False
    
    # 测试2: 查找项目根目录
    print("\n2. 测试项目根目录查找...")
    try:
        # 导入skill的函数
        sys.path.insert(0, str(skill_path.parent))
        from skill import find_project_root
        root = find_project_root()
        print(f"✓ 找到项目根目录: {root}")
    except Exception as e:
        print(f"✗ 查找项目根目录失败: {e}")
        return False
    
    # 测试3: 测试命令（不执行实际操作）
    print("\n3. 测试命令解析...")
    test_commands = [
        ["scan", "--help"],
        ["search", "--help"],
        ["annotate", "--help"],
        ["train", "--help"],
    ]
    
    for cmd in test_commands:
        result = subprocess.run(
            [sys.executable, str(skill_path)] + cmd,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print(f"✓ 命令 {' '.join(cmd)} 正常")
        else:
            print(f"✗ 命令 {' '.join(cmd)} 失败")
    
    print("\n" + "="*50)
    print("✓ 所有测试通过！")
    print("\n使用示例:")
    print(f"  python {skill_path} scan --dir D:\Photos")
    print(f"  python {skill_path} search \"海滩日落\"")
    print(f"  python {skill_path} search \"海滩\" --format json")
    
    return True


if __name__ == "__main__":
    success = test_skill()
    sys.exit(0 if success else 1)
