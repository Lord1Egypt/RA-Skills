#!/usr/bin/env python3
"""
微信公众号文章爬取模块

可以直接导入使用的模块，方便被其他程序调用。
"""

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


# 配置日志
logger = logging.getLogger(__name__)


def _sanitize_filename(filename: str) -> str:
    """清理文件名，移除非法字符"""
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    filename = filename.strip()
    if len(filename) > 100:
        filename = filename[:100]
    return filename


async def _download_image(page, img_url: str, save_path: Path) -> bool:
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


async def _extract_and_save_images(page, images_dir: Path) -> List[Dict[str, Any]]:
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
                alt = _sanitize_filename(alt)
                
                parsed = urlparse(img_url)
                path = unquote(parsed.path)
                ext = Path(path).suffix.lower()
                if not ext or ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
                    ext = '.jpg'
                
                img_filename = f"{idx:03d}_{alt}{ext}"
                img_path = images_dir / img_filename
                
                success = await _download_image(page, img_url, img_path)
                
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
    timeout: int = 60000,
    playwright_path: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    爬取微信公众号文章（异步版本）
    
    Args:
        url: 文章 URL
        output_dir: 输出目录
        save_images: 是否保存图片
        save_screenshot: 是否保存截图
        headless: 是否无头模式
        timeout: 超时时间（毫秒）
        playwright_path: Playwright 虚拟环境路径（可选）
    
    Returns:
        爬取结果字典，失败返回 None
    """
    # 验证 URL
    if not url or "mp.weixin.qq.com" not in url:
        logger.error("请提供有效的微信公众号文章 URL")
        return None
    
    # 如果指定了虚拟环境路径，使用该环境的 Playwright
    if playwright_path:
        venv_python = Path(playwright_path) / "bin" / "python"
        if venv_python.exists():
            logger.info(f"使用虚拟环境: {playwright_path}")
            # 注意：这里需要用 subprocess 调用，因为不能在运行时切换解释器
            # 所以这个参数主要是给 run_in_venv 用的
            pass
    
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        logger.error("请先安装 Playwright: pip install playwright")
        logger.error("然后安装浏览器: playwright install chromium")
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
                images_info = await _extract_and_save_images(page, images_dir)
            
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
                "base_output_dir": str(base_output_dir.absolute()),
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


def fetch_article_sync(
    url: str,
    output_dir: str = "./wechat_articles",
    save_images: bool = True,
    save_screenshot: bool = True,
    headless: bool = True,
    timeout: int = 60000,
    playwright_path: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    爬取微信公众号文章（同步版本）
    
    这是一个包装函数，可以在非异步代码中直接调用。
    
    Args:
        url: 文章 URL
        output_dir: 输出目录
        save_images: 是否保存图片
        save_screenshot: 是否保存截图
        headless: 是否无头模式
        timeout: 超时时间（毫秒）
        playwright_path: Playwright 虚拟环境路径（可选）
    
    Returns:
        爬取结果字典，失败返回 None
    """
    try:
        # 检查是否已经有事件循环在运行
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # 如果已经在运行，创建一个新任务
            async def _run():
                return await fetch_article(
                    url=url,
                    output_dir=output_dir,
                    save_images=save_images,
                    save_screenshot=save_screenshot,
                    headless=headless,
                    timeout=timeout,
                    playwright_path=playwright_path
                )
            # 注意：在已运行的循环中需要用不同的方式处理
            # 这里简化处理，直接用 run_until_complete
            return asyncio.run(_run())
        else:
            # 如果没有运行的循环，直接运行
            return asyncio.run(fetch_article(
                url=url,
                output_dir=output_dir,
                save_images=save_images,
                save_screenshot=save_screenshot,
                headless=headless,
                timeout=timeout,
                playwright_path=playwright_path
            ))
    except RuntimeError as e:
        # 如果事件循环有问题，尝试新的策略
        if "event loop is closed" in str(e):
            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop.run_until_complete(fetch_article(
                url=url,
                output_dir=output_dir,
                save_images=save_images,
                save_screenshot=save_screenshot,
                headless=headless,
                timeout=timeout,
                playwright_path=playwright_path
            ))
        else:
            raise


def fetch_article_with_venv(
    url: str,
    venv_path: str,
    output_dir: str = "./wechat_articles",
    save_images: bool = True,
    save_screenshot: bool = True,
    headless: bool = True,
    timeout: int = 60000
) -> Optional[Dict[str, Any]]:
    """
    在指定虚拟环境中爬取微信公众号文章
    
    这个函数会使用 subprocess 调用虚拟环境中的 Python 来运行脚本。
    
    Args:
        url: 文章 URL
        venv_path: 虚拟环境路径
        output_dir: 输出目录
        save_images: 是否保存图片
        save_screenshot: 是否保存截图
        headless: 是否无头模式
        timeout: 超时时间（毫秒）
    
    Returns:
        爬取结果字典，失败返回 None
    """
    import subprocess
    import tempfile
    
    # 检查虚拟环境
    venv_python = Path(venv_path) / "bin" / "python"
    if not venv_python.exists():
        venv_python = Path(venv_path) / "Scripts" / "python.exe"
    
    if not venv_python.exists():
        logger.error(f"找不到虚拟环境的 Python: {venv_path}")
        return None
    
    # 创建一个临时脚本
    script_content = f'''
import asyncio
import sys
import json
from pathlib import Path

# 添加脚本目录到路径
skill_dir = Path(r"{Path(__file__).parent}")
sys.path.insert(0, str(skill_dir / "scripts"))

from fetch import fetch_article

async def main():
    result = await fetch_article(
        url=r"{url}",
        output_dir=r"{output_dir}",
        save_images={save_images},
        save_screenshot={save_screenshot},
        headless={headless},
        timeout={timeout}
    )
    if result:
        print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(main())
'''
    
    # 这里简化处理，直接调用现有的 fetch.py 脚本
    script_dir = Path(__file__).parent
    fetch_script = script_dir / "scripts" / "fetch.py"
    
    if not fetch_script.exists():
        logger.error(f"找不到脚本: {fetch_script}")
        return None
    
    # 构建命令
    cmd = [str(venv_python), str(fetch_script), url, "-o", output_dir]
    if not save_images:
        cmd.append("--no-images")
    if not save_screenshot:
        cmd.append("--no-screenshot")
    
    logger.info(f"在虚拟环境中运行: {venv_path}")
    logger.info(f"执行命令: {' '.join(cmd)}")
    
    try:
        # 运行命令
        result = subprocess.run(
            cmd,
            cwd=str(script_dir.parent.parent),
            capture_output=False,
            text=True
        )
        
        # 注意：这里只是运行脚本，不解析输出
        # 实际结果保存在 output_dir 中
        
        if result.returncode == 0:
            logger.info("✅ 爬取完成！")
            # 尝试找到最新的结果
            output_path = Path(output_dir)
            if output_path.exists():
                # 找到最新的目录
                dirs = sorted([d for d in output_path.iterdir() if d.is_dir()], 
                            key=lambda x: x.stat().st_mtime, reverse=True)
                if dirs:
                    latest_dir = dirs[0]
                    json_path = latest_dir / "article.json"
                    if json_path.exists():
                        with open(json_path, 'r', encoding='utf-8') as f:
                            return json.load(f)
        
        return None
        
    except Exception as e:
        logger.error(f"运行失败: {e}", exc_info=True)
        return None
