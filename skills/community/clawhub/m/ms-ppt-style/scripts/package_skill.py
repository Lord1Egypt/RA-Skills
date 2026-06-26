#!/usr/bin/env python3
"""
Package a skill into a .skill file for distribution.
"""

import os
import sys
import zipfile
import yaml
from pathlib import Path

def validate_skill(skill_dir):
    """Validate skill structure."""
    skill_path = Path(skill_dir)
    
    # Check SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print("❌ ERROR: SKILL.md not found")
        return False
    
    # Parse YAML frontmatter
    content = skill_md.read_text()
    if not content.startswith("---"):
        print("❌ ERROR: SKILL.md missing YAML frontmatter")
        return False
    
    try:
        _, yaml_content, _ = content.split("---", 2)
        metadata = yaml.safe_load(yaml_content)
        
        if "name" not in metadata:
            print("❌ ERROR: Missing 'name' in frontmatter")
            return False
        if "description" not in metadata:
            print("❌ ERROR: Missing 'description' in frontmatter")
            return False
            
        print(f"✅ Skill validated: {metadata['name']}")
        return True
        
    except Exception as e:
        print(f"❌ ERROR: Invalid YAML frontmatter: {e}")
        return False

def package_skill(skill_dir, output_dir=None):
    """Package skill into .skill file."""
    skill_path = Path(skill_dir)
    skill_name = skill_path.name
    
    # Validate first
    if not validate_skill(skill_dir):
        sys.exit(1)
    
    # Determine output path
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = skill_path.parent
    
    # Create .skill file (zip with .skill extension)
    skill_file = output_path / f"{skill_name}.skill"
    
    with zipfile.ZipFile(skill_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in skill_path.rglob("*"):
            if file_path.is_file():
                # Skip node_modules and hidden files
                if "node_modules" in str(file_path):
                    continue
                if file_path.name.startswith("."):
                    continue
                
                arcname = file_path.relative_to(skill_path)
                zf.write(file_path, arcname)
                print(f"  📦 {arcname}")
    
    print(f"\n✅ Skill packaged: {skill_file}")
    print(f"   Size: {skill_file.stat().st_size / 1024:.1f} KB")
    return skill_file

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: package_skill.py <skill-folder> [output-dir]")
        sys.exit(1)
    
    skill_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    package_skill(skill_dir, output_dir)
