#!/usr/bin/env python3
"""
One-click publish Markdown articles to Zhihu (知乎).

Automates login, article creation, and publishing on Zhihu.
Uses Playwright for browser-based login and requests for API calls.

Usage:
    python publish.py --login                              # Login and save cookies
    python publish.py input.md                             # Publish article
    python publish.py input.md --draft                     # Save as draft only
    python publish.py input.md --title "Custom Title"      # Custom title
    python publish.py input.md --topic "AI,编程"           # Set topics

Dependencies:
    pip install playwright requests
    playwright install chromium
"""

import argparse
import json
import re
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
COOKIE_FILE = SCRIPT_DIR / ".zhihu_cookies.json"

# Add scripts dir to path for importing convert
sys.path.insert(0, str(SCRIPT_DIR))


# ──────────────────────────────────────────────
# Cookie Management
# ──────────────────────────────────────────────

def save_cookies(cookies: list):
    """Save browser cookies to file."""
    COOKIE_FILE.write_text(json.dumps(cookies, ensure_ascii=False, indent=2), encoding="utf-8")
    _print(f"Cookie 已保存到: {COOKIE_FILE}")


def load_cookies() -> list | None:
    """Load cookies from file, return None if not found."""
    if COOKIE_FILE.exists():
        try:
            return json.loads(COOKIE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError):
            return None
    return None


def get_xsrf_token(cookies: list) -> str | None:
    """Extract _xsrf token from cookies."""
    for cookie in cookies:
        if cookie.get("name") == "_xsrf":
            return cookie.get("value")
    return None


def cookies_to_dict(cookies: list) -> dict:
    """Convert Playwright cookie list to requests-compatible dict."""
    return {c["name"]: c["value"] for c in cookies}


def cookies_to_header(cookies: list) -> str:
    """Convert Playwright cookie list to Cookie header string."""
    return "; ".join(f'{c["name"]}={c["value"]}' for c in cookies)


# ──────────────────────────────────────────────
# Login
# ──────────────────────────────────────────────

def _get_user_data_dir() -> Path:
    """Get persistent browser profile directory for Zhihu login."""
    profile_dir = SCRIPT_DIR / ".zhihu_browser_profile"
    profile_dir.mkdir(exist_ok=True)
    return profile_dir


def _find_real_browser() -> str | None:
    """Find the real Chrome or Edge executable on the system."""
    import shutil

    candidates = [
        # Chrome paths
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        str(Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "Application" / "chrome.exe"),
        # Edge paths (always available on Windows 10+)
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    ]
    for p in candidates:
        if Path(p).exists():
            return p

    # Try PATH
    for name in ("chrome", "google-chrome", "msedge"):
        found = shutil.which(name)
        if found:
            return found

    return None


def login():
    """Login to Zhihu using the real Chrome/Edge browser via CDP.

    Launches the real browser (not Playwright's Chromium) with a dedicated
    profile and remote debugging, then connects via CDP to capture cookies.
    This completely avoids automation detection.
    """
    import subprocess as sp

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        _print("错误: playwright 未安装。请运行: pip install playwright && playwright install chromium")
        sys.exit(1)

    browser_exe = _find_real_browser()
    if not browser_exe:
        _print("错误: 未找到 Chrome 或 Edge 浏览器，请确保已安装。")
        sys.exit(1)

    browser_name = "Chrome" if "chrome" in browser_exe.lower() else "Edge"
    _print(f"检测到 {browser_name}: {browser_exe}")
    _print(f"正在启动 {browser_name}（真实浏览器，非自动化引擎）...")

    debug_port = 9222
    user_data_dir = str(_get_user_data_dir())

    # Launch real browser with remote debugging and a dedicated profile
    chrome_proc = sp.Popen(
        [
            browser_exe,
            f"--remote-debugging-port={debug_port}",
            f"--user-data-dir={user_data_dir}",
            "--no-first-run",
            "--no-default-browser-check",
            "--start-maximized",
            "https://www.zhihu.com/signin",
        ],
        stdout=sp.DEVNULL,
        stderr=sp.DEVNULL,
    )

    # Wait for browser to fully start and open debug port
    _print("等待浏览器启动...")
    import socket
    for i in range(20):
        time.sleep(1)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("localhost", debug_port)) == 0:
                _print(f"调试端口已就绪 (等待 {i+1}s)")
                break
    else:
        _print(f"浏览器调试端口未能启动。")
        _print(f"可能原因：已有其他 {browser_name} 使用相同 profile 目录。")
        _print(f"请关闭所有 {browser_name} 窗口后重试。")
        chrome_proc.kill()
        return False

    time.sleep(2)  # Extra buffer for page load

    with sync_playwright() as p:
        browser = None
        # Retry connecting (browser may take a moment)
        for attempt in range(8):
            try:
                browser = p.chromium.connect_over_cdp(f"http://localhost:{debug_port}")
                break
            except Exception as e:
                _print(f"连接尝试 {attempt+1}/8: {e}")
                time.sleep(2)

        if not browser:
            _print(f"连接 {browser_name} 失败。请确保没有其他 {browser_name} 窗口使用相同配置，然后重试。")
            chrome_proc.kill()
            return False

        _print(f"已连接到 {browser_name}！")
        _print("=" * 50)
        _print("请在浏览器窗口中登录知乎")
        _print("支持扫码登录 / 手机验证码 / 账号密码")
        _print("登录成功后，脚本会自动检测并保存登录信息")
        _print("=" * 50)

        context = browser.contexts[0]

        # Poll for login success
        max_wait = 300  # 5 minutes
        start_time = time.time()

        while time.time() - start_time < max_wait:
            time.sleep(4)
            try:
                # Find the active page
                pages = context.pages
                if not pages:
                    continue
                page = pages[-1]
                current_url = page.url

                # Check if user has navigated past login/security pages
                if ("signin" not in current_url
                    and "sign-in" not in current_url
                    and "unhuman" not in current_url
                    and "zhihu.com" in current_url):
                    time.sleep(3)
                    cookies = context.cookies()
                    has_auth = any(c["name"] == "z_c0" for c in cookies)
                    if has_auth:
                        save_cookies(cookies)
                        _print("\n登录成功！Cookie 已保存。")
                        try:
                            browser.close()
                        except Exception:
                            pass
                        chrome_proc.terminate()
                        return True
            except Exception:
                pass

        _print("\n登录超时（5分钟），请重试。")
        try:
            browser.close()
        except Exception:
            pass
        chrome_proc.terminate()
        return False


# ──────────────────────────────────────────────
# API-based Publishing
# ──────────────────────────────────────────────

def verify_login(cookies: list) -> bool:
    """Check if saved cookies are still valid."""
    try:
        import requests
    except ImportError:
        _print("错误: requests 未安装。请运行: pip install requests")
        sys.exit(1)

    try:
        resp = requests.get(
            "https://www.zhihu.com/api/v4/me",
            headers={
                "Cookie": cookies_to_header(cookies),
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            },
            timeout=10,
        )
        if resp.status_code == 200:
            data = resp.json()
            name = data.get("name", "Unknown")
            _print(f"已登录: {name}")
            return True
    except Exception as e:
        _print(f"验证登录失败: {e}")

    return False


def create_draft(cookies: list, title: str, content: str) -> str | None:
    """Create a new article draft on Zhihu, return draft ID."""
    import requests

    xsrf = get_xsrf_token(cookies)
    headers = {
        "Cookie": cookies_to_header(cookies),
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://zhuanlan.zhihu.com/write",
        "Origin": "https://zhuanlan.zhihu.com",
    }
    if xsrf:
        headers["x-xsrftoken"] = xsrf

    # Step 1: Create empty draft
    resp = requests.post(
        "https://zhuanlan.zhihu.com/api/articles/drafts",
        headers=headers,
        json={"title": title, "delta_time": 0},
        timeout=15,
    )

    if resp.status_code not in (200, 201):
        _print(f"创建草稿失败: HTTP {resp.status_code}")
        _print(f"响应: {resp.text[:500]}")
        return None

    data = resp.json()
    draft_id = str(data.get("id", ""))
    if not draft_id:
        _print(f"创建草稿失败: 无法获取草稿ID")
        return None

    _print(f"草稿已创建: ID={draft_id}")

    # Step 2: Update draft with content
    resp2 = requests.patch(
        f"https://zhuanlan.zhihu.com/api/articles/{draft_id}/draft",
        headers=headers,
        json={
            "title": title,
            "content": content,
            "delta_time": 0,
        },
        timeout=15,
    )

    if resp2.status_code != 200:
        _print(f"更新草稿内容失败: HTTP {resp2.status_code}")
        _print(f"响应: {resp2.text[:500]}")
        return None

    _print(f"草稿内容已更新")
    return draft_id


def publish_draft(cookies: list, draft_id: str, topic_names: list[str] | None = None) -> str | None:
    """Publish a draft article on Zhihu, return article URL."""
    import requests

    xsrf = get_xsrf_token(cookies)
    headers = {
        "Cookie": cookies_to_header(cookies),
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": f"https://zhuanlan.zhihu.com/p/{draft_id}/edit",
        "Origin": "https://zhuanlan.zhihu.com",
    }
    if xsrf:
        headers["x-xsrftoken"] = xsrf

    # Resolve topic IDs if topic names provided
    topic_ids = []
    if topic_names:
        for name in topic_names:
            tid = search_topic(cookies, name.strip())
            if tid:
                topic_ids.append(tid)

    publish_data = {
        "column": None,
        "commentPermission": "anyone",
        "disclaimer_type": "none",
        "disclaimer_status": "close",
    }
    if topic_ids:
        publish_data["topic_ids"] = topic_ids

    resp = requests.put(
        f"https://zhuanlan.zhihu.com/api/articles/{draft_id}/publish",
        headers=headers,
        json=publish_data,
        timeout=15,
    )

    if resp.status_code != 200:
        _print(f"发布失败: HTTP {resp.status_code}")
        _print(f"响应: {resp.text[:500]}")
        return None

    article_url = f"https://zhuanlan.zhihu.com/p/{draft_id}"
    return article_url


def search_topic(cookies: list, keyword: str) -> str | None:
    """Search for a Zhihu topic and return its ID."""
    import requests

    try:
        resp = requests.get(
            "https://www.zhihu.com/api/v4/search/suggest",
            params={"q": keyword, "t": "topic"},
            headers={
                "Cookie": cookies_to_header(cookies),
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            },
            timeout=10,
        )
        if resp.status_code == 200:
            data = resp.json()
            suggest = data.get("suggest", [])
            for item in suggest:
                if item.get("type") == "topic":
                    return str(item.get("id", ""))
    except Exception:
        pass
    return None


# ──────────────────────────────────────────────
# Browser Fallback Publishing
# ──────────────────────────────────────────────

def publish_via_browser(md_path: Path, title: str, html_content: str, draft: bool = False):
    """Fallback: publish via real Chrome/Edge browser if API fails."""
    import subprocess as sp

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        _print("错误: playwright 未安装。请运行: pip install playwright && playwright install chromium")
        return False

    cookies = load_cookies()
    if not cookies:
        _print("未找到登录信息，请先运行 --login")
        return False

    browser_exe = _find_real_browser()
    if not browser_exe:
        _print("错误: 未找到 Chrome 或 Edge 浏览器")
        return False

    _print("正在通过真实浏览器发布...")

    debug_port = 9223  # Different port to avoid conflict
    user_data_dir = str(_get_user_data_dir())

    chrome_proc = sp.Popen([
        browser_exe,
        f"--remote-debugging-port={debug_port}",
        f"--user-data-dir={user_data_dir}",
        "--no-first-run",
        "--no-default-browser-check",
        "https://zhuanlan.zhihu.com/write",
    ])

    time.sleep(5)

    with sync_playwright() as p:
        browser = None
        for attempt in range(5):
            try:
                browser = p.chromium.connect_over_cdp(f"http://localhost:{debug_port}")
                break
            except Exception:
                time.sleep(2)

        if not browser:
            _print("连接浏览器失败")
            chrome_proc.kill()
            return False

        context = browser.contexts[0]

        # Inject saved cookies
        if cookies:
            try:
                context.add_cookies(cookies)
            except Exception:
                pass

        pages = context.pages
        page = pages[-1] if pages else context.new_page()

        # Reload the write page with cookies
        page.goto("https://zhuanlan.zhihu.com/write", wait_until="domcontentloaded")
        time.sleep(4)

        # Check if redirected to login
        if "signin" in page.url or "sign-in" in page.url or "unhuman" in page.url:
            _print("Cookie 已过期，请重新运行 --login 登录")
            try:
                browser.close()
            except Exception:
                pass
            chrome_proc.terminate()
            return False

        # Input title
        try:
            title_el = page.locator('textarea').first
            title_el.fill(title)
            time.sleep(0.5)
        except Exception as e:
            _print(f"设置标题失败: {e}")

        # Inject content into editor via JS
        try:
            page.evaluate("""
                (html) => {
                    const editor = document.querySelector('.public-DraftEditor-content, .ProseMirror, [contenteditable="true"]');
                    if (editor) {
                        editor.focus();
                        // Use insertHTML command
                        document.execCommand('selectAll', false, null);
                        document.execCommand('insertHTML', false, html);
                    }
                }
            """, html_content)
            time.sleep(2)
        except Exception as e:
            _print(f"注入内容失败: {e}")
            _print("请手动将内容粘贴到编辑器中")

        if not draft:
            try:
                publish_btn = page.locator('button:has-text("发布")').first
                publish_btn.click()
                time.sleep(3)

                # Try to confirm publish in dialog
                confirm_btn = page.locator('button:has-text("确认并发布"), button:has-text("确认发布")').first
                if confirm_btn.is_visible():
                    confirm_btn.click()
                    time.sleep(3)
                    _print("文章已发布！")
            except Exception as e:
                _print(f"自动点击发布按钮失败: {e}")
                _print("请在浏览器中手动点击发布")
                input("按 Enter 键继续...")
        else:
            _print("文章已保存为草稿")
            input("请在浏览器中检查后按 Enter 键继续...")

        # Save updated cookies
        try:
            new_cookies = context.cookies()
            save_cookies(new_cookies)
        except Exception:
            pass

        try:
            browser.close()
        except Exception:
            pass
        chrome_proc.terminate()
        return True


# ──────────────────────────────────────────────
# Main Publish Flow
# ──────────────────────────────────────────────

def extract_title(md_text: str) -> str:
    """Extract title from first h1 heading."""
    match = re.match(r"^#\s+(.+)", md_text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    for line in md_text.split("\n"):
        line = line.strip()
        if line:
            return line[:100]
    return "Untitled"


def _ensure_login() -> list:
    """Ensure we have valid cookies, login if needed. Returns cookie list."""
    cookies = load_cookies()
    if not cookies:
        _print("未找到登录信息，正在启动登录流程...")
        if not login():
            sys.exit(1)
        cookies = load_cookies()

    if not verify_login(cookies):
        _print("Cookie 已过期，正在重新登录...")
        if not login():
            sys.exit(1)
        cookies = load_cookies()

    return cookies


def publish_article(
    md_file: str,
    title: str | None = None,
    draft: bool = False,
    topics: list[str] | None = None,
) -> bool:
    """Main publish flow: convert markdown and publish to Zhihu. Returns True on success."""
    md_path = Path(md_file)
    if not md_path.exists():
        _print(f"错误: 文件不存在: {md_path}")
        return False

    md_content = md_path.read_text(encoding="utf-8")

    # Extract title
    if not title:
        title = extract_title(md_content)
    _print(f"文章标题: {title}")

    # Convert markdown to Zhihu HTML
    try:
        from convert import convert_to_zhihu_content
        html_content = convert_to_zhihu_content(md_content)
    except ImportError:
        _print("错误: 无法导入 convert 模块，请确认 convert.py 存在")
        return False

    cookies = _ensure_login()

    # Try API-based publishing first
    _print("正在通过 API 发布...")
    try:
        import requests
        draft_id = create_draft(cookies, title, html_content)
        if draft_id:
            if draft:
                _print(f"文章已保存为草稿！")
                _print(f"编辑链接: https://zhuanlan.zhihu.com/p/{draft_id}/edit")
                return True
            else:
                url = publish_draft(cookies, draft_id, topics)
                if url:
                    _print(f"文章发布成功！")
                    _print(f"文章链接: {url}")
                    return True
                else:
                    _print("API 发布失败，尝试浏览器方式...")
    except ImportError:
        _print("requests 未安装，使用浏览器方式发布...")
    except Exception as e:
        _print(f"API 发布出错: {e}")
        _print("尝试浏览器方式发布...")

    # Fallback to browser-based publishing
    return publish_via_browser(md_path, title, html_content, draft)


def batch_publish(
    dir_path: str,
    draft: bool = False,
    topics: list[str] | None = None,
    delay: int = 60,
):
    """Batch publish all .md files in a directory to Zhihu.

    Args:
        dir_path: Directory containing .md files
        draft: If True, save as drafts instead of publishing
        topics: Optional topic tags for all articles
        delay: Seconds to wait between publishes (default 60s to avoid rate limiting)
    """
    folder = Path(dir_path)
    if not folder.is_dir():
        _print(f"错误: 目录不存在: {folder}")
        sys.exit(1)

    md_files = sorted(folder.glob("*.md"))
    if not md_files:
        _print(f"目录下没有找到 .md 文件: {folder}")
        sys.exit(1)

    total = len(md_files)
    _print(f"=" * 50)
    _print(f"批量发布: 找到 {total} 篇 Markdown 文章")
    _print(f"模式: {'保存草稿' if draft else '直接发布'}")
    if topics:
        _print(f"话题: {', '.join(topics)}")
    _print(f"发布间隔: {delay}s")
    _print(f"=" * 50)

    # Verify login once before batch
    _ensure_login()

    success_list = []
    fail_list = []

    for idx, md_file in enumerate(md_files, 1):
        _print(f"\n[{idx}/{total}] {md_file.name}")
        _print("-" * 40)

        try:
            ok = publish_article(str(md_file), title=None, draft=draft, topics=topics)
            if ok:
                success_list.append(md_file.name)
            else:
                fail_list.append(md_file.name)
        except Exception as e:
            _print(f"发布出错: {e}")
            fail_list.append(md_file.name)

        # Delay between publishes to avoid rate limiting (skip after last)
        if idx < total:
            _print(f"等待 {delay}s 后继续...")
            time.sleep(delay)

    # Summary
    _print(f"\n{'=' * 50}")
    _print(f"批量发布完成!")
    _print(f"  成功: {len(success_list)}")
    _print(f"  失败: {len(fail_list)}")
    _print(f"  共计: {total}")
    if fail_list:
        _print(f"\n失败文件:")
        for name in fail_list:
            _print(f"  - {name}")


# ──────────────────────────────────────────────
# Utilities
# ──────────────────────────────────────────────

def _print(msg: str):
    """Print with UTF-8 encoding for Windows compatibility."""
    import io
    try:
        out = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
        out.write(msg + "\n")
        out.flush()
        # Detach to avoid closing stdout
        out.detach()
    except Exception:
        print(msg)


# ──────────────────────────────────────────────
# CLI Entry Point
# ──────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="一键发布 Markdown 文章到知乎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python publish.py --login                             # 登录知乎
  python publish.py article.md                          # 发布单篇文章
  python publish.py article.md --draft                  # 保存草稿
  python publish.py article.md --title "标题"           # 指定标题
  python publish.py article.md --topic "AI,编程"        # 设置话题
  python publish.py --dir ./articles                    # 批量发布目录下所有 .md
  python publish.py --dir ./articles --draft            # 批量保存为草稿
  python publish.py --dir ./articles --delay 30         # 批量发布，间隔 30s
        """,
    )
    parser.add_argument("input", nargs="?", help="输入 Markdown 文件路径")
    parser.add_argument("--login", action="store_true", help="登录知乎并保存 Cookie")
    parser.add_argument("--title", help="文章标题 (默认从 Markdown 第一个 h1 提取)")
    parser.add_argument("--draft", action="store_true", help="仅保存为草稿")
    parser.add_argument("--topic", help="文章话题，逗号分隔 (如: 'AI,编程,技术')")
    parser.add_argument("--dir", help="批量发布：指定目录路径，发布该目录下所有 .md 文件")
    parser.add_argument("--delay", type=int, default=60, help="批量发布时每篇文章间隔秒数 (默认: 60，即1分钟，避免被限流)")

    args = parser.parse_args()

    if args.login:
        success = login()
        sys.exit(0 if success else 1)

    topics = [t.strip() for t in args.topic.split(",")] if args.topic else None

    # Batch mode
    if args.dir:
        batch_publish(args.dir, args.draft, topics, args.delay)
        sys.exit(0)

    # Single file mode
    if not args.input:
        parser.print_help()
        sys.exit(0)

    publish_article(args.input, args.title, args.draft, topics)


if __name__ == "__main__":
    main()
