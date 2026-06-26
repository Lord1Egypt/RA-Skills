#!/usr/bin/env python3
"""图生图 - 使用 DALL-E 3 生成图片"""

import os
import sys
import json
import argparse

def generate_image(prompt: str, api_key: str = None) -> str:
    """调用 DALL-E 3 API 生成图片"""
    import openai
    
    if not api_key:
        api_key = os.environ.get("API_KEY")
    
    if not api_key:
        print("错误: 未设置 API_KEY 环境变量", file=sys.stderr)
        sys.exit(1)
    
    client = openai.OpenAI(api_key=api_key)
    
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    
    return response.data[0].url


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DALL-E 图生图")
    parser.add_argument("prompt", help="图片描述")
    parser.add_argument("--api-key", help="OpenAI API Key")
    
    args = parser.parse_args()
    
    try:
        url = generate_image(args.prompt, args.api_key)
        print(url)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
