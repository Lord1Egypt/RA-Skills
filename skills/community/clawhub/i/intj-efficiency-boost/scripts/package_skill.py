#!/usr/bin/env python3
"""
INTJ Efficiency Boost Skill Packager
打包技能为 .skill 文件
"""

import os
import json
import zipfile
import hashlib
from pathlib import Path
from datetime import datetime

def calculate_checksum(file_path: Path) -> str:
    """计算文件 SHA256 校验和"""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def get_safe_files(skill_path: Path) -> list[Path]:
    """获取需要打包的安全文件列表"""
    safe_extensions = {".md", ".json", ".py", ".sh", ".txt", ".yaml", ".yml"}
    skip_dirs = {"__pycache__", ".git", "node_modules", ".venv"}
    skip_files = {".DS_Store", "Thumbs.db"}
    
    files = []
    for root, dirs, filenames in os.walk(skill_path):
        # 过滤目录
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        root_path = Path(root)
        for filename in filenames:
            if filename in skip_files:
                continue
            file_path = root_path / filename
            if file_path.suffix in safe_extensions:
                files.append(file_path)
    
    return files

def package_skill(skill_path: Path, output_dir: Path) -> Path:
    """打包技能为 .skill 文件"""
    skill_name = skill_path.name
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = output_dir / f"{skill_name}_{timestamp}.skill"
    
    # 读取 meta
    meta_file = skill_path / "_meta.json"
    if meta_file.exists():
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
    else:
        meta = {}
    
    # 创建 manifest
    manifest = {
        "name": skill_name,
        "version": meta.get("version", "1.0.0"),
        "packaged_at": datetime.now().isoformat(),
        "files": []
    }
    
    # 打包文件
    with zipfile.ZipFile(output_file, "w", zipfile.ZIP_DEFLATED) as zf:
        # 添加 manifest
        manifest_json = json.dumps(manifest, indent=2, ensure_ascii=False)
        zf.writestr("manifest.json", manifest_json)
        
        # 添加所有安全文件
        for file_path in get_safe_files(skill_path):
            rel_path = file_path.relative_to(skill_path)
            zf.write(file_path, rel_path)
            
            # 更新 manifest
            manifest["files"].append({
                "path": str(rel_path),
                "checksum": calculate_checksum(file_path)
            })
    
    # 更新 manifest 文件
    with zipfile.ZipFile(output_file, "a") as zf:
        zf.writestr("manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False))
    
    return output_file

def main():
    skill_path = Path(__file__).parent.parent
    output_dir = skill_path.parent
    
    print(f"Packaging skill: {skill_path.name}")
    print("-" * 50)
    
    try:
        output_file = package_skill(skill_path, output_dir)
        print(f"[SUCCESS] Package created: {output_file}")
        print(f"[INFO] File size: {output_file.stat().st_size:,} bytes")
        return 0
    except Exception as e:
        print(f"[ERROR] Packaging failed: {e}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())
