#!/usr/bin/env python
"""
Panda Data Skill - 命令行调用 tool。

Agent 可通过 exec 调用此脚本，传入 tool 名称和参数。
用法: python scripts/call_tool.py <tool_name> <key>=<value> ...
"""
import json
import sys
from pathlib import Path

# 确保能导入 panda_tools（需已安装 panda-data-tools）
try:
    from panda_tools.credential import CredentialManager
    from panda_tools.registry import ToolRegistry
except ImportError as e:
    print(json.dumps({"error": f"panda_tools 未安装: {e}"}, ensure_ascii=False))
    sys.exit(1)


def parse_args(args: list[str]) -> dict:
    """解析 key=value 形式的参数为字典。"""
    kwargs = {}
    for arg in args:
        if "=" in arg:
            k, v = arg.split("=", 1)
            # 尝试转换为数字
            try:
                v = int(v)
            except ValueError:
                try:
                    v = float(v)
                except ValueError:
                    pass
            kwargs[k.strip()] = v
    return kwargs


def main() -> None:
    if len(sys.argv) < 2:
        print(json.dumps({"error": "用法: python call_tool.py <tool_name> [key=value ...]"}, ensure_ascii=False))
        sys.exit(1)

    tool_name = sys.argv[1]
    kwargs = parse_args(sys.argv[2:])

    CredentialManager.init_from_env()
    registry = ToolRegistry()

    if tool_name not in registry.get_tool_names():
        print(json.dumps({"error": f"未知的 tool: {tool_name}"}, ensure_ascii=False))
        sys.exit(1)

    try:
        result = registry.call_tool(tool_name, **kwargs)
        print(result)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
