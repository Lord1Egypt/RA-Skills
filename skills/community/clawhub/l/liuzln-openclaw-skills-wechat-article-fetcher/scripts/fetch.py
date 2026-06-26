#!/usr/bin/env python3
"""
微信公众号文章爬取工具 - 命令行版本

支持任意微信公众号文章 URL，自动提取内容并保存图片。
"""

import argparse
import asyncio
import json
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, unquote

try:
    from playwright.async_api import async_playwright, Page
except ImportError:
    print("请先安装 Playwright: pip install playwright")
    print("然后安装浏览器: playwright install chromium")
    sys.exit(1)


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def sanitize_filename(filename: str) -> str:
    """清理文件名，移除非法字符"""
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = filename.strip()
    if len(filename) > 100:
        filename = filename[:100]
    return filename


async def download_image(page: Page, img_url: str, save_path: Path) -> bool:
    """下载图片"""
    try:
        response = await page.request.get(img_url)
        if response.ok:
            image_data = await response.body()
            with open(save_path, 'wb') as f:
                f.write(image_data)
            logger.info(f"✅ 已保存图片: {save_path.name}")
            return True
        else:
            logger.warning(f"❌ 下载图片失败 (HTTP {response.status}): {img_url}")
            return False
    except Exception as e:
        logger.warning(f"❌ 下载图片异常: {e}")
        return False


async def extract_and_save_images(page: Page, images_dir: Path) -> List[Dict[str, Any]]:
    """提取并保存文章中的图片"""
    images_info = []
    
    try:
        img_elements = await page.query_selector_all("#js_content img, .rich_media_content img")
        
        if not img_elements:
            logger.info("未找到图片元素")
            return images_info
        
        logger.info(f"找到 {len(img_elements)} 张图片")
        
        for idx, img_element in enumerate(img_elements, 1):
            try:
                src = await img_element.get_attribute("src")
                data_src = await img_element.get_attribute("data-src")
                img_url = data_src or src
                
                if not img_url:
                    continue
                
                if img_url.startswith("//"):
                    img_url = "https:" + img_url
                elif img_url.startswith("/"):
                    img_url = "https://mp.weixin.qq.com" + img_url
                
                alt = await img_element.get_attribute("alt") or f"image_{idx}"
                alt = sanitize_filename(alt)
                
                parsed = urlparse(img_url)
                path = unquote(parsed.path)
                ext = Path(path).suffix.lower()
                if not ext or ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                    ext = '.jpg'
                
                img_filename = f"{idx:03d}_{alt}{ext}"
                img_path = images_dir / img_filename
                
                success = await download_image(page, img_url, img_path)
                
                images_info.append({
                    "index": idx,
                    "url": img_url,
                    "alt": alt,
                    "filename": img_filename,
                    "success": success
                })
                
            except Exception as e:
                logger.warning(f"处理图片 {idx} 时出错: {e}")
                continue
        
    except Exception as e:
        logger.error(f"提取图片时出错: {e}", exc_info=True)
    
    return images_info


async def fetch_article(
    url: str,
    output_dir: str = "./wechat_articles",
    save_images: bool = True,
    save_screenshot: bool = True,
    headless: bool = True,
    timeout: int = 60000
) -> Optional[Dict[str, Any]]:
    """
    爬取微信公众号文章
    
    Args:
        url: 文章 URL
        output_dir: 输出目录
        save_images: 是否保存图片
        save_screenshot: 是否保存截图
        headless: 是否无头模式
        timeout: 超时时间（毫秒）
    
    Returns:
        爬取结果字典，失败返回 None
    """
    # 验证 URL
    if not url or "mp.weixin.qq.com" not in url:
        logger.error("请提供有效的微信公众号文章 URL")
        return None
    
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(
            headless=headless,
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080}
        )
        page.set_default_timeout(timeout)
        
        try:
            logger.info(f"正在访问: {url}")
            
            # 访问页面
            try:
                await page.goto(url, wait_until="domcontentloaded")
            except Exception as e:
                logger.warning(f"domcontentloaded 超时，尝试 load: {e}")
                await page.goto(url, wait_until="load")
            
            await asyncio.sleep(5)
            
            # 创建输出目录
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_output_dir = Path(output_dir)
            article_dir = base_output_dir / timestamp
            
            base_output_dir.mkdir(parents=True, exist_ok=True)
            article_dir.mkdir(exist_ok=True)
            
            images_dir = article_dir / "images"
            if save_images:
                images_dir.mkdir(exist_ok=True)
            
            # 保存截图
            screenshot_path = None
            if save_screenshot:
                try:
                    screenshot_path = article_dir / "article.png"
                    await page.screenshot(path=str(screenshot_path), full_page=True)
                    logger.info(f"已保存截图: {screenshot_path.name}")
                except Exception as e:
                    logger.warning(f"截图失败: {e}")
            
            # 提取标题
            title = ""
            title_selectors = ["#activity-name", ".rich_media_title", "h1", "title"]
            for selector in title_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        text = await element.inner_text()
                        if text and len(text.strip()) > 5:
                            title = text.strip()
                            break
                except:
                    continue
            
            # 提取作者
            author = ""
            author_selectors = ["#js_name", ".rich_media_meta_nickname", ".profile_nickname"]
            for selector in author_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        text = await element.inner_text()
                        if text:
                            author = text.strip()
                            break
                except:
                    continue
            
            # 提取发布时间
            publish_date = ""
            date_selectors = ["#publish_time", ".rich_media_meta_text", "em#post-date"]
            for selector in date_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        text = await element.inner_text()
                        if text:
                            publish_date = text.strip()
                            break
                except:
                    continue
            
            # 提取内容
            content = ""
            content_selectors = ["#js_content", ".rich_media_content", "#img-content"]
            for selector in content_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        text = await element.inner_text()
                        if text and len(text) > 100:
                            content = text
                            break
                except:
                    continue
            
            if not content:
                try:
                    content = await page.inner_text("body")
                except Exception as e:
                    logger.warning(f"获取 body 失败: {e}")
                    content = "无法提取内容"
            
            # 提取并保存图片
            images_info = []
            if save_images:
                logger.info("开始提取图片...")
                images_info = await extract_and_save_images(page, images_dir)
            
            # 构造结果
            result = {
                "title": title,
                "author": author,
                "publish_date": publish_date,
                "url": url,
                "content": content,
                "images": images_info,
                "images_count": len([i for i in images_info if i["success"]]),
                "images_dir": str(images_dir.relative_to(base_output_dir)) if save_images else None,
                "screenshot": str(screenshot_path.relative_to(base_output_dir)) if screenshot_path else None,
                "article_dir": str(article_dir.relative_to(base_output_dir)),
                "fetch_time": datetime.now().isoformat(),
                "length": len(content)
            }
            
            # 保存 JSON
            json_path = article_dir / "article.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            logger.info(f"已保存结果: {json_path.name}")
            
            return result
            
        finally:
            await browser.close()


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description="微信公众号文章爬取工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基本用法
  python fetch.py https://mp.weixin.qq.com/s/xxx
  
  # 指定输出目录
  python fetch.py https://mp.weixin.qq.com/s/xxx -o ./my_articles
  
  # 不保存图片
  python fetch.py https://mp.weixin.qq.com/s/xxx --no-images
  
  # 不保存截图
  python fetch.py https://mp.weixin.qq.com/s/xxx --no-screenshot
        """
    )
    
    parser.add_argument("url", help="微信公众号文章 URL")
    parser.add_argument("-o", "--output", default="./wechat_articles", help="输出目录 (默认: ./wechat_articles)")
    parser.add_argument("--no-images", action="store_true", help="不保存图片")
    parser.add_argument("--no-screenshot", action="store_true", help="不保存截图")
    parser.add_argument("--headless", type=bool, default=True, help="无头模式 (默认: true)")
    parser.add_argument("--timeout", type=int, default=60000, help="超时时间，毫秒 (默认: 60000)")
    
    args = parser.parse_args()
    
    print("="*80)
    print("微信公众号文章爬取工具")
    print("="*80)
    print(f"📄 URL: {args.url}")
    print(f"📁 输出目录: {args.output}")
    print(f"🖼️  保存图片: {'否' if args.no_images else '是'}")
    print(f"📸 保存截图: {'否' if args.no_screenshot else '是'}")
    print("="*80)
    
    # 运行
    result = asyncio.run(fetch_article(
        url=args.url,
        output_dir=args.output,
        save_images=not args.no_images,
        save_screenshot=not args.no_screenshot,
        headless=args.headless,
        timeout=args.timeout
    ))
    
    if result:
        print("\n" + "="*80)
        print(f"📰 标题: {result['title']}")
        if result['author']:
            print(f"✍️  作者: {result['author']}")
        if result['publish_date']:
            print(f"📅 发布时间: {result['publish_date']}")
        print(f"📝 内容长度: {result['length']} 字符")
        if not args.no_images:
            print(f"🖼️  图片保存: {result['images_count']}/{len(result['images'])} 张")
        print("="*80)
        print("\n📖 内容摘要:")
        print(result['content'][:800] + "..." if len(result['content']) > 800 else result['content'])
        print("\n" + "="*80)
        print(f"\n✅ 爬取完成！")
        print(f"📁 文章目录: {args.output}/{result['article_dir']}/")
        print(f"📄 JSON 结果: {args.output}/{result['article_dir']}/article.json")
        if not args.no_screenshot and result['screenshot']:
            print(f"📸 完整截图: {args.output}/{result['screenshot']}")
        if not args.no_images and result['images_dir']:
            print(f"📷 文章图片: {args.output}/{result['images_dir']}/")
    else:
        print("\n❌ 爬取失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
