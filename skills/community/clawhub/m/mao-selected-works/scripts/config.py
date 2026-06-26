#!/usr/bin/env python3

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG_PATH = ROOT / "config" / "search.json"


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_json(path: Path, data: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def get_nested(data: dict[str, Any], path: str) -> Any:
    keys = path.split(".")
    value = data
    for key in keys:
        if isinstance(value, dict):
            value = value.get(key)
        else:
            return None
    return value


def set_nested(data: dict[str, Any], path: str, value: Any) -> dict[str, Any]:
    keys = path.split(".")
    current = data
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value
    return data


def command_show(args: argparse.Namespace) -> int:
    config = load_json(DEFAULT_CONFIG_PATH)
    print(f"配置文件: {DEFAULT_CONFIG_PATH}")
    print()
    api_key_env = config.get("rag", {}).get("api", {}).get("api_key_env", "")
    if api_key_env:
        print(f"api_key_env: {api_key_env}")
    else:
        print("api_key_env: (未设置，建议使用环境变量 MAO_SKILL_API_KEY)")
    print(f"base_url: {config.get('rag', {}).get('api', {}).get('base_url', '')}")
    print(f"embedding.model: {config.get('rag', {}).get('embedding', {}).get('model', '')}")
    print(f"rerank.model: {config.get('rag', {}).get('rerank', {}).get('model', '')}")
    print(f"chunk_size: {config.get('chunk_size', 1024)}")
    print(f"chunk_overlap: {config.get('chunk_overlap', 100)}")
    return 0


def command_set(args: argparse.Namespace) -> int:
    if not DEFAULT_CONFIG_PATH.exists():
        print(f"错误: 配置文件不存在: {DEFAULT_CONFIG_PATH}", file=sys.stderr)
        return 1

    config = load_json(DEFAULT_CONFIG_PATH)
    key = args.key.lower()
    value: Any = args.value

    if key in ("rag.enabled", "rag.rerank.enabled", "rag.build_embeddings_on_index"):
        value = value.lower() in ("true", "1", "yes", "on")
    elif key == "chunk_size":
        value = int(value)
    elif key == "chunk_overlap":
        value = int(value)
    elif key == "rag.api.base_url":
        value = str(value).rstrip("/")
    else:
        value = str(value)

    config = set_nested(config, key, value)
    save_json(DEFAULT_CONFIG_PATH, config)
    print(f"已更新: {key} = {value}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="mao-selected-works 配置管理")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("show", help="显示当前配置")

    set_parser = subparsers.add_parser("set", help="更新配置")
    set_parser.add_argument("key", help="配置项路径，如 rag.embedding.model")
    set_parser.add_argument("value", help="新的值")

    args = parser.parse_args()

    if args.command == "show":
        return command_show(args)
    elif args.command == "set":
        return command_set(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
