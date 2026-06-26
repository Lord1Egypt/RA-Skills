#!/usr/bin/env python3
"""
yaml-validator.py — 验证 Obsidian 笔记 frontmatter YAML 闭合。
用法: python scripts/yaml-validator.py <md文件路径>
返回: 0=正常, 1=frontmatter未闭合, 2=YAML解析错误, 3=文件不存在
"""

import sys, os, json

def validate(fp):
    if not os.path.isfile(fp):
        return 3, f"文件不存在: {fp}"
    with open(fp, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()

    if not content.startswith('---'):
        return 0, "没有 frontmatter（无 --- 开头，跳过）"

    # 找第二个 ---
    end = content.find('---', 3)
    if end == -1:
        return 1, f"frontmatter 未闭合：以 --- 开头但找不到结束 ---"

    fm_text = content[3:end].strip()
    if not fm_text:
        return 0, "frontmatter 为空"
    
    # 用 Python YAML 验证语法
    import yaml
    try:
        parsed = yaml.safe_load(fm_text)
        if not isinstance(parsed, dict):
            return 2, f"frontmatter YAML 解析结果不是 dict，而是 {type(parsed).__name__}"
        return 0, f"✅ frontmatter 正常（{len(parsed)} 个字段）"
    except yaml.YAMLError as e:
        return 2, f"❌ YAML 解析错误: {e}"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(json.dumps({"code": -1, "message": "用法: python yaml-validator.py <文件路径>"}, ensure_ascii=False))
        sys.exit(-1)
    code, msg = validate(sys.argv[1])
    print(json.dumps({"code": code, "message": msg}, ensure_ascii=False))
    sys.exit(code)
