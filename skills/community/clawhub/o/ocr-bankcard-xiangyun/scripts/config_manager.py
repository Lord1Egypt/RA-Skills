#!/usr/bin/env python3
"""
config_manager.py
翔云银行卡 OCR Skill — 配置管理工具

用法:
  python config_manager.py load               # 读取并打印当前配置（JSON 格式输出）
  python config_manager.py save --key K --secret S  # 保存 key/secret 到 config.json
  python config_manager.py reset              # 清空配置（需二次确认）

配置文件默认保存在脚本同级目录的 ../config.json（即 skill 根目录）。
"""

import argparse
import json
import os
import sys

# 配置文件固定路径：skill 根目录下的 config.json
SKILL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PATH = os.path.join(SKILL_ROOT, "config.json")


def load_config() -> dict:
    """读取配置文件，返回 dict；文件不存在或解析失败返回空 dict。"""
    if not os.path.exists(CONFIG_PATH):
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, IOError):
        return {}


def save_config(key: str, secret: str) -> None:
    """将 key 和 secret 持久化写入 config.json。"""
    data = load_config()
    data["key"] = key.strip()
    data["secret"] = secret.strip()
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] 配置已保存至: {CONFIG_PATH}")


def reset_config() -> None:
    """清空 key 和 secret（保留文件其他字段）。"""
    data = load_config()
    data["key"] = ""
    data["secret"] = ""
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] 配置已重置: {CONFIG_PATH}")


def is_configured(cfg: dict) -> bool:
    """判断配置是否有效（key 和 secret 均非空）。"""
    return bool(cfg.get("key", "").strip()) and bool(cfg.get("secret", "").strip())


def main():
    parser = argparse.ArgumentParser(description="翔云 OCR Skill 配置管理器")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # load 命令
    subparsers.add_parser("load", help="读取并输出当前配置")

    # save 命令
    save_parser = subparsers.add_parser("save", help="保存 key/secret 到配置文件")
    save_parser.add_argument("--key", required=True, help="翔云 ocrKey")
    save_parser.add_argument("--secret", required=True, help="翔云 ocrSecret")

    # reset 命令
    subparsers.add_parser("reset", help="清空 key/secret 配置")

    args = parser.parse_args()

    if args.command == "load":
        cfg = load_config()
        configured = is_configured(cfg)
        output = {
            "configured": configured,
            "key": cfg.get("key", ""),
            "secret": cfg.get("secret", ""),
            "config_path": CONFIG_PATH,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
        # 退出码：0=已配置，1=未配置
        sys.exit(0 if configured else 1)

    elif args.command == "save":
        if not args.key.strip() or not args.secret.strip():
            print("[ERROR] key 和 secret 均不能为空", file=sys.stderr)
            sys.exit(2)
        save_config(args.key, args.secret)

    elif args.command == "reset":
        reset_config()


if __name__ == "__main__":
    main()
