#!/usr/bin/env python3
"""
将README.md的精华内容整合到SKILL.md中
创建一个统一的高质量skill文档
"""

import os
import re
from pathlib import Path
from typing import List, Tuple

def extract_readme_sections(readme_path: Path) -> dict:
    """提取README.md的精华部分"""
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    sections = {}
    
    # 提取快速体验部分
    quick_start_match = re.search(r'## 📸 快速体验.*?\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if quick_start_match:
        sections['quick_experience'] = quick_start_match.group(1).strip()
    
    # 提取核心功能对比
    comparison_match = re.search(r'## 📊 核心功能对比.*?\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if comparison_match:
        sections['feature_comparison'] = comparison_match.group(1).strip()
    
    # 提取实际功能演示
    demo_match = re.search(r'## 🎨 实际功能演示.*?\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if demo_match:
        sections['feature_demo'] = demo_match.group(1).strip()
    
    # 提取实际工具列表
    tools_match = re.search(r'## 🔧 实际工具列表.*?\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if tools_match:
        sections['tools_list'] = tools_match.group(1).strip()
    
    # 提取版本路线图
    roadmap_match = re.search(r'## 🗺️ 版本路线图.*?\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if roadmap_match:
        sections['roadmap'] = roadmap_match.group(1).strip()
    
    return sections

def integrate_sections(skill_content: str, readme_sections: dict) -> str:
    """将README的精华部分整合到SKILL.md中"""
    
    # 找到SKILL.md中的"快速开始"部分
    quick_start_pattern = r'(## 🚀 快速开始\n.*?\n)(?=## |\Z)'
    quick_start_match = re.search(quick_start_pattern, skill_content, re.DOTALL)
    
    if quick_start_match:
        # 在"快速开始"后面添加"快速体验"
        quick_start_section = quick_start_match.group(1)
        
        # 添加快速体验部分
        if 'quick_experience' in readme_sections:
            enhanced_section = quick_start_section + "\n\n" + "## 📸 快速体验（30秒上手）\n\n" + readme_sections['quick_experience']
            skill_content = skill_content.replace(quick_start_section, enhanced_section)
    
    # 在"核心功能"部分后添加"功能对比"
    core_features_pattern = r'(## 🎯 核心功能\n.*?\n)(?=## |\Z)'
    core_features_match = re.search(core_features_pattern, skill_content, re.DOTALL)
    
    if core_features_match and 'feature_comparison' in readme_sections:
        core_features_section = core_features_match.group(1)
        enhanced_section = core_features_section + "\n\n" + "## 📊 核心功能对比\n\n" + readme_sections['feature_comparison']
        skill_content = skill_content.replace(core_features_section, enhanced_section)
    
    # 在"详细使用指南"后添加"实际功能演示"
    usage_guide_pattern = r'(## 📋 详细使用指南\n.*?\n)(?=## |\Z)'
    usage_guide_match = re.search(usage_guide_pattern, skill_content, re.DOTALL)
    
    if usage_guide_match and 'feature_demo' in readme_sections:
        usage_guide_section = usage_guide_match.group(1)
        enhanced_section = usage_guide_section + "\n\n" + "## 🎨 实际功能演示\n\n" + readme_sections['feature_demo']
        skill_content = skill_content.replace(usage_guide_section, enhanced_section)
    
    # 在"文件结构"后添加"实际工具列表"
    file_structure_pattern = r'(## 📁 文件结构\n.*?\n)(?=## |\Z)'
    file_structure_match = re.search(file_structure_pattern, skill_content, re.DOTALL)
    
    if file_structure_match and 'tools_list' in readme_sections:
        file_structure_section = file_structure_match.group(1)
        enhanced_section = file_structure_section + "\n\n" + "## 🔧 实际工具列表\n\n" + readme_sections['tools_list']
        skill_content = skill_content.replace(file_structure_section, enhanced_section)
    
    # 在文档末尾添加"版本路线图"
    if 'roadmap' in readme_sections:
        # 找到最后一个部分
        last_section_pattern = r'(## 📞 支持与反馈\n.*?\n)(?=\Z)'
        last_section_match = re.search(last_section_pattern, skill_content, re.DOTALL)
        
        if last_section_match:
            last_section = last_section_match.group(1)
            enhanced_section = last_section + "\n\n" + "## 🗺️ 版本路线图\n\n" + readme_sections['roadmap']
            skill_content = skill_content.replace(last_section, enhanced_section)
    
    return skill_content

def main():
    """主函数"""
    skill_dir = Path.cwd()
    
    skill_path = skill_dir / "SKILL.md"
    readme_path = skill_dir / "README.md"
    
    if not skill_path.exists():
        print(f"❌ 找不到SKILL.md: {skill_path}")
        return 1
    
    if not readme_path.exists():
        print(f"❌ 找不到README.md: {readme_path}")
        return 1
    
    print("🔧 开始整合文档...")
    print(f"从: {readme_path}")
    print(f"到: {skill_path}")
    print("-" * 50)
    
    # 读取原始SKILL.md
    with open(skill_path, 'r', encoding='utf-8') as f:
        skill_content = f.read()
    
    # 提取README的精华部分
    readme_sections = extract_readme_sections(readme_path)
    
    print("✅ 提取的README精华部分:")
    for section_name in readme_sections:
        print(f"   • {section_name}")
    
    # 整合到SKILL.md
    integrated_content = integrate_sections(skill_content, readme_sections)
    
    # 保存整合后的SKILL.md
    integrated_path = skill_dir / "SKILL-integrated.md"
    with open(integrated_path, 'w', encoding='utf-8') as f:
        f.write(integrated_content)
    
    print("-" * 50)
    print(f"✅ 整合完成!")
    print(f"📄 输出文件: {integrated_path}")
    
    # 创建简化的README.md
    simplified_readme = f"""# PIPL Compliance Checker

**中国企业PIPL合规一站式解决方案**

## ⚠️ 重要说明

这是一个纯本地工具，所有功能在本地完成，不进行任何网络请求。

## 🚀 快速开始

详细使用说明请查看 **[SKILL.md](SKILL.md)**，这是本skill的核心文档。

## 📖 核心文档

- **[SKILL.md](SKILL.md)** - 完整的技能文档（推荐）
- **[USER_EXPERIENCE.md](USER_EXPERIENCE.md)** - 用户体验设计
- **[CLI_INTERACTION_DESIGN.md](CLI_INTERACTION_DESIGN.md)** - CLI交互设计
- **[ROADMAP.md](ROADMAP.md)** - 版本路线图

## 🔧 安装与使用

```bash
# 详细安装和使用说明请查看SKILL.md
pip install -r requirements.txt
python3 scripts/pipl-check.py --help
```

---

<div align="center">

**🛡️ 让PIPL合规变得简单、安全、高效！**

**详细文档：** [SKILL.md](SKILL.md)

</div>
"""
    
    simplified_readme_path = skill_dir / "README-simplified.md"
    with open(simplified_readme_path, 'w', encoding='utf-8') as f:
        f.write(simplified_readme)
    
    print(f"📄 简化版README: {simplified_readme_path}")
    print("\n🎉 文档整合完成！")
    print("现在您可以选择：")
    print("1. 使用 SKILL-integrated.md 作为主要文档")
    print("2. 使用 README-simplified.md 作为简化介绍")
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())