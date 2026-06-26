#!/usr/bin/env python3
"""
小红书图文创作脚本
用法: python3 generate_post.py --theme "主题" --audience "受众" --core "核心观点"
"""

import argparse
import os
import re
import subprocess
import sys
import urllib.parse

OUTPUT_BASE = "/root/.openclaw/workspace/output"
TEMPLATE_HTML = "/root/.openclaw/workspace/skills/xiaohongshu-post/scripts/xhs_cover_template.html"


def runSmartSearch(query: str, max_results: int = 8) -> str:
    script = "/root/.openclaw/workspace/scripts/smart_search.py"
    cmd = ["python3", script, query, "--max-results", str(max_results)]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout[:3000]
    except Exception as e:
        return f"[搜索失败] {e}"


def countChineseChars(text: str) -> int:
    """统计中文字符数（不含emoji）"""
    chinese = re.findall(r'[\u4e00-\u9fa5]', text)
    return len(chinese)


def countTotalChars(text: str) -> int:
    """统计总字符数（中文+英文+数字+emoji）"""
    return len(text)


def createOutputDir() -> str:
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    out_dir = os.path.join(OUTPUT_BASE, f"xhs_{today}")
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def generateCoverHTML(title: str, subtitle: str, out_path: str):
    """生成封面图 HTML 文件"""
    with open(TEMPLATE_HTML, "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("[主标题]", title)
    html = html.replace("[副标题/金句，1-2行]", subtitle)

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ 封面HTML已生成: {out_path}")


def screenshotCover(html_path: str, out_png: str):
    """Chrome headless 截图"""
    screenshot_js = f"""
    const puppeteer = require('puppeteer');
    (async () => {{
      const browser = await puppeteer.launch({{
        headless: 'new',
        args: ['--no-sandbox', '--disable-setuid-sandbox']
      }});
      const page = await browser.newPage();
      await page.setViewport({{ width: 1080, height: 1440, deviceScaleFactor: 2 }});
      await page.goto('file://{html_path}', {{ waitUntil: 'networkidle0' }});
      await page.screenshot({{ path: '{out_png}', type: 'png' }});
      await browser.close();
    }})();
    """

    # 优先用 puppeteer，没有则用 chrome
    try:
        import json, subprocess
        result = subprocess.run(
            ["google-chrome", "--version"],
            capture_output=True, text=True
        )
        print(f"Chrome: {result.stdout.strip()}")
    except Exception:
        print("⚠️ Chrome 不可用，尝试 chromium...")
        result = subprocess.run(
            ["chromium-browser", "--version"],
            capture_output=True, text=True
        )

    chrome_cmd = [
        "google-chrome", "--headless", "--disable-gpu", "--no-sandbox",
        "--screenshot=" + out_png,
        "--window-size=1080,1440",
        "--force-device-scale-factor=2",
        "file://" + html_path
    ]
    r = subprocess.run(chrome_cmd, capture_output=True, text=True, timeout=60)
    if r.returncode == 0:
        print(f"✅ 封面截图成功: {out_png}")
    else:
        print(f"⚠️ 截图失败（不影响整体交付）: {r.stderr[:200]}")


def compressImage(in_path: str, out_path: str):
    """压缩图片"""
    compress_script = "/root/.openclaw/workspace/skills/content-factory/scripts/compress_image.py"
    r = subprocess.run(
        ["python3", compress_script, in_path, out_path, "85"],
        capture_output=True, text=True, timeout=60
    )
    if r.returncode == 0:
        print(f"✅ 图片压缩完成: {out_path}")
    else:
        print(f"⚠️ 压缩失败（使用原图）: {r.stderr[:200]}")


def writeContentMd(title: str, body: str, hashtags: str, out_path: str):
    """写入文案文件"""
    content = f"# {title}\n\n{body}\n\n{hashtags}"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ 文案已保存: {out_path}")


def main():
    parser = argparse.ArgumentParser(description="小红书图文创作")
    parser.add_argument("--theme", required=True, help="主题/话题")
    parser.add_argument("--audience", required=True, help="面向受众")
    parser.add_argument("--core", required=True, help="核心观点")
    args = parser.parse_args()

    theme = args.theme
    audience = args.audience
    core = args.core

    print(f"\n{'='*50}")
    print(f"📌 主题: {theme}")
    print(f"📌 受众: {audience}")
    print(f"📌 核心观点: {core}")
    print(f"{'='*50}\n")

    # Step 1: 网络调研
    print("🔍 正在网络调研...")
    q1 = f"{theme} {audience} 痛点"
    q2 = f"{theme} 解决方案 案例"
    q3 = f"{theme} 小红书 热门"
    r1 = runSmartSearch(q1, 8)
    r2 = runSmartSearch(q2, 5)
    r3 = runSmartSearch(q3, 5)
    print(f"  调研完成\n")

    # Step 2: 生成文案（LLM 调用说明）
    # 注意：此脚本为脚手架，实际 LLM 调用在 agent 对话中完成
    print("📝 文案创作提示：")
    print(f"  基于以下调研内容创作小红书文案：")
    print(f"  主题: {theme}")
    print(f"  受众: {audience}")
    print(f"  核心观点: {core}")
    print(f"  调研摘要(Q1): {r1[:300]}...")
    print(f"  调研摘要(Q2): {r2[:300]}...")
    print(f"  调研摘要(Q3): {r3[:300]}...")
    print()
    print("📋 文案要求：")
    print("  标题：≤20字符，数字+悬念/对比/情绪公式")
    print("  正文：≤1000字符（中文），含emoji，口语化")
    print("  结尾：Hashtag 5-10个")
    print()

    # 输出文件路径供 agent 参考
    out_dir = createOutputDir()
    content_path = os.path.join(out_dir, "content.md")
    html_cover = os.path.join(out_dir, "cover.html")
    png_cover = os.path.join(out_dir, "cover.png")
    jpg_cover = os.path.join(out_dir, "cover_compressed.jpg")

    print(f"📁 输出目录: {out_dir}")
    print(f"  文案: {content_path}")
    print(f"  封面HTML: {html_cover}")
    print(f"  封面图: {jpg_cover}")


if __name__ == "__main__":
    main()
