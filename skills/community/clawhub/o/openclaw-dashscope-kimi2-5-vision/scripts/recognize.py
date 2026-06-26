#!/usr/bin/env python3
"""
Kimi K2.5 图片识别 - 为阿里百炼 GLM 用户设计
自动从 OpenClaw 配置读取 API Key
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error

API_URL = "https://coding.dashscope.aliyuncs.com/v1/chat/completions"
MODEL = "kimi-k2.5"
DEFAULT_PROMPT = "请详细描述这张图片的内容，包括所有文字、界面元素和重要细节。"

# 缓存文件路径
CACHE_FILE = os.path.expanduser("~/.openclaw/.kimi_vision_key_cached")


def find_api_key_in_config():
    """从 OpenClaw 配置文件中查找 API Key"""
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    if not os.path.exists(config_path):
        return None

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
    except (json.JSONDecodeError, IOError):
        return None

    # 按优先级查找
    search_paths = [
        ("env.DASHSCOPE_API_KEY", ["env", "DASHSCOPE_API_KEY"]),
        ("models.providers.qwencode.apiKey", ["models", "providers", "qwencode", "apiKey"]),
        ("models.providers.dashscope.apiKey", ["models", "providers", "dashscope", "apiKey"]),
    ]

    for path_name, path_parts in search_paths:
        value = config
        try:
            for part in path_parts:
                value = value[part]
            if isinstance(value, str) and value.startswith("sk-"):
                return value, path_name
        except (KeyError, TypeError):
            continue

    return None


def get_api_key():
    """获取 API Key，自动检测多个来源"""
    # 1. 检查环境变量
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if api_key:
        return api_key, "环境变量 DASHSCOPE_API_KEY"

    # 2. 检查缓存文件
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                cached = f.read().strip()
                if cached.startswith("sk-"):
                    os.environ["DASHSCOPE_API_KEY"] = cached
                    return cached, "缓存文件"
        except IOError:
            pass

    # 3. 从 OpenClaw 配置中查找
    result = find_api_key_in_config()
    if result:
        api_key, source = result
        os.environ["DASHSCOPE_API_KEY"] = api_key

        # 第一次找到，提示用户持久化
        env_file = os.path.expanduser("~/.openclaw/.env")
        if not os.path.exists(env_file) or "DASHSCOPE_API_KEY" not in open(env_file).read():
            print(f"✓ 从 OpenClaw 配置 ({source}) 找到 API Key", file=sys.stderr)
            print("", file=sys.stderr)
            print("💡 建议持久化到环境变量，重启后也能直接使用：", file=sys.stderr)
            print(f"   echo 'DASHSCOPE_API_KEY={api_key}' >> ~/.openclaw/.env", file=sys.stderr)
            print("", file=sys.stderr)

        return api_key, source

    # 4. 都没找到，报错
    print("❌ 未找到 DASHSCOPE_API_KEY", file=sys.stderr)
    print("", file=sys.stderr)
    print("已检查：", file=sys.stderr)
    print("  - 环境变量 DASHSCOPE_API_KEY", file=sys.stderr)
    print("  - OpenClaw 配置 env.DASHSCOPE_API_KEY", file=sys.stderr)
    print("  - OpenClaw 配置 models.providers.qwencode.apiKey", file=sys.stderr)
    print("", file=sys.stderr)
    print("请到阿里百炼控制台生成 API Key：", file=sys.stderr)
    print("  1. 打开 https://bailian.console.aliyun.com/", file=sys.stderr)
    print("  2. 登录阿里云账号", file=sys.stderr)
    print("  3. 进入「API-KEY 管理」创建 Key", file=sys.stderr)
    print("", file=sys.stderr)
    print("然后设置：", file=sys.stderr)
    print("  echo 'DASHSCOPE_API_KEY=sk-sp-你的key' >> ~/.openclaw/.env", file=sys.stderr)
    sys.exit(1)


def image_to_base64(image_path):
    """Convert image file to base64 string."""
    if not os.path.exists(image_path):
        print(f"错误：图片文件不存在: {image_path}", file=sys.stderr)
        sys.exit(1)

    with open(image_path, "rb") as f:
        data = f.read()

    ext = os.path.splitext(image_path)[1].lower()
    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    mime_type = mime_types.get(ext, "image/jpeg")
    b64_data = base64.b64encode(data).decode("utf-8")
    return f"data:{mime_type};base64,{b64_data}"


def recognize_image(image_path, prompt, api_key):
    """调用 DashScope API 识别图片"""
    image_url = image_to_base64(image_path)

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_url}},
                    {"type": "text", "text": prompt},
                ],
            }
        ],
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"API 错误 ({e.code}): {error_body}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Kimi K2.5 图片识别（自动读取 OpenClaw 配置）"
    )
    parser.add_argument("image", help="图片文件路径")
    parser.add_argument(
        "--prompt", "-p",
        default=DEFAULT_PROMPT,
        help="分析提示（默认：详细描述图片内容）"
    )

    args = parser.parse_args()

    api_key, source = get_api_key()
    result = recognize_image(args.image, args.prompt, api_key)
    print(result)


if __name__ == "__main__":
    main()