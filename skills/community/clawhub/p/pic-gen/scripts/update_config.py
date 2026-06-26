#!/usr/bin/env python3
"""
pic-gen: 配置管理脚本
支持更新 API Key、切换默认模型、查看当前配置
"""

import argparse
import os
import shutil
import sys
import yaml

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.path.join(SKILL_DIR, "config", "models.yaml")
CONFIG_TEMPLATE = os.path.join(SKILL_DIR, "config", "models.yaml.template")

import shutil  # for init_config template copy


def load_config() -> dict:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}


def save_config(config: dict):
    """原子写入配置文件（先写临时文件再 rename）"""
    tmp_path = CONFIG_PATH + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        yaml.dump(config, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
    os.replace(tmp_path, CONFIG_PATH)


def init_config():
    """初始化配置文件（从模板复制）"""
    if not os.path.exists(CONFIG_PATH):
        if os.path.exists(CONFIG_TEMPLATE):
            shutil.copy2(CONFIG_TEMPLATE, CONFIG_PATH)
            print(f"✅ 配置文件已创建: {CONFIG_PATH}")
        else:
            # 模板不存在时回退到内嵌方式
            config = {
                "default": "qwen",
                "models": {
                    "qwen": {"enabled": True, "api_key": "", "model": "qwen-image-2.0-pro",
                              "default_size": "1024*1024", "default_style": "auto"},
                    "banana": {"enabled": False, "api_key": "", "model": "flux-dev", "default_size": "1024*1024"},
                    "dalle": {"enabled": False, "api_key": "", "model": "dall-e-3", "default_size": "1024x1024"},
                }
            }
            save_config(config)
            print(f"✅ 配置文件已创建: {CONFIG_PATH}")
    else:
        print(f"配置文件已存在: {CONFIG_PATH}")


def update_api_key(model: str, key: str) -> dict:
    """更新指定模型的 API Key"""
    config = load_config()

    if model not in config.get("models", {}):
        return {"error": f"未知模型: {model}，支持的模型: qwen, banana, dalle"}

    config["models"][model]["api_key"] = key
    config["models"][model]["enabled"] = True
    save_config(config)

    return {"success": True, "model": model, "message": f"{model} API Key 已更新，模型已启用"}


def set_default_model(model: str) -> dict:
    """设置默认模型"""
    config = load_config()

    if model not in config.get("models", {}):
        return {"error": f"未知模型: {model}"}

    config["default"] = model
    save_config(config)

    return {"success": True, "default": model, "message": f"默认模型已设置为 {model}"}


def enable_model(model: str, enabled: bool = True) -> dict:
    """启用/禁用指定模型"""
    config = load_config()

    if model not in config.get("models", {}):
        return {"error": f"未知模型: {model}"}

    config["models"][model]["enabled"] = enabled
    save_config(config)

    status = "已启用" if enabled else "已禁用"
    return {"success": True, "model": model, "message": f"{model} {status}"}


def show_config() -> dict:
    """展示当前配置（隐藏 API Key 主体）"""
    config = load_config()
    display = {
        "default": config.get("default", "qwen"),
        "models": {}
    }

    for name, model_config in config.get("models", {}).items():
        display_config = dict(model_config)
        api_key = display_config.get("api_key", "")
        if api_key:
            # 隐藏 Key 中间部分，只显示前4和后4位
            if len(api_key) > 8:
                display_config["api_key"] = f"{api_key[:4]}...{api_key[-4:]}"
            else:
                display_config["api_key"] = "******"
        else:
            display_config["api_key"] = "（未设置）"
        display_config["enabled"] = display_config.get("enabled", False)
        display["models"][name] = display_config

    return display


def main():
    parser = argparse.ArgumentParser(description="pic-gen 配置管理")
    sub = parser.add_subparsers(dest="command")

    # init
    sub.add_parser("init", help="初始化配置文件")

    # set-key
    setkey = sub.add_parser("set-key", help="设置 API Key")
    setkey.add_argument("model", choices=["qwen", "banana", "dalle"], help="模型名")
    setkey.add_argument("key", help="API Key")

    # set-default
    setdef = sub.add_parser("set-default", help="设置默认模型")
    setdef.add_argument("model", choices=["qwen", "banana", "dalle"], help="模型名")

    # enable/disable
    enable = sub.add_parser("enable", help="启用模型")
    enable.add_argument("model", choices=["qwen", "banana", "dalle"])
    disable = sub.add_parser("disable", help="禁用模型")
    disable.add_argument("model", choices=["qwen", "banana", "dalle"])

    # show
    sub.add_parser("show", help="显示当前配置")

    args = parser.parse_args()

    if args.command == "init":
        init_config()

    elif args.command == "set-key":
        result = update_api_key(args.model, args.key)
        if "error" in result:
            print(f"❌ {result['error']}", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"✅ {result['message']}")

    elif args.command == "set-default":
        result = set_default_model(args.model)
        if "error" in result:
            print(f"❌ {result['error']}", file=sys.stderr)
            sys.exit(1)
        else:
            print(f"✅ {result['message']}")

    elif args.command == "enable":
        result = enable_model(args.model, True)
        print(f"✅ {result['message']}")

    elif args.command == "disable":
        result = enable_model(args.model, False)
        print(f"✅ {result['message']}")

    elif args.command == "show":
        result = show_config()
        print(yaml.dump(result, allow_unicode=True, default_flow_style=False))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
