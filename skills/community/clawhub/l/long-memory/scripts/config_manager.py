#!/usr/bin/env python3
"""配置验证与版本迁移：校验 long-memory.json 并处理版本升级"""

import argparse
import json
import re
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.filelock import safe_read_json, safe_write_json

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
CURRENT_VERSION = "5.0"

# 配置 schema
CONFIG_SCHEMA = {
    "version": {"type": str, "required": True, "pattern": r"^\d+\.\d+$"},
    "memory_dir": {"type": (str, type(None)), "required": False},
    "archive_days": {"type": int, "required": False, "min": 1, "max": 3650},
    "max_memory_md_size": {"type": int, "required": False, "min": 1000, "max": 100000},
    "auto_backup": {"type": dict, "required": False},
    "auto_backup.enabled": {"type": bool, "required": False},
    "auto_backup.git_remote": {"type": (str, type(None)), "required": False},
    "auto_backup.interval_hours": {"type": int, "required": False, "min": 1},
    "quality": {"type": dict, "required": False},
    "quality.auto_flag_low_quality": {"type": bool, "required": False},
    "retention": {"type": dict, "required": False},
    "privacy": {"type": dict, "required": False},
    "tags": {"type": dict, "required": False},
    "tags.normalize": {"type": bool, "required": False},
}


def validate_config(config: dict) -> list[dict]:
    """验证配置"""
    errors = []
    warnings = []

    for key, schema in CONFIG_SCHEMA.items():
        if key not in config:
            if schema.get("required", False):
                errors.append({"field": key, "level": "error", "message": f"缺少必要字段 '{key}'"})
            continue

        value = config[key]
        expected_type = schema.get("type")

        # 类型检查
        if expected_type and not isinstance(value, expected_type):
            if isinstance(expected_type, tuple):
                if not any(isinstance(value, t) for t in expected_type):
                    errors.append({"field": key, "level": "error",
                                 "message": f"'{key}' 类型错误: 期望 {expected_type}, 实际 {type(value).__name__}"})
            elif isinstance(expected_type, type):
                errors.append({"field": key, "level": "error",
                             "message": f"'{key}' 类型错误: 期望 {expected_type.__name__}, 实际 {type(value).__name__}"})

        # 范围检查
        if "min" in schema and isinstance(value, (int, float)):
            if value < schema["min"]:
                errors.append({"field": key, "level": "error",
                             "message": f"'{key}' 值 {value} 小于最小值 {schema['min']}"})
        if "max" in schema and isinstance(value, (int, float)):
            if value > schema["max"]:
                errors.append({"field": key, "level": "error",
                             "message": f"'{key}' 值 {value} 超过最大值 {schema['max']}"})

        # 模式检查
        if "pattern" in schema and isinstance(value, str):
            if not re.match(schema["pattern"], value):
                errors.append({"field": key, "level": "error",
                             "message": f"'{key}' 格式不匹配: {schema['pattern']}"})

    # 嵌套对象检查
    for key in ["auto_backup", "quality", "retention", "privacy", "tags"]:
        if key in config and isinstance(config[key], dict):
            sub_schema = {k: v for k, v in CONFIG_SCHEMA.items() if k.startswith(f"{key}.")}
            for sub_key, sub_val in sub_schema.items():
                actual_key = sub_key.replace(f"{key}.", "")
                if actual_key in config[key]:
                    sub_value = config[key][actual_key]
                    expected_type = sub_val.get("type")
                    if expected_type and not isinstance(sub_value, expected_type):
                        if isinstance(expected_type, tuple):
                            pass  # 允许 None
                        else:
                            errors.append({"field": f"{key}.{actual_key}", "level": "error",
                                         "message": f"'{key}.{actual_key}' 类型错误"})

    # 版本检查
    version = config.get("version", "0")
    try:
        major = int(version.split(".")[0])
        if major < int(CURRENT_VERSION.split(".")[0]):
            warnings.append({"level": "warning", "message": f"配置版本 {version} 低于当前版本 {CURRENT_VERSION}，建议迁移"})
    except (ValueError, IndexError):
        errors.append({"field": "version", "level": "error", "message": "版本号格式错误"})

    return errors + warnings


def migrate_config(config: dict, target_version: str = CURRENT_VERSION) -> dict:
    """迁移配置到目标版本"""
    source_version = config.get("version", "0")

    if source_version == target_version:
        return config

    # v0/v1 → v5
    config["version"] = target_version

    # 确保必要字段存在
    defaults = {
        "archive_days": 90,
        "max_memory_md_size": 8000,
        "auto_backup": {"enabled": False, "git_remote": None, "interval_hours": 6},
        "quality": {"auto_flag_low_quality": True},
        "retention": {},
        "privacy": {"encrypt_tags": [], "auto_redact_patterns": []},
        "tags": {"normalize": True, "custom_aliases": {}},
    }

    for key, value in defaults.items():
        if key not in config:
            config[key] = value
        elif isinstance(value, dict) and isinstance(config[key], dict):
            for sub_key, sub_value in value.items():
                if sub_key not in config[key]:
                    config[key][sub_key] = sub_value

    return config


def print_validation(results: list[dict]):
    if not results:
        print("✅ 配置验证通过，无问题")
        return

    print("=" * 60)
    print("🔍 配置验证结果")
    print("=" * 60)

    for r in results:
        level = r.get("level", "warning")
        icon = "🔴" if level == "error" else "⚠️"
        field = r.get("field", "")
        msg = r["message"]
        print(f"  {icon} [{level:7s}] {field + ': ' if field else ''}{msg}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="配置验证与迁移")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--config", default=None, help="配置文件路径")
    p.add_argument("--migrate", action="store_true", help="执行迁移")
    p.add_argument("--target-version", default=CURRENT_VERSION)
    args = p.parse_args()

    if args.config:
        config_path = Path(args.config)
    else:
        md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
        md = Path(md)
        # 查找配置文件
        config_path = md / "long-memory.json"
        if not config_path.exists():
            # 在 skill 目录查找
            config_path = Path(__file__).parent.parent / "long-memory.json"

    if not config_path.exists():
        print("⚠️ 未找到配置文件 long-memory.json")
        exit(1)

    config = safe_read_json(config_path)

    if args.migrate:
        migrated = migrate_config(config, args.target_version)
        safe_write_json(config_path, migrated)
        print(f"✅ 配置已迁移到 v{args.target_version}")

    results = validate_config(config if not args.migrate else migrated)
    print_validation(results)
