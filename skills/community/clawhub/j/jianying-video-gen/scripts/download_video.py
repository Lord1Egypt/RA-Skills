import asyncio
import json
import os
import re
import argparse
from playwright.async_api import async_playwright

COOKIES_FILE = os.path.join(os.path.dirname(__file__), '..', 'cookies.json')
DOWNLOAD_DIR = r'D:\SQLMessage\AI_Videos'


def load_and_clean_cookies():
    with open(COOKIES_FILE, 'r') as f:
        raw = json.load(f)
    cleaned = []
    allowed = ['name', 'value', 'domain', 'path', 'expires', 'httpOnly', 'secure']
    for c in raw:
        clean = {}
        for key in allowed:
            if key == 'expires':
                val = c.get('expirationDate') or c.get('expires')
                if val is not None:
                    clean['expires'] = val
                continue
            if key in c and c[key] is not None:
                clean[key] = c[key]
        cleaned.append(clean)
    return cleaned


async def download_with_page(context, video_url, output_path):
    """使用新页面直接访问视频URL来下载"""
    print(f"  [下载] 使用Playwright页面下载...")
    
    # 创建新页面访问视频URL
    video_page = await context.new_page()
    
    try:
        # 导航到视频URL - 不等待networkidle，因为大视频不会触发
        print(f"  [信息] 请求视频...")
        response = await video_page.goto(video_url, wait_until='domcontentloaded', timeout=120000)
        
        if response:
            print(f"  [信息] 响应状态: {response.status}")
            print(f"  [信息] Content-Type: {response.headers.get('content-type', 'unknown')}")
            print(f"  [信息] Content-Length: {response.headers.get('content-length', 'unknown')}")
            
            if response.status in [200, 206]:
                # 等待一下确保数据开始传输
                await asyncio.sleep(2)
                
                # 直接读取响应体
                print(f"  [信息] 读取响应体...")
                body = await response.body()
                
                if body and len(body) > 1000:  # 确保不是空响应或错误页面
                    with open(output_path, 'wb') as f:
                        f.write(body)
                    
                    size = os.path.getsize(output_path)
                    print(f"  [OK] 下载成功: {size/1024/1024:.2f} MB")
                    await video_page.close()
                    return True
                else:
                    print(f"  [ERR] 响应体太小: {len(body) if body else 0} bytes")
        
        print(f"  [ERR] 无法下载，状态: {response.status if response else 'None'}")
        await video_page.close()
        return False
        
    except Exception as e:
        print(f"  [ERR] 下载异常: {e}")
        import traceback
        traceback.print_exc()
        try:
            await video_page.close()
        except:
            pass
        return False


async def query_and_download(task_id: str, output_name: str = None):
    """查询任务并下载视频"""
    print(f"[查询] 任务ID: {task_id}")
    
    # 确保输出目录存在
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        
        # 注入cookies
        print("[步骤1] 注入登录凭证...")
        cookies = load_and_clean_cookies()
        await context.add_cookies(cookies)
        print(f"  [OK] {len(cookies)} cookies 已注入")
        
        page = await context.new_page()
        
        # 导航到任务详情页
        detail_url = f"https://xyq.jianying.com/home?tab_name=integrated-agent&thread_id={task_id}"
        print(f"[步骤2] 访问任务详情页...")
        print(f"       {detail_url}")
        
        try:
            await page.goto(detail_url, wait_until='networkidle', timeout=30000)
            await asyncio.sleep(3)
        except Exception as e:
            print(f"  [WARN] 页面加载超时，继续检查...")
        
        # 检查视频是否就绪
        print("[步骤3] 检查视频状态...")
        
        # 滚动页面确保视频元素加载
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        await asyncio.sleep(1)
        
        # 尝试多种方式找到视频元素
        video_url = None
        
        # 方法1: 直接查询 video 标签
        try:
            video_element = await page.query_selector('video')
            if video_element:
                video_url = await video_element.get_attribute('src')
                if video_url:
                    print(f"  [OK] 从video标签找到视频")
        except:
            pass
        
        # 方法2: 查询 source 标签
        if not video_url:
            try:
                source_element = await page.query_selector('video source')
                if source_element:
                    video_url = await source_element.get_attribute('src')
                    if video_url:
                        print(f"  [OK] 从source标签找到视频")
            except:
                pass
        
        # 方法3: 从页面HTML中提取
        if not video_url:
            content = await page.content()
            patterns = [
                r'https?://[^\s"\'<>]+\.mp4[^\s"\'<>]*',
                r'"url"\s*:\s*"(https?://[^"]+video[^"]*)"',
                r'src="(https?://[^"]+\.mp4[^"]*)"',
            ]
            for pattern in patterns:
                matches = re.findall(pattern, content)
                if matches:
                    video_url = matches[0]
                    print(f"  [OK] 从HTML提取到视频链接")
                    break
        
        # 检查状态
        if not video_url:
            page_text = await page.evaluate('() => document.body.innerText')
            if '生成中' in page_text:
                print("  [状态] 视频仍在生成中，请稍后再试")
                await browser.close()
                return False
            elif '失败' in page_text:
                print("  [状态] 视频生成失败")
                await browser.close()
                return False
            else:
                print("  [ERR] 未找到视频链接")
                debug_path = os.path.join(DOWNLOAD_DIR, f'debug_{task_id}.png')
                await page.screenshot(path=debug_path, full_page=True)
                print(f"  [调试] 截图已保存: {debug_path}")
                await browser.close()
                return False
        
        # 清理URL
        video_url = video_url.replace('\\u0026', '&').replace('\\', '')
        print(f"  [链接] {video_url[:80]}...")
        
        # 下载视频
        print("[步骤4] 开始下载视频...")
        if not output_name:
            output_name = f"video_{task_id[:8]}.mp4"
        if not output_name.endswith('.mp4'):
            output_name += '.mp4'
        
        output_path = os.path.join(DOWNLOAD_DIR, output_name)
        
        success = await download_with_page(context, video_url, output_path)
        
        await browser.close()
        
        if success:
            print(f"\n[完成] 视频已保存: {output_path}")
            return True
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='查询并下载剪映视频')
    parser.add_argument('task_id', help='任务ID')
    parser.add_argument('--output', '-o', help='输出文件名（可选）')
    
    args = parser.parse_args()
    
    asyncio.run(query_and_download(args.task_id, args.output))
