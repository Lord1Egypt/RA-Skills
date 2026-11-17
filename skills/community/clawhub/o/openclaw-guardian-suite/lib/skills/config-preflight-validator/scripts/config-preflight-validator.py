#!/usr/bin/env python3
# [OC-WM] licensed-to: macmini@MacminideMac-mini | bundle: vendor-suite | ts: 2026-03-09T17:30:16Z
"""
config-preflight-validator.py — OpenClaw 配置预校验工具
======================================================

在执行 config.patch 或直接修改 openclaw.json 前，进行本地 Schema 验证。
解决 "Validation issues" 错误信息模糊的问题。

用法:
  python3 config-preflight-validator.py --patch '{"plugins": {"allow": ["new-plugin"]}}'
  python3 config-preflight-validator.py --file openclaw.json
"""

import json
import sys
import os
import argparse
from pathlib import Path

# 默认 Schema 路径（如果本地有缓存的话）
SCHEMA_CACHE = Path.home() / ".openclaw" / "workspace" / ".lib" / "openclaw_schema.json"

def get_live_schema():
    """尝试从 gateway 获取最新 schema"""
    import subprocess
    try:
        # 优先使用 openclaw CLI 获取
        result = subprocess.run(["openclaw", "gateway", "config.schema"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            schema = json.loads(result.stdout)
            # 缓存一份
            SCHEMA_CACHE.parent.mkdir(parents=True, exist_ok=True)
            SCHEMA_CACHE.write_text(json.dumps(schema, indent=2))
            return schema
    except Exception:
        pass
    
    # 尝试读取缓存
    if SCHEMA_CACHE.exists():
        try:
            return json.loads(SCHEMA_CACHE.read_text())
        except Exception:
            pass
    
    return None

def validate_patch(patch_data, schema=None):
    """验证补丁是否合法（简单逻辑实现，完整验证需 jsonschema 库）"""
    errors = []
    
    # 如果没有 jsonschema 库，我们至少做基础检查
    try:
        import jsonschema
        if schema:
            jsonschema.validate(instance=patch_data, schema=schema)
            return True, []
    except ImportError:
        errors.append("⚠️ 警告: 未安装 python-jsonschema，仅执行基础语法检查。")
    except Exception as e:
        return False, [str(e)]

    # 基础手动校验（针对常见错误：plugins.allow 必须是列表等）
    if "plugins" in patch_data:
        p = patch_data["plugins"]
        if "allow" in p and not isinstance(p["allow"], list):
            errors.append("Error: 'plugins.allow' 必须是一个字符串列表 (Array of strings)")
        if "deny" in p and not isinstance(p["deny"], list):
            errors.append("Error: 'plugins.deny' 必须是一个字符串列表 (Array of strings)")
            
    if "channels" in patch_data:
        if not isinstance(patch_data["channels"], dict):
            errors.append("Error: 'channels' 必须是一个对象 (Object)")

    return len(errors) == 0, errors

def main():
    parser = argparse.ArgumentParser(description="OpenClaw 配置预校验工具")
    parser.add_argument("--patch", help="JSON 格式的补丁内容")
    parser.add_argument("--file", help="要验证的完整配置文件路径")
    parser.add_argument("--update-schema", action="store_true", help="强制更新本地 Schema 缓存")
    
    args = parser.parse_args()
    
    if args.update_schema:
        schema = get_live_schema()
        if schema:
            print("✅ Schema 缓存已更新")
        else:
            print("❌ 无法获取最新 Schema")
        return

    schema = get_live_schema()
    
    target_data = None
    if args.patch:
        try:
            target_data = json.loads(args.patch)
        except json.JSONDecodeError as e:
            print(f"❌ 补丁 JSON 语法错误: {e}")
            sys.exit(1)
    elif args.file:
        try:
            target_data = json.loads(Path(args.file).read_text())
        except Exception as e:
            print(f"❌ 配置文件读取失败: {e}")
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(0)

    ok, errors = validate_patch(target_data, schema)
    
    if ok:
        print("✅ 校验通过！该配置/补丁符合基础规范。")
        if not schema:
            print("💡 提示：未检测到有效 Schema，仅执行了硬编码规则检查。")
    else:
        print("❌ 校验失败：")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

if __name__ == "__main__":
    main()
