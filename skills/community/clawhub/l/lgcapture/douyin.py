#!/usr/bin/env python3
"""
抖音视频抓取 - 最终优化版
2026-02-25 实测有效
"""
import asyncio
import sys
import requests
from playwright.async_api import async_playwright
import re

async def download_douyin(url):
    """自动识别并下载抖音视频 - 有效版本"""
    
    # 1. 提取视频ID
    video_id = None
    
    # 短链接处理
    if 'v.douyin.com' in url:
        try:
            resp = requests.head(url, allow_redirects=True, timeout=10)
            final_url = resp.url
            match = re.search(r'/video/(\d+)', final_url)
            if match:
                video_id = match.group(1)
        except:
            pass
    
    # 标准链接处理
    if not video_id:
        match = re.search(r'/video/(\d+)', url)
        if match:
            video_id = match.group(1)
    
    if not video_id:
        print("❌ 无法提取视频ID")
        return None
    
    print(f"📌 视频ID: {video_id}")
    
    # 2. 使用 Playwright 获取页面
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={'width': 375, 'height': 812},
            user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Safari/604.1'
        )
        page = await context.new_page()
        
        await page.goto(f'https://www.douyin.com/video/{video_id}', 
                       wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(3000)
        
        # 3. 获取视频元素 (关键步骤)
        video = await page.query_selector('video')
        if not video:
            print("❌ 页面中未找到视频元素")
            await browser.close()
            return None
        
        # 4. 从 src 属性提取 video_id
        src = await video.get_attribute('src')
        if not src:
            print("❌ 无法获取视频链接")
            await browser.close()
            return None
        
        print(f"📹 视频src: {src[:80]}...")
        
        # 5. 提取 video_id 构造下载链接
        match = re.search(r'video_id=([^&"]+)', src)
        if match:
            vid = match.group(1)
            download_url = f"https://www.douyin.com/aweme/v1/playwm/?video_id={vid}&ratio=720p&line=0"
        else:
            # 直接使用 src 作为下载链接
            download_url = src
        
        # 6. 下载视频
        print(f"⬇️ 下载中...")
        resp = requests.get(download_url, headers={
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15',
            'Referer': 'https://www.douyin.com/'
        }, timeout=60)
        
        output = f'/tmp/douyin_{video_id}.mp4'
        with open(output, 'wb') as f:
            f.write(resp.content)
        
        await browser.close()
        
        size = len(resp.content) / 1024 / 1024
        print(f"✅ 下载完成: {output} ({size:.1f} MB)")
        return output

def main():
    url = sys.argv[1] if len(sys.argv) > 1 else None
    if not url:
        print("用法: python3 douyin.py <抖音链接>")
        print("示例: python3 douyin.py https://v.douyin.com/xxx/")
        sys.exit(1)
    
    asyncio.run(download_douyin(url))

if __name__ == "__main__":
    main()
