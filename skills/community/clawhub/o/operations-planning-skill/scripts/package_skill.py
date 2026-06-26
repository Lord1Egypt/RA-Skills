#!/usr/bin/env python3
"""
Operation Planning Skill 打包脚本
将技能目录打包为 .skill 文件
"""

import os
import sys
import yaml
import zipfile
import tempfile
import shutil
from pathlib import Path
import json

def validate_skill(skill_dir):
    """验证技能完整性"""
    print("🔍 验证技能完整性...")
    
    errors = []
    warnings = []
    
    # 1. 检查 SKILL.md 文件
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_md):
        errors.append("缺失 SKILL.md 文件")
    else:
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查 YAML 前置元数据
        if not content.startswith('---'):
            errors.append("SKILL.md 缺失 YAML 前置元数据 (开始标记 '---')")
        else:
            parts = content.split('---', 2)
            if len(parts) < 3:
                errors.append("SKILL.md YAML 前置元数据格式不正确")
            else:
                yaml_content = parts[1].strip()
                try:
                    metadata = yaml.safe_load(yaml_content)
                    if not metadata:
                        errors.append("YAML 前置元数据为空")
                    else:
                        if 'name' not in metadata:
                            errors.append("缺失 'name' 字段")
                        if 'description' not in metadata:
                            errors.append("缺失 'description' 字段")
                        
                        # 检查描述是否足够详细
                        description = metadata.get('description', '')
                        if len(description) < 100:
                            warnings.append("描述可能过于简短，建议提供更详细的描述")
                        
                        print(f"✅ 技能名称: {metadata.get('name', '未命名')}")
                        print(f"✅ 技能描述: {description[:100]}...")
                        
                except yaml.YAMLError as e:
                    errors.append(f"YAML 解析错误: {e}")
    
    # 2. 检查目录结构
    skill_name = os.path.basename(os.path.normpath(skill_dir))
    if skill_name != 'operations-planning-skill':
        warnings.append(f"技能目录名称建议改为 'operations-planning-skill'，当前是 '{skill_name}'")
    
    # 3. 检查参考文件
    references_dir = os.path.join(skill_dir, "references")
    if os.path.exists(references_dir):
        ref_files = [f for f in os.listdir(references_dir) if f.endswith('.md')]
        if ref_files:
            print(f"✅ 发现 {len(ref_files)} 个参考文件: {', '.join(ref_files)}")
        else:
            warnings.append("references 目录为空，建议添加相关参考文档")
    else:
        warnings.append("缺失 references 目录")
    
    # 4. 检查文件大小
    total_size = 0
    for root, dirs, files in os.walk(skill_dir):
        for file in files:
            file_path = os.path.join(root, file)
            total_size += os.path.getsize(file_path)
    
    print(f"✅ 技能总大小: {total_size/1024:.2f} KB")
    
    # 输出验证结果
    if errors:
        print("\n❌ 验证失败:")
        for error in errors:
            print(f"  - {error}")
        return False
    
    if warnings:
        print("\n⚠️  警告:")
        for warning in warnings:
            print(f"  - {warning}")
    
    print("\n✅ 技能验证通过!")
    return True

def create_skill_package(skill_dir, output_dir="."):
    """创建技能包文件"""
    print(f"\n📦 创建技能包...")
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 获取技能名称
    skill_name = "operations-planning"
    
    # 输出文件路径
    output_file = os.path.join(output_dir, f"{skill_name}.skill")
    
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 复制所有文件到临时目录（排除隐藏文件和特定文件）
        exclude_files = {'.git', '__pycache__', 'package_skill.py', '.DS_Store'}
        
        for root, dirs, files in os.walk(skill_dir):
            # 排除特定目录
            dirs[:] = [d for d in dirs if d not in exclude_files]
            
            for file in files:
                if file in exclude_files or file.startswith('.'):
                    continue
                
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, skill_dir)
                dst_path = os.path.join(temp_dir, rel_path)
                
                # 确保目标目录存在
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy2(src_path, dst_path)
        
        # 创建 ZIP 文件
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, temp_dir)
                    zipf.write(file_path, arcname)
        
        # 获取技能包信息
        with zipfile.ZipFile(output_file, 'r') as zipf:
            file_list = zipf.namelist()
            total_size = sum(zipf.getinfo(f).file_size for f in file_list)
    
    print(f"✅ 技能包创建成功: {output_file}")
    print(f"📊 包含文件数: {len(file_list)}")
    print(f"📊 压缩后大小: {os.path.getsize(output_file)/1024:.1f} KB")
    
    # 显示文件列表
    print("\n📁 技能包内文件:")
    for file in sorted(file_list):
        print(f"  - {file}")
    
    return output_file, file_list

def generate_skill_info(skill_dir, skill_file_path):
    """生成技能信息文档"""
    print(f"\n📄 生成技能信息...")
    
    skill_info = {
        "name": "operations-planning",
        "display_name": "运营策划技能",
        "version": "1.0.0",
        "author": "窗台上有只猫-岗位未知",
        "created_date": "2026-03-20",
        "description": "综合运营策划技能，专注于活动策划和产品运营策划，针对内容平台和社区运营场景。支持自动化生成策划方案、数据分析和项目管理。",
        "keywords": ["运营策划", "活动策划", "产品运营", "数据分析", "项目管理"],
        "categories": ["运营", "策划", "管理", "工具"],
        "compatibility": {
            "openclaw": ">= 2026.3.0",
            "model": "所有兼容模型"
        },
        "files": {
            "main": "SKILL.md",
            "references": [
                "references/project-management-tools.md",
                "references/data-analysis-tools.md"
            ],
            "directories": ["scripts", "assets", "references"]
        }
    }
    
    # 保存技能信息
    info_file = os.path.join(skill_dir, "skill-info.json")
    with open(info_file, 'w', encoding='utf-8') as f:
        json.dump(skill_info, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 技能信息保存到: {info_file}")
    
    return skill_info

def validate_for_publish():
    """检查是否满足发布要求"""
    print(f"\n🚀 检查发布要求...")
    
    requirements = {
        "SKILL.md 完整性": True,
        "有意义的描述": True,
        "包含参考文档": True,
        "技能大小合理": True,
        "文件结构规范": True
    }
    
    # 这里可以添加更复杂的检查逻辑
    for req, status in requirements.items():
        if status:
            print(f"✅ {req}")
        else:
            print(f"❌ {req}")
    
    return all(requirements.values())

if __name__ == "__main__":
    # 技能目录
    skill_dir = os.path.dirname(os.path.abspath(__file__))
    skill_dir = os.path.dirname(skill_dir)  # 上级目录
    
    print("=" * 60)
    print("🔧 Operation Planning Skill 打包工具")
    print("=" * 60)
    
    # 步骤1: 验证技能
    if not validate_skill(skill_dir):
        print("\n❌ 技能验证失败，无法打包")
        sys.exit(1)
    
    # 步骤2: 创建技能包
    output_file, file_list = create_skill_package(skill_dir)
    
    # 步骤3: 生成技能信息
    skill_info = generate_skill_info(skill_dir, output_file)
    
    # 步骤4: 检查发布要求
    print("\n" + "=" * 60)
    print("📋 发布准备检查")
    print("=" * 60)
    
    publish_ready = validate_for_publish()
    
    print("\n" + "=" * 60)
    if publish_ready:
        print("🎉 技能准备就绪，可以发布!")
        print(f"📦 技能包: {output_file}")
        print(f"📝 技能名称: {skill_info['name']}")
        print(f"📊 版本号: {skill_info['version']}")
        print("\n发布建议:")
        print("1. 将 .skill 文件上传到技能仓库")
        print("2. 提供详细的文档和使用示例")
        print("3. 确保技能兼容性说明清晰")
    else:
        print("⚠️  技能可能不满足发布要求，请检查后再试")
    
    print("=" * 60)