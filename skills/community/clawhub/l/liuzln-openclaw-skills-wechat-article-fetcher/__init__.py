#!/usr/bin/env python3
"""
微信公众号文章爬取 - 简单调用接口

可以被直接调用的简单接口，用于快速爬取微信公众号文章。
"""

import sys
import json
import asyncio
from pathlib import Path

# 添加模块路径
skill_dir = Path(__file__).parent
sys.path.insert(0, str(skill_dir))


def fetch(url: str, venv_path: str = None, output_dir: str = "./wechat_articles"):
    """
    爬取微信公众号文章（简单接口）
    
    Args:
        url: 文章 URL
        venv_path: 虚拟环境路径（可选）
        output_dir: 输出目录
    
    Returns:
        爬取结果字典
    """
    if venv_path:
        # 使用虚拟环境方式
        from wechat_article_fetcher import fetch_article_with_venv
        return fetch_article_with_venv(
            url=url,
            venv_path=venv_path,
            output_dir=output_dir
        )
    else:
        # 直接调用方式
        from wechat_article_fetcher import fetch_article_sync
        return fetch_article_sync(
            url=url,
            output_dir=output_dir
        )


def print_summary(result: dict):
    """打印文章摘要"""
    if not result:
        print("❌ 爬取失败")
        return
    
    print("="*80)
    print("📰 微信公众号文章")
    print("="*80)
    print(f"标题: {result['title']}")
    if result.get('author'):
        print(f"作者: {result['author']}")
    if result.get('publish_date'):
        print(f"发布时间: {result['publish_date']}")
    print(f"链接: {result['url']}")
    print(f"内容长度: {result['length']} 字符")
    if result.get('images_count'):
        print(f"图片: {result['images_count']} 张")
    print("="*80)
    print("\n📖 内容摘要:")
    content = result['content']
    print(content[:1000] + "..." if len(content) > 1000 else content)
    print("\n" + "="*80)
    if result.get('base_output_dir'):
        print(f"\n📁 保存位置: {result['base_output_dir']}/{result['article_dir']}/")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="微信公众号文章快速爬取")
    parser.add_argument("url", help="文章 URL")
    parser.add_argument("--venv", help="虚拟环境路径（可选）")
    parser.add_argument("-o", "--output", default="./wechat_articles", help="输出目录")
    parser.add_argument("--summary", action="store_true", help="只打印摘要")
    
    args = parser.parse_args()
    
    result = fetch(args.url, args.venv, args.output)
    
    if args.summary:
        print_summary(result)
    elif result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
