#!/usr/bin/env python3
"""
通用配置管理器
支持跨会话、跨平台的个性化配置存储
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime

# 配置文件名
CONFIG_FILE = "config.json"

# 默认配置结构
DEFAULT_CONFIG = {
    "version": "1.0",
    "workdir": None,
    "project_name": None,
    "build_command": None,
    "run_command": None,
    "test_command": None,
    "preferences": {},
    "custom": {},
    "created_at": None,
    "updated_at": None
}

# 预定义配置项说明
CONFIG_SCHEMA = {
    "workdir": {
        "type": "string",
        "description": "工作目录路径",
        "command": "/set-workdir"
    },
    "project_name": {
        "type": "string",
        "description": "项目名称",
        "auto": True  # 自动从 workdir 提取
    },
    "build_command": {
        "type": "string",
        "description": "构建命令",
        "example": "npm run build"
    },
    "run_command": {
        "type": "string",
        "description": "运行命令",
        "example": "npm run dev"
    },
    "test_command": {
        "type": "string",
        "description": "测试命令",
        "example": "npm test"
    },
    "preferences": {
        "type": "object",
        "description": "偏好设置",
        "fields": {
            "language": "语言偏好 (zh/en)",
            "detail_level": "详细程度 (brief/normal/detailed)",
            "auto_update": "自动更新文档 (true/false)"
        }
    },
    "custom": {
        "type": "object",
        "description": "自定义配置（任意键值对）"
    }
}


def get_config_path(base_dir: str) -> str:
    """获取配置文件路径"""
    return os.path.join(base_dir, CONFIG_FILE)


def load_config(base_dir: str) -> Dict[str, Any]:
    """加载配置文件"""
    config_path = get_config_path(base_dir)

    if not os.path.exists(config_path):
        return DEFAULT_CONFIG.copy()

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            result = DEFAULT_CONFIG.copy()
            result.update(config)
            return result
    except (json.JSONDecodeError, IOError) as e:
        print(f"[警告] 配置文件读取失败: {e}", file=sys.stderr)
        return DEFAULT_CONFIG.copy()


def save_config(base_dir: str, config: Dict[str, Any]) -> bool:
    """保存配置文件"""
    config_path = get_config_path(base_dir)

    try:
        config["updated_at"] = datetime.now().isoformat()
        if not config.get("created_at"):
            config["created_at"] = config["updated_at"]

        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"[错误] 配置文件保存失败: {e}", file=sys.stderr)
        return False


def get_value(base_dir: str, key: str) -> Dict[str, Any]:
    """获取单个配置项"""
    config = load_config(base_dir)

    # 支持嵌套键，如 preferences.language
    keys = key.split('.')
    value = config
    for k in keys:
        if isinstance(value, dict) and k in value:
            value = value[k]
        else:
            return {"success": False, "key": key, "error": f"配置项不存在: {key}"}

    return {"success": True, "key": key, "value": value}


def set_value(base_dir: str, key: str, value: Any) -> Dict[str, Any]:
    """设置单个配置项"""
    config = load_config(base_dir)

    # 支持嵌套键，如 preferences.language
    keys = key.split('.')
    target = config

    for k in keys[:-1]:
        if k not in target:
            target[k] = {}
        target = target[k]

    target[keys[-1]] = value

    # 特殊处理：设置 workdir 时自动提取 project_name
    if key == "workdir" and isinstance(value, str) and os.path.isdir(value):
        config["project_name"] = os.path.basename(value)

    if save_config(base_dir, config):
        return {"success": True, "key": key, "value": value}
    return {"success": False, "error": "保存失败"}


def delete_value(base_dir: str, key: str) -> Dict[str, Any]:
    """删除配置项"""
    config = load_config(base_dir)

    keys = key.split('.')
    target = config

    for k in keys[:-1]:
        if k not in target:
            return {"success": True, "key": key, "message": "配置项不存在"}
        target = target[k]

    if keys[-1] in target:
        del target[keys[-1]]
        save_config(base_dir, config)
        return {"success": True, "key": key, "message": "已删除"}
    return {"success": True, "key": key, "message": "配置项不存在"}


def show_all(base_dir: str) -> Dict[str, Any]:
    """显示所有配置"""
    config = load_config(base_dir)
    result = {"config": {}}

    for key in ["workdir", "project_name", "build_command", "run_command", "test_command"]:
        result["config"][key] = config.get(key)

    if config.get("preferences"):
        result["config"]["preferences"] = config["preferences"]

    if config.get("custom"):
        result["config"]["custom"] = config["custom"]

    result["created_at"] = config.get("created_at")
    result["updated_at"] = config.get("updated_at")

    return result


def show_schema() -> Dict[str, Any]:
    """显示配置项说明"""
    return {"schema": CONFIG_SCHEMA}


# ============ 便捷方法（兼容旧接口） ============

def get_workdir(base_dir: str) -> Optional[str]:
    """获取工作目录"""
    result = get_value(base_dir, "workdir")
    if result.get("success") and result.get("value"):
        workdir = result["value"]
        if os.path.isdir(workdir):
            return workdir
    return None


def set_workdir(base_dir: str, workdir: str) -> Dict[str, Any]:
    """设置工作目录"""
    workdir = os.path.abspath(workdir)

    if not os.path.isdir(workdir):
        return {"success": False, "error": f"目录不存在: {workdir}"}

    return set_value(base_dir, "workdir", workdir)


# ============ 命令行入口 ============

def print_help():
    """打印帮助信息"""
    help_text = """
配置管理器 - 支持跨会话个性化配置

用法: config_manager.py <baseDir> <command> [args]

命令:
  get <key>              获取配置项 (支持嵌套键，如 preferences.language)
  set <key> <value>      设置配置项
  delete <key>           删除配置项
  show                   显示所有配置
  schema                 显示配置项说明

  # 便捷命令（兼容旧接口）
  get-workdir            获取工作目录
  set-workdir <path>     设置工作目录

预定义配置项:
  workdir          工作目录路径
  project_name     项目名称（自动提取）
  build_command    构建命令
  run_command      运行命令
  test_command     测试命令
  preferences      偏好设置 (对象)
  custom           自定义配置 (对象)

示例:
  # 设置工作目录
  config_manager.py /path/to/skill set workdir /home/user/project

  # 设置构建命令
  config_manager.py /path/to/skill set build_command "npm run build"

  # 设置偏好
  config_manager.py /path/to/skill set preferences.language zh
  config_manager.py /path/to/skill set preferences.detail_level detailed

  # 设置自定义配置
  config_manager.py /path/to/skill set custom.api_key "xxx"
  config_manager.py /path/to/skill set custom.timeout 30
"""
    print(help_text)


def main():
    if len(sys.argv) < 3:
        print_help()
        sys.exit(1)

    base_dir = sys.argv[1]
    command = sys.argv[2]

    if command == "get":
        if len(sys.argv) < 4:
            print("用法: config_manager.py <baseDir> get <key>")
            sys.exit(1)
        result = get_value(base_dir, sys.argv[3])
        print(json.dumps(result, ensure_ascii=False))

    elif command == "set":
        if len(sys.argv) < 5:
            print("用法: config_manager.py <baseDir> set <key> <value>")
            sys.exit(1)
        key = sys.argv[3]
        value = sys.argv[4]
        # 尝试解析 JSON 值
        try:
            value = json.loads(value)
        except:
            pass
        result = set_value(base_dir, key, value)
        print(json.dumps(result, ensure_ascii=False))

    elif command == "delete":
        if len(sys.argv) < 4:
            print("用法: config_manager.py <baseDir> delete <key>")
            sys.exit(1)
        result = delete_value(base_dir, sys.argv[3])
        print(json.dumps(result, ensure_ascii=False))

    elif command == "show":
        result = show_all(base_dir)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "schema":
        result = show_schema()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    # 兼容旧接口
    elif command == "get-workdir":
        workdir = get_workdir(base_dir)
        if workdir:
            print(json.dumps({"success": True, "workdir": workdir}))
        else:
            print(json.dumps({"success": False, "workdir": None, "error": "工作目录未设置"}))

    elif command == "set-workdir":
        if len(sys.argv) < 4:
            print("用法: config_manager.py <baseDir> set-workdir <path>")
            sys.exit(1)
        result = set_workdir(base_dir, sys.argv[3])
        print(json.dumps(result, ensure_ascii=False))

    elif command == "clear-workdir":
        result = delete_value(base_dir, "workdir")
        print(json.dumps(result, ensure_ascii=False))

    elif command == "help" or command == "--help" or command == "-h":
        print_help()

    else:
        print(f"未知命令: {command}")
        print("运行 'config_manager.py help' 查看帮助")
        sys.exit(1)


if __name__ == "__main__":
    main()