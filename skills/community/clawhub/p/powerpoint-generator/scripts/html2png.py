#!/usr/bin/env python3
"""HTML to PNG -- 将 HTML 文件截图生成 PNG 图片

使用 Puppeteer 对每个 HTML 文件进行截图，支持多页并行。
优先使用完整 puppeteer（含捆绑 Chrome）；
若失败则自动降级到 puppeteer-core + 系统 Chrome（/usr/bin/google-chrome）。

用法:
  python html2png.py <slides_dir> -o <output_dir>
  python html2png.py ppt-output/slides/ -o ppt-output/png/
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

# -------------------------------------------------------------------
# 配置
# -------------------------------------------------------------------
SLIDE_WIDTH = 1280
SLIDE_HEIGHT = 720

import platform
import os

def get_chrome_path():
    system = platform.system()
    if system == 'Windows':
        paths = [
            os.path.expandvars(r'%ProgramFiles%\Google\Chrome\Application\chrome.exe'),
            os.path.expandvars(r'%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe'),
            os.path.expandvars(r'%LocalAppData%\Google\Chrome\Application\chrome.exe'),
        ]
        for p in paths:
            if os.path.exists(p):
                return p
        return None
    elif system == 'Darwin':  # macOS
        return '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    else:  # Linux
        return '/usr/bin/google-chrome'
SYSTEM_CHROME_PATH = get_chrome_path()


# -------------------------------------------------------------------
# Puppeteer 初始化（优先 puppeteer，降级 puppeteer-core）
# -------------------------------------------------------------------
_puppeteer_cache = None
_chrome_path_cache = None

def get_puppeteer():
    """优先使用 puppeteer，降级到 puppeteer-core + 系统 Chrome"""
    global _puppeteer_cache, _chrome_path_cache
    
    if _puppeteer_cache is not None:
        return _puppeteer_cache
    
    # 优先尝试 puppeteer（自带 Chrome）
    try:
        import puppeteer
        print("Using puppeteer (bundled Chrome)")
        _puppeteer_cache = puppeteer
        _chrome_path_cache = None
        return puppeteer
    except ImportError:
        pass

    # 降级到 puppeteer-core
    try:
        import puppeteer_core as puppeteer
    except ImportError:
        try:
            import puppeteer_core as puppeteer
        except ImportError:
            # 安装 puppeteer-core
            print("Installing puppeteer-core...")
            import subprocess
            subprocess.run(
                ["npm", "install", "puppeteer-core"],
                capture_output=True, text=True, timeout=60
            )
            try:
                import puppeteer_core as puppeteer
            except ImportError:
                print("ERROR: Neither puppeteer nor puppeteer-core installed.", file=sys.stderr)
                print("Run: npm install -g puppeteer puppeteer-core", file=sys.stderr)
                _puppeteer_cache = False
                return None

    # 检查系统 Chrome
    if Path(SYSTEM_CHROME_PATH).exists():
        _chrome_path_cache = SYSTEM_CHROME_PATH
        print(f"Using puppeteer-core with system Chrome: {_chrome_path_cache}")
    else:
        print(f"WARNING: System Chrome not found at {SYSTEM_CHROME_PATH}", file=sys.stderr)
        _chrome_path_cache = None

    _puppeteer_cache = puppeteer
    return puppeteer


# -------------------------------------------------------------------
# Puppeteer 截图核心
# -------------------------------------------------------------------
async def screenshot_html(html_path: Path, output_path: Path, page_number: int = 0, chrome_path: str = None) -> bool:
    """对单个 HTML 文件截图。"""
    puppeteer = get_puppeteer()
    if not puppeteer:
        return False

    browser = None
    try:
        launch_opts = {
            "headless": True,
            "args": ["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage"]
        }
        if chrome_path:
            launch_opts["executablePath"] = chrome_path
        elif hasattr(puppeteer, '_chrome_path') and puppeteer._chrome_path:
            launch_opts["executablePath"] = puppeteer._chrome_path

        browser = await puppeteer.launch(**launch_opts)
        page = await browser.newPage()
        await page.setViewport({"width": SLIDE_WIDTH, "height": SLIDE_HEIGHT, "deviceScaleFactor": 2})

        # 加载 HTML 文件
        html_url = f"file://{html_path.absolute()}"
        await page.goto(html_url, {"waitUntil": "networkidle0"})

        # 等待字体加载完成
        try:
            await page.evaluate("""document.fonts.ready""")
        except Exception:
            pass  # 字体等待超时不影响截图

        # 截图
        await page.screenshot({
            "path": str(output_path),
            "type": "png",
            "fullPage": False,
            "clip": {"x": 0, "y": 0, "width": SLIDE_WIDTH, "height": SLIDE_HEIGHT}
        })

        print(f"  [{page_number}] {html_path.name} -> {output_path.name}")
        return True

    except Exception as e:
        print(f"  [!] {html_path.name}: {e}", file=sys.stderr)
        return False

    finally:
        if browser:
            await browser.close()


async def batch_screenshot(slides_dir: Path, output_dir: Path, concurrency: int = 4) -> int:
    """批量截图，支持并发控制。"""
    output_dir.mkdir(parents=True, exist_ok=True)

    html_files = sorted(slides_dir.glob("*.html"))
    if not html_files:
        print(f"WARNING: No HTML files found in {slides_dir}", file=sys.stderr)
        return 0

    print(f"Found {len(html_files)} HTML files, processing with concurrency={concurrency}...")

    # 获取 chrome 路径
    puppeteer = get_puppeteer()
    chrome_path = None
    if _chrome_path_cache:
        chrome_path = _chrome_path_cache

    # 创建信号量控制并发
    semaphore = asyncio.Semaphore(concurrency)

    async def process_file(html_file: Path, idx: int) -> bool:
        output_file = output_dir / f"slide-{idx:02d}.png"
        async with semaphore:
            return await screenshot_html(html_file, output_file, idx, chrome_path)

    tasks = [process_file(f, i) for i, f in enumerate(html_files, 1)]
    results = await asyncio.gather(*tasks)

    success = sum(1 for r in results if r)
    print(f"\nCompleted: {success}/{len(results)} screenshots")
    return success


def main():
    parser = argparse.ArgumentParser(description="HTML to PNG screenshot generator")
    parser.add_argument("slides_dir", type=Path, help="Directory containing HTML slide files")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output directory for PNG files")
    parser.add_argument("-c", "--concurrency", type=int, default=4, help="Max concurrent screenshots (default: 4)")
    parser.add_argument("--width", type=int, default=1280, help="Viewport width (default: 1280)")
    parser.add_argument("--height", type=int, default=720, help="Viewport height (default: 720)")

    args = parser.parse_args()

    global SLIDE_WIDTH, SLIDE_HEIGHT
    SLIDE_WIDTH = args.width
    SLIDE_HEIGHT = args.height

    if not args.slides_dir.exists():
        print(f"ERROR: Slides directory not found: {args.slides_dir}", file=sys.stderr)
        sys.exit(1)

    success = asyncio.run(batch_screenshot(args.slides_dir, args.output, args.concurrency))
    sys.exit(0 if success > 0 else 1)


if __name__ == "__main__":
    main()