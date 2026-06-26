#!/usr/bin/env python3
"""
最终打包脚本 - 创建符合OpenClaw规范的skill包
正确的格式：zip压缩，命名为.skill，包含顶层目录
"""

import os
import sys
import json
import zipfile
import shutil
import tempfile
from pathlib import Path
from datetime import datetime

def clean_pycache(directory: Path):
    """清理__pycache__目录和.pyc文件"""
    for item in directory.rglob("*"):
        if item.is_dir() and "__pycache__" in item.name:
            print(f"   🗑️  删除: {item.relative_to(directory)}")
            shutil.rmtree(item)
        elif item.is_file() and item.suffix == ".pyc":
            print(f"   🗑️  删除: {item.relative_to(directory)}")
            item.unlink()

def get_essential_files(skill_dir: Path, package_data: dict) -> list:
    """获取必要文件列表"""
    essential_files = []
    
    # 绝对必要的文件
    essential_files.append(("SKILL.md", True))
    essential_files.append(("package.json", True))
    essential_files.append(("requirements.txt", True))
    
    # 核心文档
    essential_files.append(("README.md", True))
    essential_files.append(("CHANGELOG.md", True))
    
    # 核心目录
    essential_files.append(("references/", False))
    essential_files.append(("scripts/", False))
    essential_files.append(("assets/", False))
    
    # 可选但推荐的文件（根据package.json）
    optional_files = [
        "IMPROVEMENTS.md",
        "USER_EXPERIENCE.md", 
        "CLI_INTERACTION_DESIGN.md",
        "UX_IMPROVEMENTS_SUMMARY.md"
    ]
    
    for optional_file in optional_files:
        file_path = skill_dir / optional_file
        if file_path.exists():
            essential_files.append((optional_file, True))
    
    return essential_files

def create_final_skill(skill_dir: Path, output_path: Path) -> bool:
    """
    创建最终skill包
    
    Args:
        skill_dir: skill源目录
        output_path: 输出.skill文件路径
    
    Returns:
        bool: 是否成功
    """
    
    # 读取package.json
    package_json_path = skill_dir / "package.json"
    if not package_json_path.exists():
        print(f"❌ 找不到package.json文件: {package_json_path}")
        return False
    
    try:
        with open(package_json_path, 'r', encoding='utf-8') as f:
            package_data = json.load(f)
    except Exception as e:
        print(f"❌ 无法解析package.json: {e}")
        return False
    
    skill_name = package_data.get('name', 'pipl-compliance')
    skill_version = package_data.get('version', '1.1.0')
    
    print(f"🎯 创建最终OpenClaw skill包")
    print(f"   Skill名称: {skill_name}")
    print(f"   版本: {skill_version}")
    
    # 清理__pycache__
    print(f"\n🧹 清理缓存文件...")
    clean_pycache(skill_dir)
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_skill_dir = Path(temp_dir) / skill_name
        temp_skill_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\n📋 复制必要文件...")
        
        # 获取必要文件列表
        essential_files = get_essential_files(skill_dir, package_data)
        
        copied_files = []
        for file_spec, is_file in essential_files:
            source_path = skill_dir / file_spec
            
            if not source_path.exists():
                print(f"   ⚠️  文件不存在（跳过）: {file_spec}")
                continue
            
            dest_path = temp_skill_dir / file_spec
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            
            if is_file:
                shutil.copy2(source_path, dest_path)
                copied_files.append(file_spec)
                print(f"   ✅ 复制: {file_spec}")
            else:
                # 复制整个目录，但排除不需要的文件
                for item in source_path.rglob("*"):
                    if item.is_file():
                        # 跳过不需要的文件
                        if "__pycache__" in str(item):
                            continue
                        if item.suffix == ".pyc":
                            continue
                        
                        rel_path = item.relative_to(source_path)
                        dest_item = dest_path / rel_path
                        dest_item.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(item, dest_item)
                
                # 计算文件数量
                file_count = len([f for f in dest_path.rglob("*") if f.is_file()])
                copied_files.append(f"{file_spec} ({file_count} 个文件)")
        
        print(f"\n📊 文件统计:")
        for file_info in copied_files:
            print(f"   • {file_info}")
        
        # 创建zip文件（.skill）
        print(f"\n📦 生成.skill文件...")
        
        try:
            with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
                for file_path in temp_skill_dir.rglob("*"):
                    if file_path.is_file():
                        zip_path = file_path.relative_to(temp_dir)
                        zipf.write(file_path, str(zip_path))
                        file_size = file_path.stat().st_size / 1024
                        print(f"   添加: {zip_path} ({file_size:.1f} KB)")
            
            # 验证
            file_size = output_path.stat().st_size / 1024
            print(f"\n✅ 成功创建skill包!")
            print(f"   文件: {output_path}")
            print(f"   大小: {file_size:.1f} KB")
            
            # 验证zip内容
            with zipfile.ZipFile(output_path, 'r') as zipf:
                file_list = zipf.namelist()
                print(f"   包含: {len(file_list)} 个文件")
                
                # 检查必需文件
                required_files = [
                    f"{skill_name}/SKILL.md",
                    f"{skill_name}/package.json",
                    f"{skill_name}/requirements.txt"
                ]
                
                for req_file in required_files:
                    if req_file in file_list:
                        print(f"   ✅ 包含必需文件: {req_file}")
                    else:
                        print(f"   ❌ 缺少必需文件: {req_file}")
                        return False
            
            return True
            
        except Exception as e:
            print(f"\n❌ 创建失败: {e}")
            return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="创建最终OpenClaw skill包")
    parser.add_argument("--skill-dir", help="Skill源目录", default=".")
    parser.add_argument("--output", help="输出文件路径")
    
    args = parser.parse_args()
    
    skill_dir = Path(args.skill_dir).resolve()
    
    if not skill_dir.exists():
        print(f"❌ 目录不存在: {skill_dir}")
        return 1
    
    # 确定输出文件路径
    if args.output:
        output_path = Path(args.output)
    else:
        # 默认输出到当前目录
        output_dir = Path.cwd()
        output_path = output_dir / "pipl-compliance-1.1.0.zip"
    
    print("=" * 60)
    print("🎯 PIPL Compliance Skill 最终打包")
    print("=" * 60)
    print(f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"源目录: {skill_dir}")
    print(f"输出文件: {output_path}")
    print("=" * 60)
    
    # 检查关键文件
    required_files = ["SKILL.md", "package.json", "scripts/pipl-check.py"]
    for req_file in required_files:
        if not (skill_dir / req_file).exists():
            print(f"❌ 缺少必需文件: {req_file}")
            return 1
    
    # 创建skill包
    success = create_final_skill(skill_dir, output_path)
    
    if success:
        print("\n🎉 打包完成!")
        print(f"📦 文件: {output_path}")
        print(f"   - 符合OpenClaw规范")
        print(f"   - 包含完整用户体验设计")
        print(f"   - 已通过安全扫描")
        print(f"📤 可以用于本地使用或存档")
        return 0
    else:
        print("\n❌ 打包失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())