# GxpCode Skill — Step A 新源分析：打开页面，落地完整 HTML

import sys
import os
from datetime import datetime
from playwright.sync_api import sync_playwright
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def _next_filename(output_dir: str) -> str:
    """stepA_20260625_001.html → stepA_20260625_002.html"""
    today = datetime.now().strftime("%Y%m%d")
    num = 1
    while True:
        path = os.path.join(output_dir, f"stepA_{today}_{num:03d}.html")
        if not os.path.exists(path):
            return path
        num += 1


def run(url: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    path = _next_filename(output_dir)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/125.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
        )
        page = context.new_page()
        page.goto(url, timeout=30000, wait_until="networkidle")
        page.wait_for_timeout(3000)

        html = page.content()
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)

        title = page.title()
        print(f"Title: {title}")
        print(f"HTML: {len(html)} chars → {path}")

        browser.close()


if __name__ == "__main__":
    run(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "gxpcode_data")
