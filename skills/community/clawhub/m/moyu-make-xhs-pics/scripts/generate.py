#!/usr/bin/env python3
"""
命令行工具 - 生成小红书图片
"""

import argparse
import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src import generate_article_images, VALID_STYLES, VALID_LAYOUTS


def main():
    parser = argparse.ArgumentParser(
        description="小红书图片生成工具"
    )
    
    parser.add_argument(
        "article",
        help="文章文件路径"
    )
    
    parser.add_argument(
        "--cover", "-c",
        type=int,
        default=1,
        help="封面图数量 (默认: 1)"
    )
    
    parser.add_argument(
        "--illustration", "-i",
        type=int,
        default=1,
        help="插图数量 (默认: 1)"
    )
    
    parser.add_argument(
        "--decoration", "-d",
        type=int,
        default=2,
        help="配图数量 (默认: 2)"
    )
    
    parser.add_argument(
        "--style", "-s",
        choices=VALID_STYLES,
        default="fresh",
        help=f"风格 (默认: fresh)"
    )
    
    parser.add_argument(
        "--layout", "-l",
        choices=VALID_LAYOUTS,
        default="auto",
        help="布局 (默认: auto)"
    )
    
    parser.add_argument(
        "--provider", "-p",
        choices=["minimax", "dashscope"],
        default="minimax",
        help="API 提供商 (默认: minimax)"
    )
    
    args = parser.parse_args()
    
    print(f"📄 文章: {args.article}")
    print(f"🎨 风格: {args.style}")
    print(f"📐 布局: {args.layout}")
    print(f"🤖 Provider: {args.provider}")
    print(f"📊 数量: 封面{args.cover} + 插图{args.illustration} + 配图{args.decoration}")
    print()
    
    result = generate_article_images(
        article_path=args.article,
        cover_count=args.cover,
        illustration_count=args.illustration,
        decoration_count=args.decoration,
        style=args.style,
        layout=args.layout,
        provider=args.provider
    )
    
    if result["success"]:
        print("✅ 生成成功!")
        print()
        
        if result["covers"]:
            print("� cover:")
            for path in result["covers"]:
                print(f"  - {path}")
        
        if result["illustrations"]:
            print("📐 illustration:")
            for path in result["illustrations"]:
                print(f"  - {path}")
        
        if result["decorations"]:
            print("🖼️ decoration:")
            for path in result["decorations"]:
                print(f"  - {path}")
        
        print()
        print(f"总计: {result['total']} 张图片")
    else:
        print(f"❌ 生成失败: {result['error']}")
        sys.exit(1)


if __name__ == "__main__":
    main()
