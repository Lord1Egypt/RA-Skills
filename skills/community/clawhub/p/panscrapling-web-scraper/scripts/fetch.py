#!/usr/bin/env python3
"""
Panscrapling Web Scraper - 主抓取脚本
自动绕过 Cloudflare，支持动态渲染
"""
import sys
import json
import argparse
import subprocess
import os
import re
from pathlib import Path
from urllib.parse import urlparse

# ═══════════════════════════════════════════════════════════════
#  配置
# ═══════════════════════════════════════════════════════════════

SKILL_DIR = Path(__file__).parent.parent
WHEELS_DIR = SKILL_DIR / "wheels"
SETUP_SCRIPT = SKILL_DIR / "scripts" / "setup.py"

SCRAPLING_INSTALLED = False
PYTHON_PATH = None

# ═══════════════════════════════════════════════════════════════
#  Python 检测
# ═══════════════════════════════════════════════════════════════

PYTHON_PATHS = [
    "/opt/homebrew/bin/python3.11",
    "/opt/homebrew/bin/python3.12",
    "/opt/homebrew/bin/python3.13",
    "/usr/local/bin/python3.11",
    "/usr/local/bin/python3.12",
    "/usr/local/bin/python3.13",
]


def find_python():
    """查找 Python 3.10+"""
    global PYTHON_PATH
    
    if PYTHON_PATH:
        return PYTHON_PATH
    
    # 检查预定义路径
    for py in PYTHON_PATHS:
        if os.path.isfile(py):
            try:
                r = subprocess.run([py, "--version"], capture_output=True, text=True, timeout=5)
                m = re.search(r"Python (\d+)\.(\d+)", r.stdout)
                if m and int(m.group(2)) >= 10:
                    PYTHON_PATH = py
                    return py
            except:
                pass
    
    # 检查当前 Python
    v = sys.version_info
    if v.major == 3 and v.minor >= 10:
        PYTHON_PATH = sys.executable
        return sys.executable
    
    return None


# ═══════════════════════════════════════════════════════════════
#  自动安装
# ═══════════════════════════════════════════════════════════════

def run_setup():
    """运行自动安装脚本"""
    python_path = find_python()
    
    if not python_path:
        print("📦 Python 3.10+ not found, running setup...")
    else:
        # 检查 scrapling 是否已安装
        try:
            r = subprocess.run(
                [python_path, "-c", "import scrapling"],
                capture_output=True, timeout=5
            )
            if r.returncode == 0:
                global SCRAPLING_INSTALLED
                SCRAPLING_INSTALLED = True
                return python_path
        except:
            pass
    
    # 运行 setup.py
    if SETUP_SCRIPT.exists():
        print("📦 Running setup script...")
        subprocess.run([sys.executable, str(SETUP_SCRIPT)], check=False)
        
        # 重新检测
        python_path = find_python()
        if python_path:
            SCRAPLING_INSTALLED = True
        return python_path
    
    return None


# ═══════════════════════════════════════════════════════════════
#  Fetcher
# ═══════════════════════════════════════════════════════════════

def get_fetcher(mode="auto", headless=True, solve_cloudflare=True):
    """获取 Fetcher"""
    from scrapling.fetchers import Fetcher, StealthyFetcher, DynamicFetcher
    
    if mode == "fast":
        return lambda url: Fetcher.get(url, stealthy_headers=True)
    elif mode == "stealthy":
        return lambda url: StealthyFetcher.fetch(url, headless=headless, solve_cloudflare=solve_cloudflare)
    elif mode == "dynamic":
        return lambda url: DynamicFetcher.fetch(url, headless=headless, network_idle=True)
    else:  # auto
        return lambda url: StealthyFetcher.fetch(url, headless=headless, solve_cloudflare=solve_cloudflare)


# ═══════════════════════════════════════════════════════════════
#  内容提取
# ═══════════════════════════════════════════════════════════════

def extract_content(page, selector=None, xpath=None, output="text"):
    """从页面提取内容"""
    result = {"url": getattr(page, 'url', None), "status": "success"}
    
    if selector:
        elements = page.css(selector)
        if elements:
            result["data"] = [e.css("::text").get() for e in elements] if output != "html" else [e.get() for e in elements]
        else:
            result["data"] = []
            result["warning"] = f"No elements found for selector: {selector}"
    elif xpath:
        elements = page.xpath(xpath)
        if elements:
            result["data"] = [e.css("::text").get() for e in elements] if output != "html" else [e.get() for e in elements]
        else:
            result["data"] = []
            result["warning"] = f"No elements found for xpath: {xpath}"
    else:
        if output == "text":
            texts = page.css("body ::text").getall()
            result["data"] = " ".join(texts).strip()
        elif output == "markdown":
            result["data"] = to_markdown(page)
        else:
            result["data"] = page.css("body").get()
    
    return result


def extract_links(page):
    """提取链接"""
    return [{"text": a.css("::text").get(default="").strip(), "href": a.attrib.get("href", "")} 
            for a in page.css("a")]


def extract_images(page):
    """提取图片"""
    return [{"src": img.attrib.get("src", ""), "alt": img.attrib.get("alt", "")} 
            for img in page.css("img")]


def extract_meta(page):
    """提取元数据"""
    meta = {"title": page.css("title::text").get(default="")}
    for m in page.css("meta"):
        name = m.attrib.get("name", m.attrib.get("property", ""))
        if name in ["description", "keywords", "og:title", "og:description", "og:image"]:
            meta[name] = m.attrib.get("content", "")
    return meta


def to_markdown(page):
    """转 Markdown"""
    lines = []
    for i in range(1, 7):
        for h in page.css(f"h{i}"):
            text = h.css("::text").get(default="").strip()
            if text:
                lines.append("#" * i + " " + text)
    for p in page.css("p"):
        text = p.css("::text").get(default="").strip()
        if text:
            lines.append(text + "\n")
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
#  主函数
# ═══════════════════════════════════════════════════════════════

def fetch(url, mode="auto", selector=None, xpath=None, output="text", 
          headless=True, solve_cloudflare=True):
    """抓取网页"""
    global SCRAPLING_INSTALLED
    
    if not SCRAPLING_INSTALLED:
        python_path = run_setup()
        if not python_path:
            return {"error": "Failed to setup Python/Scrapling", "url": url}
    
    try:
        fetcher = get_fetcher(mode, headless, solve_cloudflare)
        page = fetcher(url)
        return extract_content(page, selector, xpath, output)
    except Exception as e:
        return {"error": str(e), "url": url, "hint": "Try --mode stealthy or --mode dynamic"}


def main():
    parser = argparse.ArgumentParser(description="Panscrapling Web Scraper")
    parser.add_argument("url", nargs="?", help="URL to scrape")
    parser.add_argument("--mode", "-m", default="auto", 
                       choices=["auto", "stealthy", "dynamic", "fast"])
    parser.add_argument("--selector", "-s", help="CSS selector")
    parser.add_argument("--xpath", "-x", help="XPath")
    parser.add_argument("--output", "-o", default="text", 
                       choices=["text", "html", "json", "markdown"])
    parser.add_argument("--text", action="store_true")
    parser.add_argument("--links", action="store_true")
    parser.add_argument("--images", action="store_true")
    parser.add_argument("--meta", action="store_true")
    parser.add_argument("--markdown", action="store_true")
    parser.add_argument("--setup", action="store_true", help="Run setup only")
    
    args = parser.parse_args()
    
    if args.setup:
        run_setup()
        return
    
    if not args.url:
        parser.print_help()
        return
    
    output = "markdown" if args.markdown else args.output
    result = fetch(args.url, args.mode, args.selector, args.xpath, output)
    
    # 额外提取
    if "error" not in result:
        if args.text or args.links or args.images or args.meta:
            try:
                page = get_fetcher(args.mode)(args.url)
                if args.text:
                    result["text"] = " ".join(page.css("body ::text").getall()).strip()
                if args.links:
                    result["links"] = extract_links(page)
                if args.images:
                    result["images"] = extract_images(page)
                if args.meta:
                    result["meta"] = extract_meta(page)
            except:
                pass
    
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
