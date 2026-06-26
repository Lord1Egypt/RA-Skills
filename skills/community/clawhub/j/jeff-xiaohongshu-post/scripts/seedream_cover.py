#!/usr/bin/env python3
"""
小红书封面图生成 - Seedream 5.0 API
用法: python3 seedream_cover.py --title "标题" --subtitle "副标题" --output /path/to/output.png
"""

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.request
import urllib.error
import os
import json


# 从凭据文件读取 API Key（安全存储）
CREDENTIALS_FILE = "/root/.openclaw/credentials/seedream.json"

def _load_credentials() -> dict:
    """加载凭据文件。"""
    try:
        with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ 凭据文件未找到: {CREDENTIALS_FILE}")
        print("   请创建该文件并填入 seedream API 配置")
        sys.exit(2)
    except json.JSONDecodeError:
        print(f"❌ 凭据文件 JSON 格式错误: {CREDENTIALS_FILE}")
        sys.exit(2)


_CREDENTIALS = _load_credentials()


API_URL = _CREDENTIALS.get("endpoint", "https://ark.cn-beijing.volces.com/api/v3/images/generations")
API_KEY = _CREDENTIALS.get("api_key", "")
MODEL = _CREDENTIALS.get("model", "doubao-seedream-5-0-260128")

if not API_KEY:
    print("❌ seedream.json 中缺少 api_key")
    sys.exit(2)


def buildPrompt(title: str, subtitle: str) -> str:
    """构造 Seedream prompt

    ⚠️ 严格规则：
    - 封面图的文字 = 用户确认的标题，一字不差
    - prompt 中禁止自行添加副标题、金句或额外描述性文字
    - 只在标题后附加基础风格标签
    """
    if subtitle and subtitle.strip():
        prompt = f"小红红书封面图，{title}，{subtitle}，扁平矢量风格，简约几何装饰，暖色调，3:4竖版构图"
    else:
        # 标题严格等于用户确认的标题，不扩展
        prompt = f"小红书封面图，{title}，扁平矢量风格，简约几何装饰，暖色调，3:4竖版构图"
    return prompt


def generateImage(prompt: str, output_path: str) -> bool:
    """调用 Seedream 5.0 API 生成图片"""

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "sequential_image_generation": "disabled",
        "response_format": "url",
        "size": "1920x2560",   # 3:4 竖版
        "stream": False,
        "watermark": False,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}",
    }

    print(f"🎨 正在生成封面图...")
    print(f"   Prompt: {prompt[:80]}...")

    req = urllib.request.Request(
        API_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"❌ API HTTP 错误 {e.code}: {error_body[:500]}")
        return False
    except Exception as e:
        print(f"❌ 请求失败: {e}")
        return False

    if "data" not in result or not result["data"]:
        print(f"❌ 返回无 data 字段: {result}")
        return False

    image_url = result["data"][0].get("url")
    if not image_url:
        print(f"❌ 未获取到图片 URL: {result}")
        return False

    print(f"✅ 图片生成成功，正在下载...")

    # 下载图片
    try:
        urllib.request.urlretrieve(image_url, output_path)
        size_kb = os.path.getsize(output_path) / 1024
        print(f"✅ 下载完成: {output_path} ({size_kb:.1f} KB)")
        return True
    except Exception as e:
        print(f"❌ 下载失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="小红书封面图 - Seedream 5.0")
    parser.add_argument("--title", required=True, help="封面标题")
    parser.add_argument("--subtitle", default="", help="封面副标题/金句")
    parser.add_argument("--output", required=True, help="输出图片路径（.png）")
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    prompt = buildPrompt(args.title, args.subtitle)
    success = generateImage(prompt, args.output)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
