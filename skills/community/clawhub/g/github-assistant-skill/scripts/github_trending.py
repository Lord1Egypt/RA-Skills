#!/usr/bin/env python3
"""
GitHub Trending Fetcher - Browser Mode Only

⚠️ IMPORTANT: GitHub does NOT provide an official Trending API.
This script ONLY uses browser automation to scrape real Trending data from:
- Daily:   https://github.com/trending?since=daily
- Weekly:  https://github.com/trending?since=weekly
- Monthly: https://github.com/trending?since=monthly

Browser mode opens a VISIBLE browser window so users can see the process.
"""

import json
import sys
import re
import os
import time
import platform

# Import centralized configuration
from config import get_auth_state_file


def fetch_trending_via_browser(since="daily", language=""):
    """
    Playwright browser scraper - extracts real GitHub Trending data.
    
    Opens a VISIBLE browser window (headless=False) so users can see:
    - Browser launching
    - Navigation to GitHub Trending page
    - Data extraction process
    
    URLs accessed:
    - https://github.com/trending?since=daily
    - https://github.com/trending?since=weekly  
    - https://github.com/trending?since=monthly
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {
            "success": False,
            "error": "playwright not installed. Run: pip install playwright && playwright install chromium",
            "data": []
        }

    auth_file = get_auth_state_file()
    storage_state = auth_file if os.path.exists(auth_file) else None

    results = []

    # 检测可用的浏览器（备用方案）
    def find_browser_executable():
        """查找可用的浏览器可执行文件（用于备用方案）"""
        system = platform.system()
        
        possible_paths = []
        
        if system == "Darwin":  # macOS
            possible_paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
                "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
            ]
        elif system == "Linux":
            possible_paths = [
                "/usr/bin/google-chrome",
                "/usr/bin/google-chrome-stable",
                "/usr/bin/chromium",
                "/usr/bin/chromium-browser",
                # WSL下的Windows浏览器
                "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe",
                "/mnt/c/Program Files (x86)/Google/Chrome/Application/chrome.exe",
            ]
        elif system == "Windows":
            possible_paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
                r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            ]
            # 尝试从注册表获取Chrome路径
            try:
                import winreg
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe") as key:
                    chrome_path, _ = winreg.QueryValueEx(key, "")
                    if chrome_path and os.path.exists(chrome_path):
                        possible_paths.insert(0, chrome_path)
            except:
                pass
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"   ✓ 找到系统浏览器: {path}")
                return path
        
        return None

    # 检测运行环境
    def is_headless_environment():
        """检测是否在无图形界面环境运行（如Agent/服务器）"""
        # 检查常见headless环境标志
        if os.environ.get('DISPLAY') == '' and platform.system() == 'Linux':
            return True
        if os.environ.get('CI') == 'true':
            return True
        if os.environ.get('HEADLESS') == 'true':
            return True
        # 检查是否在Docker容器内
        if os.path.exists('/.dockerenv'):
            return True
        return False

    with sync_playwright() as p:
        print(f"🌐 Opening browser to fetch GitHub Trending ({since})...")
        
        # 尝试查找系统浏览器
        browser_path = find_browser_executable()
        
        # 自动检测环境并设置headless模式
        headless_mode = is_headless_environment()
        if headless_mode:
            print("   ℹ️  检测到无图形界面环境，使用headless模式")
        
        launch_options = {"headless": headless_mode}
        if browser_path:
            launch_options["executable_path"] = browser_path
        
        try:
            browser = p.chromium.launch(**launch_options)
        except Exception as e:
            error_msg = str(e)
            if "Executable doesn't exist" in error_msg:
                # 在Agent环境中提供更友好的提示
                if is_headless_environment():
                    return {
                        "success": False,
                        "error": f"浏览器未安装。在Agent/服务器环境中，请使用以下方案：\n"
                                f"1. 【推荐】使用Docker: docker run -it --rm mcr.microsoft.com/playwright/python:v1.40.0-jammy\n"
                                f"2. 安装Playwright: python3 -m playwright install chromium\n"
                                f"3. 查看README中的'方案2-Docker'或'方案3-API模式'",
                        "data": []
                    }
                return {
                    "success": False,
                    "error": f"浏览器未安装。请尝试以下方案：\n"
                            f"1. 安装Playwright浏览器: python3 -m playwright install chromium\n"
                            f"2. 使用Docker（推荐Agent环境）: docker run -it --rm mcr.microsoft.com/playwright/python:v1.40.0-jammy\n"
                            f"3. 查看README中的安装方案",
                    "data": []
                }
            raise
        context = browser.new_context(storage_state=storage_state)
        page = context.new_page()

        # Build GitHub Trending URL
        url = "https://github.com/trending"
        if language:
            url += f"/{language}"
        url += f"?since={since}"

        print(f"   Navigating to: {url}")
        page.goto(url, timeout=30000, wait_until="domcontentloaded")
        page.wait_for_selector("article", timeout=15000)
        print(f"   ✓ Page loaded, extracting data...")
        
        # Scroll to load all repositories (GitHub Trending uses infinite scroll)
        print("   Scrolling to load all repositories...")
        last_count = 0
        max_scrolls = 50  # Prevent infinite loops
        scroll_count = 0
        
        while scroll_count < max_scrolls:
            # Get current article count
            articles = page.query_selector_all("article")
            current_count = len(articles)
            
            if current_count == last_count:
                # No new content loaded
                break
            
            print(f"   ... loaded {current_count} repositories")
            last_count = current_count
            
            # Scroll to bottom
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(1.5)  # Wait for content to load
            
            scroll_count += 1
        
        print(f"   ✓ Finished scrolling, total {last_count} repositories found")
        
        # Extract data from all articles
        articles = page.query_selector_all("article")
        for article in articles:
            try:
                # Repo name (owner/repo)
                name_el = article.query_selector("h2 a")
                name = name_el.get_attribute("href").strip("/") if name_el else ""
                repo_url = f"https://github.com/{name}" if name else ""

                # Description
                desc_el = article.query_selector("p")
                description = desc_el.inner_text().strip() if desc_el else ""

                # Language
                lang_el = article.query_selector("[itemprop='programmingLanguage']")
                lang = lang_el.inner_text().strip() if lang_el else ""

                # Total Stars
                stars_el = article.query_selector("a[href*='/stargazers']")
                stars_text = stars_el.inner_text().strip().replace(",", "") if stars_el else "0"
                stars = int(stars_text) if stars_text.isdigit() else 0

                # Forks
                forks_el = article.query_selector("a[href*='/forks']")
                forks_text = forks_el.inner_text().strip().replace(",", "") if forks_el else "0"
                forks = int(forks_text) if forks_text.isdigit() else 0

                # Built by contributors
                contributors = []
                all_links = article.query_selector_all("a")
                for link in all_links:
                    text = link.inner_text().strip()
                    if text.startswith("@"):
                        contributors.append(text)

                # Period stars (e.g. "2,390 stars today")
                period_stars = ""
                all_text = article.inner_text()
                period_match = re.search(r'([\d,]+)\s+stars?\s+(today|this week|this month)', all_text)
                if period_match:
                    period_stars = f"+{period_match.group(1)} stars {period_match.group(2)}"

                results.append({
                    "name": name,
                    "url": repo_url,
                    "description": description,
                    "language": lang,
                    "stars": stars,
                    "forks": forks,
                    "built_by": contributors,
                    "period_stars": period_stars,
                })
            except Exception as e:
                print(f"   ⚠️  Error parsing article: {e}")
                continue

        print(f"   ✓ Extracted {len(results)} repositories")
        
        # Keep browser open briefly so user can see
        print("   Waiting 3 seconds before closing browser...")
        time.sleep(3)
        
        context.close()
        browser.close()
        print("   ✓ Browser closed")

    return {
        "success": True, 
        "data": results, 
        "count": len(results), 
        "source": "github_trending_page",
        "method": "browser_scraper",
        "page_url": f"https://github.com/trending?since={since}"
    }


if __name__ == "__main__":
    since = sys.argv[1] if len(sys.argv) > 1 else "daily"
    language = sys.argv[2] if len(sys.argv) > 2 else ""
    
    # Always use browser mode - no API fallback
    result = fetch_trending_via_browser(since, language)
    print(json.dumps(result, ensure_ascii=False, indent=2))
