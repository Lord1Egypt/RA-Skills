#!/usr/bin/env python3
"""
微信公众号文章爬取脚本（增强版）

专门用于爬取微信公众号文章内容，支持保存图片。
"""

import asyncio
import json
import logging
import os
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from urllib.parse import urlparse, unquote

try:
    from playwright.async_api import async_playwright, Page
except ImportError:
    print("请先安装 Playwright: pip install playwright")
    print("然后安装浏览器: playwright install chromium")
    exit(1)


# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# 配置
CONFIG = {
    "headless": True,
    "timeout": 60000,
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "url": "https://mp.weixin.qq.com/s/HTGvy5C6SYyr5XQhTfTfzw",
    "save_images": True,  # 是否保存图片
    "images_dir": "images",  # 图片保存目录
    "image_quality": 90  # 图片质量 (0-100)
}


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
        # 使用 page.request 下载图片
        response = await page.request.get(img_url)
        if response.ok:
            image_data = await response.body()
            with open(save_path, 'wb') as f:
                f.write(image_data)
            logger.info(f"✅ 已保存图片: {save_path}")
            return True
        else:
            logger.warning(f"❌ 下载图片失败 (HTTP {response.status}): {img_url}")
            return False
    except Exception as e:
        logger.warning(f"❌ 下载图片异常: {img_url} - {e}")
        return False


async def extract_and_save_images(page: Page, images_dir: Path) -> List[Dict[str, Any]]:
    """提取并保存文章中的图片"""
    images_info = []
    
    try:
        # 获取所有图片元素
        img_elements = await page.query_selector_all("#js_content img, .rich_media_content img")
        
        if not img_elements:
            logger.info("未找到图片元素")
            return images_info
        
        logger.info(f"找到 {len(img_elements)} 张图片")
        
        for idx, img_element in enumerate(img_elements, 1):
            try:
                # 获取图片 URL
                src = await img_element.get_attribute("src")
                data_src = await img_element.get_attribute("data-src")
                
                # 优先使用 data-src（微信公众号常用）
                img_url = data_src or src
                
                if not img_url:
                    continue
                
                # 确保 URL 完整
                if img_url.startswith("//"):
                    img_url = "https:" + img_url
                elif img_url.startswith("/"):
                    img_url = "https://mp.weixin.qq.com" + img_url
                
                # 获取图片 alt 作为文件名
                alt = await img_element.get_attribute("alt") or f"image_{idx}"
                alt = sanitize_filename(alt)
                
                # 确定文件扩展名
                parsed = urlparse(img_url)
                path = unquote(parsed.path)
                ext = Path(path).suffix.lower()
                if not ext or ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                    ext = '.jpg'
                
                # 保存图片
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


async def fetch_wechat_article(url: str = None):
    """爬取微信公众号文章"""
    if url is None:
        url = CONFIG["url"]
    
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(
            headless=CONFIG["headless"],
            args=["--no-sandbox", "--disable-dev-shm-usage"]
        )
        page = await browser.new_page(
            user_agent=CONFIG["user_agent"],
            viewport={"width": 1920, "height": 1080}
        )
        page.set_default_timeout(CONFIG["timeout"])
        
        try:
            logger.info(f"正在访问微信公众号文章: {url}")
            
            # 访问页面
            try:
                await page.goto(url, wait_until="domcontentloaded")
            except Exception as e:
                logger.warning(f"domcontentloaded 超时，尝试 load: {e}")
                await page.goto(url, wait_until="load")
            
            # 等待页面渲染
            await asyncio.sleep(5)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 创建目录
            screenshots_dir = Path("screenshots")
            results_dir = Path("results")
            images_dir = Path(CONFIG["images_dir"]) / timestamp
            
            screenshots_dir.mkdir(exist_ok=True)
            results_dir.mkdir(exist_ok=True)
            if CONFIG["save_images"]:
                images_dir.mkdir(parents=True, exist_ok=True)
            
            # 截图
            try:
                screenshot_file = screenshots_dir / f"wechat_article_{timestamp}.png"
                await page.screenshot(path=str(screenshot_file), full_page=True)
                logger.info(f"已保存完整截图: {screenshot_file}")
            except Exception as e:
                logger.warning(f"截图失败: {e}")
            
            # 提取文章标题
            title = ""
            title_selectors = [
                "#activity-name",
                ".rich_media_title",
                "h1",
                "title"
            ]
            
            for selector in title_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        text = await element.inner_text()
                        if text and len(text.strip()) > 5:
                            title = text.strip()
                            logger.info(f"找到标题 (选择器: {selector}): {title}")
                            break
                except Exception as e:
                    logger.debug(f"选择器 {selector} 失败: {e}")
                    continue
            
            # 提取作者
            author = ""
            author_selectors = [
                "#js_name",
                ".rich_media_meta_nickname",
                ".profile_nickname"
            ]
            
            for selector in author_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        text = await element.inner_text()
                        if text:
                            author = text.strip()
                            logger.info(f"找到作者 (选择器: {selector}): {author}")
                            break
                except Exception as e:
                    logger.debug(f"选择器 {selector} 失败: {e}")
                    continue
            
            # 提取发布时间
            publish_date = ""
            date_selectors = [
                "#publish_time",
                ".rich_media_meta_text",
                "em#post-date"
            ]
            
            for selector in date_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        text = await element.inner_text()
                        if text:
                            publish_date = text.strip()
                            logger.info(f"找到时间 (选择器: {selector}): {publish_date}")
                            break
                except Exception as e:
                    logger.debug(f"选择器 {selector} 失败: {e}")
                    continue
            
            # 提取文章内容
            content = ""
            content_selectors = [
                "#js_content",
                ".rich_media_content",
                "#img-content"
            ]
            
            for selector in content_selectors:
                try:
                    element = await page.query_selector(selector)
                    if element:
                        text = await element.inner_text()
                        if text and len(text) > 100:
                            content = text
                            logger.info(f"找到内容 (选择器: {selector})，长度: {len(content)} 字符")
                            break
                except Exception as e:
                    logger.debug(f"选择器 {selector} 失败: {e}")
                    continue
            
            if not content:
                try:
                    content = await page.inner_text("body")
                    logger.info("使用 body 内容")
                except Exception as e:
                    logger.warning(f"获取 body 失败: {e}")
                    content = "无法提取内容"
            
            # 提取并保存图片
            images_info = []
            if CONFIG["save_images"]:
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
                "images_dir": str(images_dir) if CONFIG["save_images"] else None,
                "fetch_time": datetime.now().isoformat(),
                "length": len(content)
            }
            
            # 保存结果
            result_file = results_dir / f"wechat_article_{timestamp}.json"
            with open(result_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            logger.info(f"已保存结果: {result_file}")
            
            return result
            
        finally:
            await browser.close()


async def main():
    """主函数"""
    print("="*80)
    print("微信公众号文章爬取脚本（增强版）")
    print("="*80)
    
    url = CONFIG["url"]
    print(f"📄 目标文章: {url}")
    print(f"🖼️  保存图片: {'是' if CONFIG['save_images'] else '否'}")
    if CONFIG['save_images']:
        print(f"📁 图片目录: {CONFIG['images_dir']}/")
    print("="*80)
    
    result = await fetch_wechat_article(url)
    
    if result:
        print("\n" + "="*80)
        print(f"📰 标题: {result['title']}")
        if result['author']:
            print(f"✍️  作者: {result['author']}")
        if result['publish_date']:
            print(f"📅 发布时间: {result['publish_date']}")
        print(f"🔗 链接: {result['url']}")
        print(f"📝 内容长度: {result['length']} 字符")
        if CONFIG['save_images']:
            print(f"🖼️  图片保存: {result['images_count']}/{len(result['images'])} 张")
            print(f"📁 图片目录: {result['images_dir']}")
        print("="*80)
        print("\n📖 内容摘要:")
        print(result['content'][:1000] + "..." if len(result['content']) > 1000 else result['content'])
        print("\n" + "="*80)
        print("\n✅ 爬取完成！")
        print(f"📄 JSON 结果: results/wechat_article_*.json")
        print(f"🖼️  完整截图: screenshots/wechat_article_*.png")
        if CONFIG['save_images']:
            print(f"📷 文章图片: {result['images_dir']}/")
    else:
        print("\n❌ 未能获取文章内容")


if __name__ == "__main__":
    asyncio.run(main())
