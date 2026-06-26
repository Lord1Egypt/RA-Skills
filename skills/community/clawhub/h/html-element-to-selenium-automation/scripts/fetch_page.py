#!/usr/bin/env python3
"""
fetch_page.py - 使用 Playwright 获取页面截图 + HTML DOM

用法:
    python fetch_page.py <url> [--output <目录>] [--wait <秒>] [--login] [--username <用户名>] [--password <密码>]

输出:
    <output>/screenshot.png       - 完整页面截图
    <output>/html.html            - 渲染后的完整 HTML DOM
    <output>/meta.json            - 页面元信息 (URL, title, 元素计数等)
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("[ERROR] playwright 未安装. 请运行: pip install playwright && playwright install")
    sys.exit(1)


def get_creds_from_env():
    """从环境变量读取凭据（优先级：显式参数 > 环境变量）."""
    return (
        os.environ.get("ROUTER_USERNAME") or os.environ.get("ROUTER_USER"),
        os.environ.get("ROUTER_PASSWORD") or os.environ.get("ROUTER_PASS"),
    )


def is_login_page(page) -> bool:
    """通过 DOM 特征判断当前页面是否为登录页."""
    indicators = [
        'input[type="password"]',
        'input[name*="password" i]',
        'input[name*="passwd" i]',
        '[placeholder*="password" i]',
        '[placeholder*="密码" i]',
        '[id*="password" i]',
        '[class*="password" i]',
        'form[action*="login" i]',
        'form[action*="signin" i]',
        'form[action*="auth" i]',
        '[class*="login" i][class*="form" i]',
        '[id*="login" i][id*="form" i]',
    ]
    for sel in indicators:
        try:
            if page.query_selector(sel):
                return True
        except Exception:
            pass
    return False


def login_if_needed(page, url: str, username: str = None, password: str = None) -> bool:
    """
    检测是否需要登录并尝试登录. 返回是否进行了登录.
    凭据优先用传入参数, 其次尝试从环境变量读取.
    """
    if not is_login_page(page):
        return False

    # 如果是目标登录页且用户未提供凭据, 不自动登录
    if not username or not password:
        print("[INFO] 检测到登录页但未提供凭据, 跳过自动登录")
        return False

    print(f"[INFO] 检测到登录页, 尝试登录用户: {username}")

    # 通用登录字段选择器
    USERNAME_SELECTORS = [
        'input[name="username"]', 'input[name="user"]', 'input[name="email"]',
        'input[name="login"]', 'input[type="email"]', 'input[id*="username"]',
        'input[id*="user"]', 'input[id*="email"]', 'input[placeholder*="用户名"]',
        'input[placeholder*="邮箱"]', 'input[placeholder*="email" i]',
    ]
    PASSWORD_SELECTORS = [
        'input[name="password"]', 'input[type="password"]', 'input[id*="password"]',
        'input[placeholder*="密码"]', 'input[placeholder*="password" i]',
    ]
    SUBMIT_SELECTORS = [
        'button[type="submit"]', 'input[type="submit"]',
        'button:has-text("登录")', 'button:has-text("登录" i)',
        'button:has-text("Sign in")', 'button:has-text("登 录")',
        '[class*="login" i][type="submit"]',
    ]

    # 填充用户名
    filled_user = False
    for sel in USERNAME_SELECTORS:
        try:
            el = page.wait_for_selector(sel, timeout=3000)
            el.click(click_count=3)
            el.fill(username)
            filled_user = True
            print(f"[OK] 已填入用户名 (selector: {sel})")
            break
        except Exception:
            continue

    if not filled_user:
        print("[WARN] 未找到用户名输入框")

    # 填充密码
    filled_pass = False
    for sel in PASSWORD_SELECTORS:
        try:
            el = page.wait_for_selector(sel, timeout=3000)
            el.fill(password)
            filled_pass = True
            print(f"[OK] 已填入密码 (selector: {sel})")
            break
        except Exception:
            continue

    if not filled_pass:
        print("[WARN] 未找到密码输入框")

    # 点击登录按钮
    if filled_user and filled_pass:
        for sel in SUBMIT_SELECTORS:
            try:
                btn = page.wait_for_selector(sel, timeout=3000)
                btn.click()
                print(f"[OK] 已点击登录按钮 (selector: {sel})")
                time.sleep(2)
                break
            except Exception:
                continue

        # 检查是否还停留在登录页
        if is_login_page(page):
            print("[WARN] 登录可能失败, 仍停留在登录页")
            return False

        print("[OK] 登录成功")
        return True

    return False


def fetch_page(
    url: str,
    output_dir: str = ".",
    wait: int = 3,
    do_login: bool = False,
    username: str = None,
    password: str = None,
) -> dict:
    """抓取页面并保存截图 + HTML + 元信息."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    result = {
        "url": url,
        "screenshot": str(output_path / "screenshot.png"),
        "html_file": str(output_path / "html.html"),
        "meta_file": str(output_path / "meta.json"),
        "page_type": "unknown",
        "login_performed": False,
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
        )
        page = context.new_page()

        initial_url = url
        page.goto(url, wait_until="networkidle", timeout=30000)
        time.sleep(wait)

        result["final_url"] = page.url
        result["title"] = page.title()

        # AI 判断页面类型 (自动化检测: 仅用于辅助提示)
        if is_login_page(page):
            result["page_type"] = "login_required"
        else:
            result["page_type"] = "public"

        # 如需要登录，且未提供凭据，尝试从环境变量读取
        if do_login and result["page_type"] == "login_required":
            if not username or not password:
                env_user, env_pass = get_creds_from_env()
                username = username or env_user
                password = password or env_pass
            result["login_performed"] = login_if_needed(
                page, url, username, password
            )
            if result["login_performed"]:
                # 等待页面稳定
                time.sleep(wait)
                result["final_url"] = page.url
                result["title"] = page.title()
                # 重新判断
                if is_login_page(page):
                    result["page_type"] = "login_required"
                else:
                    result["page_type"] = "authenticated"

        # 截图 (全页)
        page.screenshot(path=str(output_path / "screenshot.png"), full_page=True)
        print(f"[OK] 截图已保存: {output_path / 'screenshot.png'}")

        # 截图 (仅视口)
        page.screenshot(path=str(output_path / "screenshot_viewport.png"), full_page=False)
        print(f"[OK] 视口截图已保存: {output_path / 'screenshot_viewport.png'}")

        # 完整 DOM (渲染后)
        html_content = page.content()
        with open(output_path / "html.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[OK] HTML 已保存: {output_path / 'html.html'}")

        # 元素统计
        selectors = {
            "form": "form",
            "input": "input",
            "button": "button",
            "a": "a",
            "table": "table",
            "select": "select",
            "textarea": "textarea",
            "iframe": "iframe",
            "img": "img",
            "script": "script",
            "link": "link",
        }
        element_counts = {}
        for name, sel in selectors.items():
            try:
                element_counts[name] = len(page.query_selector_all(sel))
            except Exception:
                element_counts[name] = 0

        result["elements"] = element_counts

        # meta.json
        meta = {
            "url": result["url"],
            "final_url": result["final_url"],
            "title": result["title"],
            "page_type": result["page_type"],
            "login_performed": result["login_performed"],
            "elements": element_counts,
        }
        with open(output_path / "meta.json", "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
        print(f"[OK] 元信息已保存: {output_path / 'meta.json'}")

        browser.close()

    return result


def main():
    parser = argparse.ArgumentParser(description="使用 Playwright 获取页面截图 + HTML")
    parser.add_argument("url", help="目标 URL")
    parser.add_argument("--output", "-o", default=".", help="输出目录 (默认当前目录)")
    parser.add_argument("--wait", "-w", type=int, default=3, help="加载后等待秒数 (默认 3)")
    parser.add_argument("--login", "-l", action="store_true", help="检测到登录页时自动登录")
    parser.add_argument("--username", "-u", default=None, help="登录用户名")
    parser.add_argument("--password", "-p", default=None, help="登录密码")
    args = parser.parse_args()

    result = fetch_page(
        url=args.url,
        output_dir=args.output,
        wait=args.wait,
        do_login=args.login,
        username=args.username,
        password=args.password,
    )

    print("\n=== 抓取结果摘要 ===")
    print(f"  原始 URL:  {result['url']}")
    print(f"  最终 URL:  {result['final_url']}")
    print(f"  页面标题:  {result['title']}")
    print(f"  页面类型:  {result['page_type']}")
    print(f"  登录操作:  {'是' if result['login_performed'] else '否'}")
    print(f"  元素统计:  {result['elements']}")


if __name__ == "__main__":
    main()
