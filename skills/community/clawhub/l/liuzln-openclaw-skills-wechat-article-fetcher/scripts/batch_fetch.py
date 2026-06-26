#!/usr/bin/env python3
"""
微信公众号文章批量爬取工具

支持从文件或命令行读取多个 URL 进行批量爬取。
"""

import argparse
import asyncio
import logging
import sys
from pathlib import Path
from typing import List

# 导入 fetch.py 中的函数
sys.path.insert(0, str(Path(__file__).parent))
from fetch import fetch_article


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def batch_fetch(
    urls: List[str],
    output_dir: str = "./wechat_articles",
    save_images: bool = True,
    save_screenshot: bool = True,
    headless: bool = True,
    timeout: int = 60000,
    delay: float = 2.0
):
    """
    批量爬取文章
    
    Args:
        urls: URL 列表
        output_dir: 输出目录
        save_images: 是否保存图片
        save_screenshot: 是否保存截图
        headless: 是否无头模式
        timeout: 超时时间
        delay: 每次爬取之间的延迟（秒）
    """
    results = []
    total = len(urls)
    
    print("="*80)
    print(f"批量爬取工具 - 共 {total} 篇文章")
    print("="*80)
    
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{total}] 正在处理: {url[:60]}...")
        
        try:
            result = await fetch_article(
                url=url,
                output_dir=output_dir,
                save_images=save_images,
                save_screenshot=save_screenshot,
                headless=headless,
                timeout=timeout
            )
            
            if result:
                results.append({
                    "index": i,
                    "url": url,
                    "title": result['title'],
                    "success": True,
                    "article_dir": result['article_dir']
                })
                print(f"✅ [{i}/{total}] 成功: {result['title'][:50]}...")
            else:
                results.append({
                    "index": i,
                    "url": url,
                    "success": False,
                    "error": "爬取失败"
                })
                print(f"❌ [{i}/{total}] 失败")
        
        except Exception as e:
            logger.error(f"爬取异常: {e}", exc_info=True)
            results.append({
                "index": i,
                "url": url,
                "success": False,
                "error": str(e)
            })
            print(f"❌ [{i}/{total}] 异常: {e}")
        
        # 延迟（除了最后一个）
        if i < total and delay > 0:
            print(f"⏳ 等待 {delay} 秒...")
            await asyncio.sleep(delay)
    
    # 总结
    print("\n" + "="*80)
    print("批量爬取完成")
    print("="*80)
    
    success_count = sum(1 for r in results if r['success'])
    print(f"\n📊 统计: {success_count}/{total} 成功")
    
    if success_count < total:
        print("\n❌ 失败的文章:")
        for r in results:
            if not r['success']:
                print(f"  - [{r['index']}] {r['url'][:60]}...")
                if 'error' in r:
                    print(f"    错误: {r['error']}")
    
    return results


def read_urls_from_file(file_path: str) -> List[str]:
    """从文件中读取 URL"""
    urls = []
    path = Path(file_path)
    
    if not path.exists():
        logger.error(f"文件不存在: {file_path}")
        return urls
    
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                urls.append(line)
    
    return urls


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="微信公众号文章批量爬取工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从命令行指定多个 URL
  python batch_fetch.py --urls "url1" "url2" "url3"
  
  # 从文件中读取 URL 列表
  python batch_fetch.py --urls-file urls.txt
  
  # 不保存图片，减少延迟
  python batch_fetch.py --urls-file urls.txt --no-images --delay 1
        """
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--urls", nargs="+", help="URL 列表（多个）")
    group.add_argument("--urls-file", help="包含 URL 列表的文件路径")
    
    parser.add_argument("-o", "--output", default="./wechat_articles", help="输出目录 (默认: ./wechat_articles)")
    parser.add_argument("--no-images", action="store_true", help="不保存图片")
    parser.add_argument("--no-screenshot", action="store_true", help="不保存截图")
    parser.add_argument("--headless", type=bool, default=True, help="无头模式 (默认: true)")
    parser.add_argument("--timeout", type=int, default=60000, help="超时时间，毫秒 (默认: 60000)")
    parser.add_argument("--delay", type=float, default=2.0, help="每次爬取之间的延迟，秒 (默认: 2.0)")
    
    args = parser.parse_args()
    
    # 获取 URL 列表
    if args.urls_file:
        urls = read_urls_from_file(args.urls_file)
    else:
        urls = args.urls
    
    if not urls:
        print("❌ 没有找到有效的 URL")
        sys.exit(1)
    
    # 运行
    asyncio.run(batch_fetch(
        urls=urls,
        output_dir=args.output,
        save_images=not args.no_images,
        save_screenshot=not args.no_screenshot,
        headless=args.headless,
        timeout=args.timeout,
        delay=args.delay
    ))


if __name__ == "__main__":
    main()
