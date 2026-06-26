#!/usr/bin/env python3
"""
Max-Self-Improvement Skill 验证脚本
验证 SKILL.md frontmatter 格式和目录结构
"""

import os
import re
import sys
from pathlib import Path

def validate_frontmatter(skill_path: Path) -> tuple[bool, list[str]]:
    """验证 frontmatter 格式"""
    errors = []
    skill_md = skill_path / "SKILL.md"
    
    if not skill_md.exists():
        return False, ["SKILL.md not found"]
    
    content = skill_md.read_text(encoding="utf-8")
    
    # 检查是否以 --- 开头
    if not content.startswith("---"):
        errors.append("SKILL.md must start with --- (frontmatter delimiter)")
        return False, errors
    
    # 提取 frontmatter
    frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not frontmatter_match:
        errors.append("Cannot parse frontmatter block")
        return False, errors
    
    frontmatter = frontmatter_match.group(1)
    
    # 检查必需字段
    required_fields = ["name", "description"]
    for field in required_fields:
        if not re.search(rf'^{field}:', frontmatter, re.MULTILINE):
            errors.append(f"Missing required field: {field}")
    
    # 检查 name 格式（连字符）
    name_match = re.search(r'^name:\s*(.+)', frontmatter, re.MULTILINE)
    if name_match:
        name = name_match.group(1).strip()
        if not re.match(r'^[a-z0-9-]+$', name):
            errors.append(f"name '{name}' must be lowercase with hyphens only")
    
    return len(errors) == 0, errors


def validate_meta_json(skill_path: Path) -> tuple[bool, list[str]]:
    """验证 _meta.json"""
    import json
    errors = []
    meta_path = skill_path / "_meta.json"
    
    if not meta_path.exists():
        return False, ["_meta.json not found"]
    
    try:
        meta = json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        return False, [f"Invalid JSON: {e}"]
    
    required_fields = ["id", "version"]
    for field in required_fields:
        if field not in meta:
            errors.append(f"Missing required field in _meta.json: {field}")
    
    # 检查 version 格式
    if "version" in meta:
        if not re.match(r'^\d+\.\d+\.\d+$', meta["version"]):
            errors.append("version must be semantic format (e.g., 1.0.0)")
    
    return len(errors) == 0, errors


def validate_structure(skill_path: Path) -> tuple[bool, list[str]]:
    """验证目录结构"""
    errors = []
    
    # 检查必需的目录和文件
    required = ["SKILL.md", "_meta.json"]
    for item in required:
        if not (skill_path / item).exists():
            errors.append(f"Missing required file: {item}")
    
    return len(errors) == 0, errors


def main():
    skill_path = Path(__file__).parent.parent.resolve()
    
    print(f"Validating skill at: {skill_path}")
    print("-" * 50)
    
    all_passed = True
    
    # 1. 结构验证
    passed, errors = validate_structure(skill_path)
    if passed:
        print("[PASS] Structure validation")
    else:
        print("[FAIL] Structure validation")
        for e in errors:
            print(f"  - {e}")
        all_passed = False
    
    # 2. Frontmatter 验证
    passed, errors = validate_frontmatter(skill_path)
    if passed:
        print("[PASS] Frontmatter validation")
    else:
        print("[FAIL] Frontmatter validation")
        for e in errors:
            print(f"  - {e}")
        all_passed = False
    
    # 3. Meta JSON 验证
    passed, errors = validate_meta_json(skill_path)
    if passed:
        print("[PASS] _meta.json validation")
    else:
        print("[FAIL] _meta.json validation")
        for e in errors:
            print(f"  - {e}")
        all_passed = False
    
    print("-" * 50)
    if all_passed:
        print("All validations passed!")
        sys.exit(0)
    else:
        print("Validation failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
