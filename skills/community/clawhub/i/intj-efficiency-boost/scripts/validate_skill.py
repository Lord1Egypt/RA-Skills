#!/usr/bin/env python3
"""
INTJ Efficiency Boost Skill Validator
验证技能文件的结构和内容规范
"""

import os
import json
import re
import sys
from pathlib import Path

def validate_frontmatter(skill_path: Path) -> tuple[bool, str]:
    """验证 SKILL.md frontmatter 格式"""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"
    
    content = skill_md.read_text(encoding="utf-8")
    
    # 检查第一行必须是 ---
    lines = content.split("\n")
    if not lines or lines[0].strip() != "---":
        return False, "SKILL.md must start with --- (frontmatter delimiter)"
    
    # 查找 frontmatter 结束标记
    end_idx = -1
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            end_idx = i
            break
    
    if end_idx == -1:
        return False, "Frontmatter missing closing ---"
    
    # 解析 frontmatter
    frontmatter_text = "\n".join(lines[1:end_idx])
    try:
        # 简单 YAML 解析
        fm = {}
        for line in frontmatter_text.split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                fm[key.strip()] = value.strip().strip('"').strip("'")
    except Exception as e:
        return False, f"Frontmatter parse error: {e}"
    
    # 检查必填字段
    if "name" not in fm:
        return False, "Frontmatter missing 'name' field"
    if "description" not in fm:
        return False, "Frontmatter missing 'description' field"
    
    # 检查 name 格式（连字符）
    name = fm.get("name", "")
    if not re.match(r'^[a-z0-9-]+$', name):
        return False, f"name '{name}' should use hyphen-case (lowercase with hyphens)"
    
    # 检查 name 与文件夹名一致
    folder_name = skill_path.name
    if name != folder_name:
        return False, f"name '{name}' should match folder name '{folder_name}'"
    
    return True, "Frontmatter validation passed"

def validate_meta(skill_path: Path) -> tuple[bool, str]:
    """验证 _meta.json"""
    meta_file = skill_path / "_meta.json"
    if not meta_file.exists():
        return False, "_meta.json not found"
    
    try:
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return False, f"_meta.json parse error: {e}"
    
    # 检查必填字段
    if "id" not in meta:
        return False, "_meta.json missing 'id'"
    if "version" not in meta:
        return False, "_meta.json missing 'version'"
    
    return True, "_meta.json validation passed"

def validate_structure(skill_path: Path) -> tuple[bool, list[str]]:
    """验证目录结构"""
    errors = []
    
    # 必须存在的文件
    required_files = ["SKILL.md", "_meta.json"]
    for f in required_files:
        if not (skill_path / f).exists():
            errors.append(f"Missing required file: {f}")
    
    # 推荐的目录（可选）
    recommended_dirs = ["scripts", "references", "assets"]
    for d in recommended_dirs:
        dir_path = skill_path / d
        if dir_path.exists() and not any(dir_path.iterdir()):
            errors.append(f"Directory '{d}' is empty")
    
    return len(errors) == 0, errors

def main():
    skill_path = Path(__file__).parent.parent
    
    print(f"Validating skill at: {skill_path}")
    print("-" * 50)
    
    all_passed = True
    
    # 验证 frontmatter
    passed, msg = validate_frontmatter(skill_path)
    print(f"[{'PASS' if passed else 'FAIL'}] Frontmatter: {msg}")
    all_passed = all_passed and passed
    
    # 验证 _meta.json
    passed, msg = validate_meta(skill_path)
    print(f"[{'PASS' if passed else 'FAIL'}] Meta: {msg}")
    all_passed = all_passed and passed
    
    # 验证结构
    passed, errors = validate_structure(skill_path)
    if passed:
        print(f"[PASS] Structure: All required files present")
    else:
        for err in errors:
            print(f"[FAIL] Structure: {err}")
        all_passed = False
    
    print("-" * 50)
    print(f"Overall: {'ALL PASSED' if all_passed else 'SOME FAILED'}")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
