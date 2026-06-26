#!/usr/bin/env python3
"""
Max-Self-Improvement Skill 打包脚本
将技能打包为 .skill 文件用于分发
"""

import os
import zipfile
import json
from pathlib import Path
from datetime import datetime


def get_excluded_patterns():
    """排除的文件模式"""
    return {
        '__pycache__', '.pyc', '.git', '.DS_Store',
        'Thumbs.db', '*.log', '.env', 'node_modules'
    }


def should_exclude(path: Path) -> bool:
    """检查是否应排除文件"""
    name = path.name
    for pattern in get_excluded_patterns():
        if pattern.startswith('*'):
            if name.endswith(pattern[1:]):
                return True
        elif name == pattern or pattern in path.parts:
            return True
    return False


def package_skill(skill_path: Path, output_dir: Path) -> Path:
    """打包技能为 .skill 文件"""
    
    if not skill_path.exists():
        raise FileNotFoundError(f"Skill path not found: {skill_path}")
    
    # 读取 meta 获取版本信息
    meta_path = skill_path / "_meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
        skill_name = meta.get("id", skill_path.name)
        version = meta.get("version", "1.0.0")
    else:
        skill_name = skill_path.name
        version = "1.0.0"
    
    # 生成输出文件名
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = output_dir / f"{skill_name}_v{version}_{timestamp}.skill"
    
    # 创建 zip 包
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_path):
            # 过滤目录
            dirs[:] = [d for d in dirs if not should_exclude(Path(d))]
            
            for file in files:
                file_path = Path(root) / file
                if should_exclude(file_path):
                    continue
                
                # 计算相对路径
                arcname = file_path.relative_to(skill_path)
                zf.write(file_path, arcname)
    
    return output_file


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Package Max-Self-Improvement skill")
    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="Path to skill directory (default: script's parent directory)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output directory for .skill file (default: current directory)"
    )
    
    args = parser.parse_args()
    
    # 确定路径
    if args.path:
        skill_path = Path(args.path).resolve()
    else:
        skill_path = Path(__file__).parent.parent.resolve()
    
    output_dir = Path(args.output).resolve() if args.output else Path.cwd()
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Packaging skill from: {skill_path}")
    print(f"Output directory: {output_dir}")
    print("-" * 50)
    
    try:
        output_file = package_skill(skill_path, output_dir)
        print(f"Packaged successfully: {output_file}")
        
        # 显示包内容
        with zipfile.ZipFile(output_file, 'r') as zf:
            print("\nPackage contents:")
            for name in sorted(zf.namelist()):
                info = zf.getinfo(name)
                print(f"  {name} ({info.file_size} bytes)")
        
        print(f"\nTotal files: {len(zf.namelist())}")
        
    except Exception as e:
        print(f"Packaging failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    main()
