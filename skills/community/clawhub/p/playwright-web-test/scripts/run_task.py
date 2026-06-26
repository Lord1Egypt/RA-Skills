#!/usr/bin/env python3
import os
import re
import sys
import json
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except Exception:
    print("错误：未安装 playwright。请先执行：python3 -m pip install playwright && python3 -m playwright install chromium")
    sys.exit(1)

OUTPUT_DIR = Path(os.environ.get("OPENCLAW_OUTPUT_DIR", "/tmp/playwright-web-test"))
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def detect_mode(user_input: str) -> str:
    s = user_input.lower()
    if any(k in s for k in ["console", "日志", "log"]):
        return "console"
    if any(k in s for k in ["按钮", "链接", "输入框", "元素", "discover", "selector"]):
        return "discover"
    return "screenshot"


def extract_target(user_input: str) -> str | None:
    patterns = [
        r'(https?://[^\s]+)',
        r'(file://[^\s]+)',
    ]
    for p in patterns:
        m = re.search(p, user_input)
        if m:
            return m.group(1)

    m = re.search(r'(/[^\s]+\.html?)', user_input)
    if m:
        return 'file://' + os.path.abspath(m.group(1))
    return None


def safe_name(name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9._-]+', '_', name)


def run_screenshot(page, target: str):
    out = OUTPUT_DIR / 'page.png'
    page.goto(target)
    page.wait_for_load_state('networkidle')
    page.screenshot(path=str(out), full_page=True)
    print(f"已完成页面截图：{out}")
    print(f"MEDIA:{out}")


def run_discovery(page, target: str):
    out = OUTPUT_DIR / 'discovery.png'
    page.goto(target)
    page.wait_for_load_state('networkidle')

    buttons = page.locator('button').all()
    links = page.locator('a[href]').all()
    inputs = page.locator('input, textarea, select').all()

    print(f"目标页面：{target}")
    print(f"发现按钮 {len(buttons)} 个")
    for i, button in enumerate(buttons[:20]):
        try:
            text = button.inner_text().strip() if button.is_visible() else '[隐藏]'
        except Exception:
            text = '[无法获取]'
        print(f"  [button:{i}] {text}")

    print(f"发现链接 {len(links)} 个（最多显示前 20 个）")
    for i, link in enumerate(links[:20]):
        try:
            text = (link.inner_text() or '').strip() or '[无文本]'
            href = link.get_attribute('href') or ''
        except Exception:
            text, href = '[获取失败]', ''
        print(f"  [link:{i}] {text} -> {href}")

    print(f"发现输入元素 {len(inputs)} 个")
    for i, elem in enumerate(inputs[:20]):
        try:
            name = elem.get_attribute('name') or elem.get_attribute('id') or '[未命名]'
            etype = elem.get_attribute('type') or elem.evaluate("e => e.tagName.toLowerCase()")
        except Exception:
            name, etype = '[获取失败]', '[获取失败]'
        print(f"  [input:{i}] {name} ({etype})")

    page.screenshot(path=str(out), full_page=True)
    print(f"页面结构截图：{out}")
    print(f"MEDIA:{out}")


def run_console(page, target: str):
    out = OUTPUT_DIR / 'console.log'
    logs = []

    def on_console(msg):
        logs.append(f"[{msg.type}] {msg.text}")
        print(f"控制台日志：[{msg.type}] {msg.text}")

    page.on('console', on_console)
    page.goto(target)
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(1000)
    out.write_text('\n'.join(logs), encoding='utf-8')
    print(f"共采集 {len(logs)} 条 console 日志")
    print(f"日志文件：{out}")


def main():
    user_input = ' '.join(sys.argv[1:]).strip()
    if not user_input:
        print("用法：python3 scripts/run_task.py '打开 http://localhost:5173 并截图'")
        sys.exit(1)

    target = extract_target(user_input)
    if not target:
        print("错误：未从输入中识别到 URL 或 file:// 路径。")
        sys.exit(1)

    mode = detect_mode(user_input)
    print(f"识别模式：{mode}")
    print(f"目标地址：{target}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1440, 'height': 900})

        try:
            if mode == 'console':
                run_console(page, target)
            elif mode == 'discover':
                run_discovery(page, target)
            else:
                run_screenshot(page, target)
        finally:
            browser.close()


if __name__ == '__main__':
    main()
