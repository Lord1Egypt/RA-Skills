#!/usr/bin/env python3
"""
Skill打包脚本

将Skill打包为可安装的.skill文件。
"""

import os
import sys
import zipfile
import json
from pathlib import Path
from datetime import datetime


def package_skill(skill_dir: Path, output_dir: Path = None):
    """
    打包Skill
    
    Args:
        skill_dir: Skill目录
        output_dir: 输出目录
    """
    if output_dir is None:
        output_dir = skill_dir.parent
    
    skill_dir = Path(skill_dir)
    output_dir = Path(output_dir)
    
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        print(f"❌ SKILL.md not found in {skill_dir}")
        return False
    
    with open(skill_md, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not content.startswith('---'):
        print("❌ SKILL.md format error: missing YAML frontmatter")
        return False
    
    lines = content.split('\n')
    yaml_end = -1
    for i, line in enumerate(lines):
        if i > 0 and line.strip() == '---':
            yaml_end = i
            break
    
    if yaml_end == -1:
        print("❌ SKILL.md format error: invalid YAML frontmatter")
        return False
    
    yaml_content = '\n'.join(lines[1:yaml_end])
    
    try:
        import yaml
        metadata = yaml.safe_load(yaml_content)
    except:
        metadata = {}
        for line in lines[1:yaml_end]:
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip().strip('"\'')
    
    skill_name = metadata.get('name', skill_dir.name)
    version = metadata.get('version', '1.0.0')
    
    print(f"📦 Packaging skill: {skill_name} v{version}")
    
    output_file = output_dir / f"{skill_name}.skill"
    
    exclude_patterns = [
        '__pycache__',
        '*.pyc',
        '*.pyo',
        '.git',
        '.gitignore',
        '.DS_Store',
        'venv',
        'env',
        '*.egg-info',
        'data/radios/*.wav',
        'data/radios/*.json',
        '.skill'
    ]
    
    def should_exclude(path: Path) -> bool:
        """检查是否应该排除"""
        path_str = str(path)
        for pattern in exclude_patterns:
            if pattern.startswith('*'):
                if path_str.endswith(pattern[1:]):
                    return True
            elif pattern in path_str:
                return True
        return False
    
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(skill_dir):
            root_path = Path(root)
            
            dirs[:] = [d for d in dirs if not should_exclude(root_path / d)]
            
            for file in files:
                file_path = root_path / file
                
                if should_exclude(file_path):
                    continue
                
                arcname = file_path.relative_to(skill_dir)
                zipf.write(file_path, arcname)
                print(f"   Adding: {arcname}")
    
    file_size = output_file.stat().st_size
    file_size_mb = file_size / (1024 * 1024)
    
    print(f"\n✅ Skill packaged successfully!")
    print(f"   Output: {output_file}")
    print(f"   Size: {file_size_mb:.2f} MB")
    print(f"   Name: {skill_name}")
    print(f"   Version: {version}")
    
    metadata_file = output_dir / f"{skill_name}.metadata.json"
    with open(metadata_file, 'w', encoding='utf-8') as f:
        json.dump({
            'name': skill_name,
            'version': version,
            'packaged_at': datetime.now().isoformat(),
            'file_size': file_size,
            'metadata': metadata
        }, f, ensure_ascii=False, indent=2)
    
    print(f"   Metadata: {metadata_file}")
    
    return True


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Package OpenClaw Skill')
    parser.add_argument(
        'skill_dir',
        type=str,
        help='Skill directory path'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        help='Output directory (default: parent of skill_dir)'
    )
    
    args = parser.parse_args()
    
    skill_dir = Path(args.skill_dir)
    output_dir = Path(args.output_dir) if args.output_dir else None
    
    if not skill_dir.exists():
        print(f"❌ Skill directory not found: {skill_dir}")
        sys.exit(1)
    
    success = package_skill(skill_dir, output_dir)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
