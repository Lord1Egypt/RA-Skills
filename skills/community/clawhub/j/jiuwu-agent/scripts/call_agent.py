#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
久吾智能体调用脚本
支持文本分析和文件分析两种方式

Token 读取优先级:
1. OpenClaw 环境变量 JIUWU_CORE_TOKEN (env.vars)
2. workspace/.env 文件
3. OpenClaw根目录的 .env 文件
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

# 修复 Windows 控制台 UTF-8 输出乱码
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')


def load_token() -> str:
    """加载认证Token"""
    token = os.environ.get('JIUWU_CORE_TOKEN')
    if token:
        return token

    workspace_env = Path.home() / '.openclaw' / 'workspace' / '.env'
    if workspace_env.exists():
        token = parse_env_file(workspace_env)
        if token:
            return token

    openclaw_env = Path.home() / '.openclaw' / '.env'
    if openclaw_env.exists():
        token = parse_env_file(openclaw_env)
        if token:
            return token

    raise ValueError("未找到 JIUWU_CORE_TOKEN，请配置环境变量或在 .env 文件中设置")


def parse_env_file(env_path: Path) -> str:
    """解析 .env 文件"""
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('JIUWU_CORE_TOKEN='):
                    return line.split('=', 1)[1].strip().strip('"').strip("'")
    except Exception:
        pass
    return None


AUTH_TOKEN = load_token()
BASE_URL = "http://192.168.1.213:5000"
DEFAULT_TIMEOUT = 3600  # 默认超时1小时（文本和文件分析均适用）


def call_text_api(name: str, docno: str, content: str, timeout: int = DEFAULT_TIMEOUT) -> dict:
    """调用文本分析API"""
    encoded_content = urllib.parse.quote(content)
    url = (f"{BASE_URL}/api/AiReview/AgentAnswer"
           f"?name={urllib.parse.quote(name)}"
           f"&docno={urllib.parse.quote(docno)}"
           f"&content={encoded_content}")

    request = urllib.request.Request(url, method='GET')
    request.add_header('accept', 'text/plain')
    request.add_header('Authorization', f'Bearer {AUTH_TOKEN}')

    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode('utf-8'))


def call_file_api(name: str, docno: str, files: list, code: str = "", timeout: int = DEFAULT_TIMEOUT) -> dict:
    """调用文件分析API"""
    import requests

    url = f"{BASE_URL}/api/AiReview/AgentAnswerByFiles"

    files_data = []
    for file_path in files:
        with open(file_path, 'rb') as f:
            file_content = f.read()
        files_data.append(('files', (os.path.basename(file_path), file_content, 'application/octet-stream')))

    data = {
        'code': code,
        'name': name,
        'docno': docno
    }

    headers = {
        'accept': 'text/plain',
        'Authorization': f'Bearer {AUTH_TOKEN}'
    }

    response = requests.post(url, data=data, files=files_data, headers=headers, timeout=timeout)
    return response.json()


def print_result(result: dict):
    """格式化输出结果"""
    if result.get('success'):
        print("[OK] 请求成功")
        print("\n[结果]")
        print("-" * 40)
        print(result['data']['reviewOpinion'])
        print("-" * 40)
        print(f"\n[模型] {result['data'].get('modelId', 'N/A')}")
    else:
        print("[FAIL] 请求失败")
        print(f"\n[错误] {result.get('message', '未知错误')}")


def main():
    parser = argparse.ArgumentParser(description='久吾智能体调用工具')
    subparsers = parser.add_subparsers(dest='command', help='命令类型')

    text_parser = subparsers.add_parser('text', help='文本分析')
    text_parser.add_argument('-n', '--name', required=True, help='智能体名称')
    text_parser.add_argument('-d', '--docno', required=True, help='文档编号')
    text_parser.add_argument('-c', '--content', required=True, help='要分析的文本内容')
    text_parser.add_argument('-t', '--timeout', type=int, default=DEFAULT_TIMEOUT, help='超时时间（秒，默认3600/1小时）')

    file_parser = subparsers.add_parser('file', help='文件分析')
    file_parser.add_argument('-n', '--name', required=True, help='智能体名称')
    file_parser.add_argument('-d', '--docno', required=True, help='文档编号')
    file_parser.add_argument('-f', '--files', nargs='+', required=True, help='要上传的文件列表')
    file_parser.add_argument('--code', default='', help='预留参数（可选）')
    file_parser.add_argument('-t', '--timeout', type=int, default=DEFAULT_TIMEOUT,
                             help=f'超时时间（秒，默认3600/1小时）')

    args = parser.parse_args()

    if args.command == 'text':
        result = call_text_api(args.name, args.docno, args.content, timeout=args.timeout)
        print_result(result)
    elif args.command == 'file':
        result = call_file_api(args.name, args.docno, args.files, args.code, timeout=args.timeout)
        print_result(result)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
