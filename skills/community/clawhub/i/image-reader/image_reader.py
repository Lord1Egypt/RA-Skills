#!/usr/bin/env python3
"""
图片识别与理解工具
调用豆包多模态模型分析图片内容
"""

import os
import sys
import base64
import yaml
import argparse
from pathlib import Path
from typing import Optional

try:
    from openai import OpenAI
except ImportError:
    print("错误：需要安装 openai 库")
    print("请运行: pip install openai")
    sys.exit(1)


def load_config() -> dict:
    """加载配置文件"""
    config_path = Path(__file__).parent / "config.yaml"
    
    if not config_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_path}")
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def encode_image(image_path: str) -> str:
    """将图片编码为 base64"""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def analyze_image(
    image_path: str,
    api_base: str,
    api_key: str,
    model: str,
    system_prompt: str,
    user_prompt: Optional[str] = None
) -> str:
    """调用多模态模型分析图片"""
    
    # 初始化 OpenAI 客户端
    client = OpenAI(
        api_key=api_key,
        base_url=api_base
    )
    
    # 编码图片
    base64_image = encode_image(image_path)
    
    # 构建消息
    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": user_prompt if user_prompt else "请分析这张图片的内容"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }
                }
            ]
        }
    ]
    
    # 调用 API
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=64000
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"分析图片时出错: {str(e)}"


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='图片识别与理解工具')
    parser.add_argument('image_path', help='图片文件路径')
    parser.add_argument('--prompt', '-p', help='额外的分析提示', default=None)
    
    args = parser.parse_args()
    
    # 检查图片文件是否存在
    if not os.path.exists(args.image_path):
        print(f"错误: 图片文件不存在: {args.image_path}")
        sys.exit(1)
    
    # 加载配置
    try:
        config = load_config()
    except FileNotFoundError as e:
        print(f"错误: {e}")
        sys.exit(1)
    
    # 分析图片
    result = analyze_image(
        image_path=args.image_path,
        api_base=config['api_base'],
        api_key=config['api_key'],
        model=config['model'],
        system_prompt=config['system_prompt'],
        user_prompt=args.prompt
    )
    
    print(result)


if __name__ == '__main__':
    main()