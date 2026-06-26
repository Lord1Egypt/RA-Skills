#!/usr/bin/env python3
"""
gpt-image-2 skill 核心脚本
调用生图 API，将结果保存为本地 PNG 文件。

用法:
  python3 generate_image.py --key <ACCESS_KEY> --prompt <提示词> [--output <路径>] [--quality low|medium|high] [--n 1-4]

示例:
  python3 generate_image.py --key IMGKEY-HK-XXXXXX --prompt "一只可爱的猫咪" --output /tmp/cat.png
"""

import argparse
import base64
import json
import sys
import os
import tempfile
import requests

SERVER = "http://124.156.166.147:8765"

def default_output_path():
    """返回跨平台兼容的默认输出路径（使用系统临时目录）"""
    return os.path.join(tempfile.gettempdir(), "generated.png")

def generate(key: str, prompt: str, output: str, quality: str = "low", n: int = 1):
    headers = {"x-access-key": key, "Content-Type": "application/json"}
    payload = {"prompt": prompt, "size": "1024x1024", "quality": quality, "n": n}

    try:
        r = requests.post(f"{SERVER}/generate", headers=headers, json=payload, timeout=200)
    except Exception as e:
        print(f"[ERROR] 连接服务器失败: {e}", file=sys.stderr)
        sys.exit(1)

    if r.status_code == 401:
        print("[ERROR] 密钥无效，请检查你的访问密钥。", file=sys.stderr)
        sys.exit(1)
    elif r.status_code == 403:
        detail = r.json().get("detail", "")
        print(f"[ERROR] 配额不足: {detail}", file=sys.stderr)
        sys.exit(1)
    elif r.status_code != 200:
        print(f"[ERROR] 服务器错误 ({r.status_code}): {r.text[:200]}", file=sys.stderr)
        sys.exit(1)

    data = r.json()
    images = data.get("images", [])
    remaining = data.get("quota_remaining", "?")
    usage = data.get("usage", {})

    saved_paths = []
    for i, b64 in enumerate(images):
        if n == 1:
            path = output
        else:
            base, ext = os.path.splitext(output)
            path = f"{base}_{i+1}{ext}"
        img_bytes = base64.b64decode(b64)
        with open(path, "wb") as f:
            f.write(img_bytes)
        saved_paths.append(path)
        print(f"[OK] 图片已保存: {path} ({len(img_bytes)//1024} KB)")

    print(f"[INFO] 剩余配额: {remaining} 张")
    print(f"[INFO] Token 消耗: 输入={usage.get('input_tokens',0)} 输出={usage.get('output_tokens',0)} 总计={usage.get('total_tokens',0)}")
    return saved_paths

def query_quota(key: str):
    headers = {"x-access-key": key}
    try:
        r = requests.get(f"{SERVER}/quota", headers=headers, timeout=10)
    except Exception as e:
        print(f"[ERROR] 连接服务器失败: {e}", file=sys.stderr)
        sys.exit(1)
    if r.status_code == 401:
        print("[ERROR] 密钥无效。", file=sys.stderr)
        sys.exit(1)
    d = r.json()
    print(f"配额总量: {d['quota']} 张 | 已使用: {d['used']} 张 | 剩余: {d['remaining']} 张")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="gpt-image-2 生图工具")
    parser.add_argument("--key",     required=True, help="访问密钥")
    parser.add_argument("--prompt",  default="",    help="图片描述提示词")
    parser.add_argument("--output",  default=default_output_path(), help="输出图片路径（默认使用系统临时目录）")
    parser.add_argument("--quality", default="low", choices=["low","medium","high"])
    parser.add_argument("--n",       default=1, type=int, help="生成数量(1-4)")
    parser.add_argument("--quota",   action="store_true", help="仅查询剩余配额")
    args = parser.parse_args()

    if args.quota:
        query_quota(args.key)
    else:
        if not args.prompt:
            print("[ERROR] 请提供 --prompt 参数", file=sys.stderr)
            sys.exit(1)
        generate(args.key, args.prompt, args.output, args.quality, args.n)
