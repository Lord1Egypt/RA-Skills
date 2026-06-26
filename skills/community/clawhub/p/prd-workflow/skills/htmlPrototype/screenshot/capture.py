#!/usr/bin/env python3
"""
截图工具 - 智能降级方案

优先级：
1. html2image（轻量，推荐安装：pip install html2image）
2. macOS Safari（零依赖，仅 macOS）
3. Playwright（备选）
4. 提示手动操作
"""

import subprocess
import platform
from pathlib import Path


def screenshot(html_path: str, output_path: str, width: int = 1440, height: int = 900) -> bool:
    """
    智能截图 - 自动选择最佳方案

    Args:
        html_path: HTML 文件路径
        output_path: 输出图片路径
        width: viewport 宽度
        height: viewport 高度

    Returns:
        是否成功
    """
    html_path = Path(html_path).resolve()
    output_path = Path(output_path).resolve()

    if not html_path.exists():
        print(f"❌ HTML 文件不存在：{html_path}")
        return False

    # 确保输出目录存在
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 方案 1：html2image（推荐，最轻量）
    try:
        result = _html2image_screenshot(html_path, output_path, width, height)
        if result:
            return True
    except ImportError:
        pass
    except Exception as e:
        print(f"⚠️ html2image 截图失败：{e}")

    # 方案 2：macOS Safari（零依赖）
    if platform.system() == 'Darwin':
        try:
            result = _safari_screenshot(html_path, output_path, width, height)
            if result:
                return True
        except Exception as e:
            print(f"⚠️ Safari 截图失败：{e}")

    # 方案 3：Playwright（备选）
    try:
        result = _playwright_screenshot(html_path, output_path, width, height)
        if result:
            return True
    except ImportError:
        pass
    except Exception as e:
        print(f"⚠️ Playwright 截图失败：{e}")

    # 方案 4：降级提示
    print("\n⚠️ 无法自动截图，请选择以下方式：")
    print("   1. 安装轻量方案：pip install html2image")
    print("   2. 安装完整方案：pip install playwright && playwright install chromium")
    print(f"   3. 手动查看：open {html_path}")
    print(f"   4. 手动截图后保存到：{output_path}")
    return False


def _html2image_screenshot(html_path: Path, output_path: Path, width: int, height: int) -> bool:
    """html2image 截图（推荐方案）"""
    from html2image import Html2Image

    hti = Html2Image(size=(width, height), output_path=str(output_path.parent))

    # 跨平台浏览器路径
    system = platform.system()
    chrome_paths = {
        'Darwin': [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ],
        'Windows': [
            "C:/Program Files/Google/Chrome/Application/chrome.exe",
            "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe",
            "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe",
        ],
        'Linux': [
            "/usr/bin/google-chrome",
            "/usr/bin/chromium-browser",
            "/usr/bin/chromium",
        ]
    }

    # 尝试找到可用的浏览器
    if system in chrome_paths:
        for chrome_path in chrome_paths[system]:
            if Path(chrome_path).exists():
                hti.chrome_path = chrome_path
                break

    # 截图
    html_content = html_path.read_text(encoding='utf-8')
    hti.screenshot(html_str=html_content, save_as=output_path.name)

    # 验证
    if output_path.exists():
        print(f"✅ html2image 截图成功")
        return True
    return False


def _safari_screenshot(html_path: Path, output_path: Path, width: int, height: int) -> bool:
    """macOS Safari 截图（零依赖方案）"""
    script = f'''
    tell application "Safari"
        activate
        set newDoc to make new document at end of documents
        set URL of newDoc to "file://{html_path}"
        delay 1.5
        set bounds of window 1 to {{0, 0, {width}, {height}}}
        delay 0.5
    end tell
    do shell script "screencapture -x -R 0,0,{width},{height} {output_path}"
    tell application "Safari" to close window 1
    '''

    result = subprocess.run(
        ['osascript', '-e', script],
        capture_output=True,
        text=True,
        timeout=30
    )

    if result.returncode == 0 and output_path.exists():
        print(f"✅ Safari 截图成功")
        return True
    elif result.returncode != 0:
        raise Exception(result.stderr)
    return False


def _playwright_screenshot(html_path: Path, output_path: Path, width: int, height: int) -> bool:
    """Playwright 截图（备选方案）"""
    from playwright.sync_api import sync_playwright

    # 尝试使用系统 Chrome
    chrome_path = None
    system = platform.system()

    chrome_paths = {
        'Darwin': "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        'Windows': "C:/Program Files/Google/Chrome/Application/chrome.exe",
        'Linux': "/usr/bin/google-chrome",
    }

    if system in chrome_paths and Path(chrome_paths[system]).exists():
        chrome_path = chrome_paths[system]

    with sync_playwright() as p:
        # 优先使用系统 Chrome，否则使用 Playwright 下载的 Chromium
        launch_options = {'headless': True}
        if chrome_path:
            launch_options['executable_path'] = chrome_path

        browser = p.chromium.launch(**launch_options)
        page = browser.new_page(viewport={'width': width, 'height': height})
        page.goto(f'file://{html_path}')
        page.wait_for_load_state('networkidle')
        page.screenshot(path=str(output_path), full_page=True)
        browser.close()

    if output_path.exists():
        print(f"✅ Playwright 截图成功")
        return True
    return False


# ============ 向后兼容 ============
def capture(html_path: str, output_path: str, width: int = 1440, height: int = 900) -> bool:
    """向后兼容的函数名"""
    return screenshot(html_path, output_path, width, height)


# ============ CLI 测试 ============
if __name__ == "__main__":
    import sys
    import tempfile

    # 创建测试 HTML
    test_html = '''
    <!DOCTYPE html>
    <html>
    <head><title>Test</title></head>
    <body style="font-family: sans-serif; padding: 40px;">
        <h1>📸 截图测试</h1>
        <p>如果你看到这张图片，说明截图功能正常工作！</p>
        <p>当前方案：智能降级</p>
    </body>
    </html>
    '''

    # 写入临时文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(test_html)
        html_path = f.name

    output_path = tempfile.mktemp(suffix='.png')

    print("=" * 50)
    print("📸 截图工具测试")
    print("=" * 50)

    result = screenshot(html_path, output_path)

    if result:
        print(f"\n✅ 测试成功！")
        print(f"📁 输出：{output_path}")
        print(f"📊 大小：{Path(output_path).stat().st_size / 1024:.1f} KB")

        # macOS 自动打开
        if platform.system() == 'Darwin':
            subprocess.run(['open', output_path])
    else:
        print(f"\n❌ 测试失败")

    # 清理
    Path(html_path).unlink(missing_ok=True)