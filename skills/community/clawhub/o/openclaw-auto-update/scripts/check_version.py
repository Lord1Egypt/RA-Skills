#!/usr/bin/env python3
"""
OpenClaw 版本检查工具
用于比较当前版本与最新稳定版本
"""

import subprocess
import json
import re

def get_current_version():
    """获取当前 OpenClaw 版本"""
    try:
        result = subprocess.run(
            ["openclaw", "--version"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def parse_version(version_str):
    """解析版本号"""
    # 支持格式：v2026.3.7, 2026.3.7, v2026.3.2 等
    match = re.search(r'v?(\d{4})\.(\d+)\.(\d+)', version_str)
    if match:
        return {
            'year': int(match.group(1)),
            'month': int(match.group(2)),
            'patch': int(match.group(3)),
            'full': version_str
        }
    return None

def version_diff(v1, v2):
    """计算版本差距"""
    if not v1 or not v2:
        return 0
    # 简单计算 patch 版本差距
    return v2['patch'] - v1['patch']

def main():
    current = get_current_version()
    current_parsed = parse_version(current)
    
    print(f"当前版本：{current}")
    if current_parsed:
        print(f"解析结果：年={current_parsed['year']}, 月={current_parsed['month']}, 补丁={current_parsed['patch']}")
    else:
        print("⚠️ 无法解析版本号")
    
    print("\n请使用 agent-reach 访问 https://github.com/openclaw/openclaw/releases 获取最新版本")

if __name__ == "__main__":
    main()
