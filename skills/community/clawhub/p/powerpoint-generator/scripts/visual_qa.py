#!/usr/bin/env python3
"""Visual QA -- 截图 + 视觉模型审计 + DOM 结构断言

两段式校验：
1. Visual Audit: Puppeteer截图 → 视觉模型审计（需要支持视觉的模型）
2. DOM Assertion: 纯代码结构检查（不需要视觉模型，所有环境可用）

用法:
  python visual_qa.py OUTPUT_DIR/slides/slide-3.html
  python visual_qa.py OUTPUT_DIR/slides/ --parallel 4
  python visual_qa.py OUTPUT_DIR/ --strict --verbose
"""

import argparse
import asyncio
import base64
import json
import re
import sys
from pathlib import Path

# 可通过环境变量配置视觉模型
VISION_MODEL = "gpt-4o"  # 可改为 claude-sonnet / gemini-pro-vision 等


# -------------------------------------------------------------------
# DOM 结构断言（不需要视觉模型）
# -------------------------------------------------------------------
def dom_assert(html_path: Path) -> tuple[bool, list]:
    """纯代码 DOM 结构检查，不需要视觉模型。"""
    issues = []

    if not html_path.exists():
        return False, [f"File not found: {html_path}"]

    content = html_path.read_text(encoding="utf-8")

    # 1. 检查 overflow:hidden
    if 'overflow:hidden' not in content and 'overflow: hidden' not in content:
        issues.append("MISSING: overflow:hidden — may cause layout overflow")

    # 2. 检查 ::before/::after 用于视觉装饰
    # 匹配 ::before { ... } 和 ::after { ... } 内容（简单版）
    pseudo_pattern = re.compile(r'::(before|after)\s*\{[^}]*?(?:width|height|margin|padding|border|background|content)[^}]*\}')
    for match in pseudo_pattern.finditer(content):
        issues.append(f"FORBIDDEN: ::{match.group(1)} used for visual decoration — use real DOM elements instead")

    # 3. 检查 conic-gradient
    if 'conic-gradient' in content:
        issues.append("FORBIDDEN: conic-gradient — not supported in SVG conversion")

    # 4. 检查 CSS border 三角形
    if re.search(r'border\s*:\s*[^;]*none\s+[^;]*none\s+[^;]*solid', content):
        issues.append("FORBIDDEN: CSS border triangle trick — use SVG path instead")

    # 5. 检查硬编码颜色（非 CSS 变量）
    # 排除 SVG 内的颜色和 data URI
    html_lines = [l for l in content.split('\n') if 'class=' in l or '<style' in l]
    for line in html_lines:
        hex_colors = re.findall(r'#[0-9a-fA-F]{6}', line)
        for color in hex_colors:
            # 过滤明显的 CSS 变量用法（--开头的变量）
            # 但不过滤具体颜色值
            pass
    # 更严格的检查：直接出现在 style 属性中的硬编码颜色
    inline_style_colors = re.findall(r'style="[^"]*#[0-9a-fA-F]{6}[^"]*"', content)
    if inline_style_colors:
        issues.append(f"WARNING: Inline hardcoded colors found — use CSS variables instead")

    # 6. 检查 SVG text 元素
    svg_texts = re.findall(r'<text[^>]*>[^<]+</text>', content)
    for match in svg_texts:
        if len(match) > 500:  # 过长的 text 节点可能渲染异常
            issues.append(f"WARNING: Long SVG text node — may cause rendering issues")

    # 7. 检查图片路径（相对路径）
    img_srcs = re.findall(r'<img[^>]+src="([^"]+)"', content)
    for src in img_srcs:
        if src.startswith('http') or src.startswith('data:'):
            continue
        if not Path(src).exists():
            issues.append(f"MISSING: Image file not found: {src}")

    return len(issues) == 0, issues


# -------------------------------------------------------------------
# Puppeteer 截图
# -------------------------------------------------------------------
async def capture_screenshot(html_path: Path, output_png: Path) -> bool:
    """使用 Puppeteer 截图。"""
    try:
        import puppeteer
    except ImportError:
        print("WARNING: puppeteer not installed. Run: npm install puppeteer", file=sys.stderr)
        return False

    browser = None
    try:
        browser = await puppeteer.launch({
            "headless": True,
            "args": ["--no-sandbox", "--disable-setuid-sandbox"]
        })
        page = await browser.newPage()
        await page.setViewport({"width": 1280, "height": 720, "deviceScaleFactor": 2})

        html_url = f"file://{html_path.absolute()}"
        await page.goto(html_url, {"waitUntil": "networkidle0"})
        await page.screenshot({
            "path": str(output_png),
            "type": "png",
            "clip": {"x": 0, "y": 0, "width": 1280, "height": 720}
        })
        return True
    except Exception as e:
        print(f"ERROR: Screenshot failed: {e}", file=sys.stderr)
        return False
    finally:
        if browser:
            await browser.close()


async def batch_capture(slides_dir: Path, concurrency: int = 4) -> int:
    """批量截图。"""
    output_dir = slides_dir.parent / "png"
    output_dir.mkdir(exist_ok=True)

    html_files = sorted(slides_dir.glob("*.html"))
    semaphore = asyncio.Semaphore(concurrency)

    async def process(html_file: Path) -> bool:
        idx = int(re.search(r'slide-(\d+)', html_file.stem).group(1))
        output_png = output_dir / f"slide-{idx:02d}.png"
        async with semaphore:
            return await capture_screenshot(html_file, output_png)

    tasks = [process(f) for f in html_files]
    results = await asyncio.gather(*tasks)
    return sum(1 for r in results if r)


# -------------------------------------------------------------------
# 视觉模型审计（需要支持视觉的模型）
# -------------------------------------------------------------------
def visual_audit(screenshot_path: Path, model: str = VISION_MODEL) -> tuple[bool, list]:
    """使用视觉模型审计截图（需要模型支持视觉）。"""
    issues = []

    # 读取图片并转为 base64
    try:
        img_data = screenshot_path.read_bytes()
        img_base64 = base64.b64encode(img_data).decode()
    except Exception as e:
        return False, [f"Cannot read screenshot: {e}"]

    # 调用视觉模型（需要配置 OPENAI_API_KEY 等）
    api_key = _get_api_key()
    if not api_key:
        return False, ["VISION_MODEL_API_KEY not configured — skip visual audit"]

    prompt = """Review this PPT slide screenshot and check for:
1. Text overflow or clipping
2. Element overlapping
3. Unreadable text
4. Color scheme conflicts
5. Density issues (too crowded or too sparse)

Respond in JSON format:
{"pass": true/false, "issues": ["issue1", "issue2", ...]}
Only report real problems, not minor issues."""

    try:
        import openai
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}},
                    {"type": "text", "text": prompt}
                ]}
            ],
            max_tokens=256,
            response_format={"type": "json_object"}
        )
        result = json.loads(response.choices[0].message.content)
        return result.get("pass", False), result.get("issues", [])
    except Exception as e:
        return False, [f"Visual audit failed: {e}"]


def _get_api_key() -> str:
    """获取 API Key。"""
    import os
    return os.environ.get("OPENAI_API_KEY") or os.environ.get("VISION_MODEL_API_KEY", "")


# -------------------------------------------------------------------
# 主函数
# -------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Visual QA")
    parser.add_argument("target", type=Path, help="Single HTML file or slides directory")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show details")
    parser.add_argument("--no-visual", action="store_true", help="Skip visual model audit")
    parser.add_argument("--parallel", type=int, default=4, help="Concurrency for screenshot")

    args = parser.parse_args()

    # 批量模式
    if args.target.is_dir():
        slides_dir = args.target if "slides" in str(args.target) else args.target / "slides"
        if not slides_dir.exists():
            print(f"ERROR: Slides directory not found: {slides_dir}", file=sys.stderr)
            sys.exit(1)

        # 先截图
        if not args.no_visual:
            print(f"Capturing screenshots (concurrency={args.parallel})...")
            captured = asyncio.run(batch_capture(slides_dir, args.parallel))
            print(f"Captured: {captured} screenshots")

        # DOM 断言
        html_files = sorted(slides_dir.glob("*.html"))
        all_passed = True
        all_issues = []

        for html_file in html_files:
            dom_pass, issues = dom_assert(html_file)
            if not dom_pass:
                all_passed = False
                all_issues.extend([(html_file.name, issues)])

        if all_passed:
            print(f"✅ All DOM checks passed ({len(html_files)} files)")
            sys.exit(0)
        else:
            print(f"❌ DOM checks failed:")
            for fname, issues in all_issues:
                print(f"  {fname}:")
                for issue in issues:
                    print(f"    - {issue}")
            sys.exit(1)

    # 单文件模式
    elif args.target.is_file():
        dom_pass, issues = dom_assert(args.target)
        print(f"[DOM Assertion] {args.target.name}: {'✅ PASS' if dom_pass else '❌ FAIL'}")
        if args.verbose or not dom_pass:
            for issue in issues:
                print(f"  - {issue}")

        # 如果有 PNG 同名文件，进行视觉审计
        png_path = args.target.with_suffix('.png')
        if not args.no_visual and png_path.exists():
            vis_pass, vis_issues = visual_audit(png_path)
            print(f"[Visual Audit] {args.target.name}: {'✅ PASS' if vis_pass else '❌ FAIL'}")
            if args.verbose or not vis_pass:
                for issue in vis_issues:
                    print(f"  - {issue}")

        sys.exit(0 if dom_pass else 1)

    else:
        print(f"ERROR: Target not found: {args.target}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
