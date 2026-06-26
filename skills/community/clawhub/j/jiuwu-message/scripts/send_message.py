#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
久吾消息网关发送消息脚本
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path

# 修复 Windows 控制台 UTF-8 输出乱码
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')


def load_openclaw_env():
    """加载OpenClaw的.env配置文件"""
    env_paths = [
        Path.home() / ".openclaw" / "workspace" / ".env",
        Path.home() / ".openclaw" / ".env",
    ]

    for env_path in env_paths:
        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ.setdefault(key, value)


def get_gateway_url():
    """获取消息网关服务器地址"""
    load_openclaw_env()
    return os.environ.get("JIUWU_MESSAGE_GATEWAY_URL", "http://192.168.1.213:5000")


def send_message(code: str, text: str, title: str = None, timeout: int = 30) -> dict:
    """
    发送消息到久吾消息网关

    Args:
        code: 接收人工号，多个工号用英文逗号分隔
        text: 消息内容
        title: 消息标题（可选）
        timeout: 超时时间（秒，默认30）

    Returns:
        dict: 包含 success, data, message 字段的响应
    """
    gateway_url = get_gateway_url()
    url = f"{gateway_url}/api/MessageGateway/SendMessagePost"

    payload = {
        "code": code,
        "text": text
    }
    if title:
        payload["title"] = title

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            'accept': 'text/plain',
            'Content-Type': 'application/json-patch+json'
        },
        method='POST'
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.HTTPError as e:
        return {
            "success": False,
            "data": None,
            "message": f"HTTP错误: {e.code} - {e.reason}"
        }
    except urllib.error.URLError as e:
        return {
            "success": False,
            "data": None,
            "message": f"连接失败: {e.reason}"
        }
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "message": f"发生异常: {str(e)}"
        }


def main():
    parser = argparse.ArgumentParser(description="久吾消息网关发送消息")
    parser.add_argument("-c", "--code", required=True, help="接收人工号，多个用英文逗号分隔")
    parser.add_argument("-t", "--text", required=True, help="消息内容")
    parser.add_argument("-tt", "--title", default=None, help="消息标题（可选）")
    parser.add_argument("--timeout", type=int, default=30, help="超时时间（秒，默认30）")

    args = parser.parse_args()

    result = send_message(code=args.code, text=args.text, title=args.title, timeout=args.timeout)

    print(json.dumps(result, ensure_ascii=False, indent=2))

    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
