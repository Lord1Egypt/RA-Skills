#!/usr/bin/env python3
"""
NSAP (神经稀疏异步处理架构) - 技能验证脚本
用于验证技能完整性并生成打包信息
"""

import json
import os
from datetime import datetime


def verify_skill_structure(skill_dir):
    """验证技能目录结构"""
    required_files = [
        "SKILL.md",
        "README.md",
        "_meta.json",
        "CHANGELOG.md",
        "scripts/modular_split.py",
        "scripts/sparse_activate.py",
        "scripts/async_run.py",
        "scripts/resource_monitor.py"
    ]
    
    missing_files = []
    for req in required_files:
        if not os.path.exists(os.path.join(skill_dir, req)):
            missing_files.append(req)
    
    return missing_files


def calculate_file_size(skill_dir):
    """计算技能总大小"""
    total_size = 0
    file_count = 0
    
    for root, dirs, files in os.walk(skill_dir):
        # 跳过隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if not file.startswith('.') and file.endswith(('.py', '.md', '.json')):
                file_path = os.path.join(root, file)
                try:
                    total_size += os.path.getsize(file_path)
                    file_count += 1
                except:
                    pass
    
    return total_size, file_count


def main():
    """主验证流程"""
    # 获取技能根目录（脚本的上一级目录）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(script_dir)
    skill_name = os.path.basename(skill_dir)
    
    print(f"=== NSAP 技能验证 ===\n")
    print(f"技能目录：{skill_name}\n")
    
    # 1. 验证结构
    print("1. 验证技能结构...")
    missing = verify_skill_structure(skill_dir)
    if missing:
        print(f"  ❌ 缺失文件:")
        for f in missing:
            print(f"     - {f}")
    else:
        print("  ✅ 所有必需文件都存在")
    print()
    
    # 2. 文件大小统计
    print("2. 文件大小统计:")
    total_size, file_count = calculate_file_size(skill_dir)
    print(f"   文件数量：{file_count}")
    print(f"   总大小：{total_size} bytes ({total_size/1024:.1f} KB)")
    print()
    
    # 3. 读取元数据
    print("3. 技能信息:")
    meta_path = os.path.join(skill_dir, "_meta.json")
    if os.path.exists(meta_path):
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
        print(f"   名称：{meta.get('skill', {}).get('name', '未知')}")
        print(f"   ID: {meta.get('name', '未知')}")
        print(f"   版本：{meta.get('version', '1.0.0')}")
        print(f"   许可证：{meta.get('license', 'MIT')}")
        print()
    else:
        print("   ⚠️  未找到 _meta.json")
        print()
    
    # 4. 完整性检查
    print("4. 完整性检查:")
    if not missing and os.path.exists(meta_path):
        print("   ✅ 完整 - 可以发布")
    else:
        print("   ❌ 不完整 - 需要修复")
    print()
    
    # 5. 打包信息
    print("5. 打包信息:")
    print(f"   技能名称：{skill_name}")
    print(f"   文件大小：{total_size/1024:.1f} KB")
    print(f"   文件数量：{file_count}")
    print(f"   完整性：{'✅ 完整' if not missing else '❌ 不完整'}")
    print(f"   生成时间：{datetime.now().isoformat()}")
    print()
    
    # 6. 发布建议
    print("6. 发布建议:")
    if not missing:
        print("   ✅ 可以直接发布到 ClawHub")
        print(f"   \n命令:")
        print(f"   clawhub publish . \\")
        print(f"     --slug {meta.get('name', skill_name)} \\")
        print(f"     --name '{meta.get('skill', {}).get('name', 'NSAP')}' \\")
        print(f"     --version {meta.get('version', '1.0.0')} \\")
        print(f"     --changelog 'v1.0.0 初始发布：神经稀疏异步处理架构'")
    else:
        print("   ❌ 请先修复缺失文件")
    
    print("\n=== 验证完成 ===")


if __name__ == "__main__":
    main()
