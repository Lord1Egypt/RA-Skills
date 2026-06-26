#!/usr/bin/env python3
"""
输出工具模块
"""

import json
from typing import Dict, Any


def print_result(result: Dict[str, Any]):
    """打印结果摘要"""
    print("\n" + "=" * 50)
    print("项目初始化完成！")
    print("=" * 50)

    print(f"\n项目名称: {result.get('name', 'unknown')}")
    print(f"项目类型: {result.get('type', 'unknown')}")
    print(f"主要语言: {result.get('language', 'unknown')}")
    print(f"框架: {result.get('framework', 'unknown')}")
    print(f"构建系统: {result.get('build_system', 'unknown')}")

    if result.get('target_platform'):
        print(f"目标平台: {result.get('target_platform')}")

    print(f"\n已生成项目文档: .claude/project.md")
    print("=" * 50)


def format_json(data: Dict[str, Any]) -> str:
    """格式化JSON输出"""
    return json.dumps(data, indent=2, ensure_ascii=False)