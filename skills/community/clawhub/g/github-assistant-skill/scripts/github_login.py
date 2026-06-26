#!/usr/bin/env python3
"""
GitHub Login Manager
Supports two modes:
1. Browser login (interactive) - opens browser for manual login, supports operations via browser automation
2. Token login - user provides GitHub Personal Access Token for API operations

浏览器模式特点：
- 打开可视浏览器窗口让用户手动登录
- 登录后可保存 session 用于后续浏览器自动化操作
- 仓库操作(Star/Fork/Watch)可通过浏览器直接点击完成
- 无需提供 Personal Access Token
"""

import json
import os
import sys
import time

# Import centralized configuration
from config import (
    get_token_file,
    get_auth_state_file,
    get_browser_data_dir,
    save_token,
    has_token,
    has_browser_session,
    clear_credentials
)

# Global browser instance for persistent session
_browser_instance = None
_context_instance = None
_playwright_instance = None  # Keep playwright instance to prevent GC




def browser_login():
    """
    Launch browser for interactive GitHub login.
    The agent opens the browser, user logs in manually.
    After login, the browser storage state (cookies) is saved for future use.
    
    Features:
    - Check login status every 1 minute
    - Do NOT close browser window automatically
    - Prompt user to notify when login is complete
    - Use persistent context to avoid automation detection
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed.")
        print("Run: pip install playwright && playwright install chromium")
        return {"success": False, "error": "playwright not installed"}
    
    print("=" * 60)
    print("🌐 正在打开浏览器进行 GitHub 登录...")
    print("=" * 60)
    print()
    print("📋 登录步骤：")
    print("   1. 在弹出的浏览器窗口中输入您的 GitHub 账号和密码")
    print("   2. 完成登录后，GitHub 页面会自动跳转到首页")
    print("   3. 登录成功后，请在这里输入 'done' 或按 Enter 确认")
    print()
    print("⏱️  系统会每分钟自动检测一次登录状态")
    print("🖥️  浏览器窗口会一直保持打开，直到您确认登录完成")
    print("❌ 如需取消，请直接关闭浏览器窗口")
    print("=" * 60)
    print()
    
    # Use centralized browser data directory in user's home folder
    user_data_dir = get_browser_data_dir()
    
    with sync_playwright() as p:
        # Use persistent context to avoid automation detection
        # This creates a real browser profile that persists across sessions
        context = p.chromium.launch_persistent_context(
            user_data_dir,
            headless=False,
            # Hide automation flags
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-infobars',
                '--no-first-run',
                '--no-default-browser-check',
            ],
            # Set realistic viewport and user agent
            viewport={'width': 1280, 'height': 800},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            # Ignore HTTPS errors for corporate proxies
            ignore_https_errors=True,
        )
        page = context.new_page()
        
        page.goto("https://github.com/login", timeout=30000)
        
        print("✅ 浏览器已打开，请进行登录...")
        print()
        
        # Check login status every 30 seconds
        logged_in = False
        check_interval = 30  # seconds
        max_checks = 60  # 30 minutes max (60 * 30 = 1800 seconds)
        
        for check_count in range(max_checks):
            # Wait for check_interval seconds
            time.sleep(check_interval)
            
            # Check current URL to detect if login completed
            current_url = page.url
            print(f"⏱️  [{check_count + 1}/{max_checks}] 检测登录状态... 当前页面: {current_url}")
            
            # Check if user is logged in (not on login page)
            if "github.com/login" not in current_url and "github.com/session" not in current_url:
                # Additional check: look for user-specific elements
                try:
                    # Check for avatar or user menu which indicates logged in state
                    avatar = page.query_selector('img.avatar, [data-testid="user-avatar"], .Header-link[aria-label*="View profile"]')
                    if avatar or "/dashboard" in current_url or "/settings" in current_url or (current_url == "https://github.com/" or current_url == "https://github.com"):
                        logged_in = True
                        print()
                        print("🎉 检测到您已成功登录 GitHub！")
                        print(f"   当前页面: {current_url}")
                        break
                except:
                    pass
        
        if not logged_in:
            print()
            print("⚠️  等待超时或登录未完成")
            print("   浏览器窗口保持打开，您可以继续登录")
            print("   登录完成后请手动关闭浏览器")
            return {"success": False, "error": "Login not completed within time limit", "browser_open": True}
        
        # Ask user to confirm
        print()
        print("=" * 60)
        print("✅ 登录状态已确认！")
        print("=" * 60)
        print()
        print("💾 正在保存浏览器会话...")
        
        # Save storage state (cookies)
        auth_state_file = get_auth_state_file()
        context.storage_state(path=auth_state_file)
        print(f"   ✓ 会话已保存到: {auth_state_file}")
        
        # Try to extract username from page
        username = None
        try:
            # Try to get username from avatar alt text or profile link
            avatar = page.query_selector('img.avatar')
            if avatar:
                alt_text = avatar.get_attribute("alt") or ""
                if "@" in alt_text:
                    username = alt_text.replace("@", "").strip()
            
            # Alternative: check profile link
            if not username:
                profile_link = page.query_selector('a[href^="/"][data-testid="user-profile-link"], .Header-link[aria-label*="View profile"]')
                if profile_link:
                    href = profile_link.get_attribute("href") or ""
                    username = href.strip("/").split("/")[-1]
        except:
            pass
        
        print()
        print("📝 登录信息：")
        if username:
            print(f"   用户名: @{username}")
        print(f"   登录时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Keep browser open until user confirms
        print("🖥️  浏览器窗口保持打开")
        print("   您可以继续浏览或手动关闭")
        print("   按 Enter 键关闭浏览器并返回...")
        
        try:
            input()
        except KeyboardInterrupt:
            pass
        
        print("   正在关闭浏览器...")
        context.close()
        print("   ✓ 浏览器已关闭")
        
        print()
        print("=" * 60)
        print("🎉 GitHub 浏览器登录完成！")
        print("=" * 60)
        print()
        print("💡 提示：")
        print("   • 浏览器会话已保存，后续操作可直接使用")
        print("   • Star/Fork 操作可通过浏览器模式自动完成")
        print("   • 如需 Watch 功能，请使用 Token 登录")
        print()
        
        result = {
            "success": True,
            "method": "browser",
            "username": username,
            "message": "Browser login completed successfully."
        }
        if username:
            result["username"] = username
        
        return result


def token_login(token):
    """
    Verify and save a GitHub Personal Access Token.
    """
    import requests
    
    url = "https://api.github.com/user"
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {token}",
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            user = resp.json()
            save_token(token)
            return {
                "success": True,
                "method": "token",
                "username": user.get("login", ""),
                "name": user.get("name", ""),
                "avatar": user.get("avatar_url", ""),
                "message": f"Successfully authenticated as {user.get('login', 'unknown')}"
            }
        else:
            err = resp.json()
            return {
                "success": False,
                "error": f"Token verification failed: {err.get('message', resp.text)}"
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


def check_login():
    """Check if currently logged in"""
    if has_token():
        token_file = get_token_file()
        with open(token_file) as f:
            token = f.read().strip()
        if token:
            import requests
            resp = requests.get(
                "https://api.github.com/user",
                headers={"Authorization": f"token {token}"},
                timeout=15
            )
            if resp.status_code == 200:
                user = resp.json()
                return {
                    "logged_in": True,
                    "method": "token",
                    "username": user.get("login", ""),
                    "name": user.get("name", ""),
                }
    
    if has_browser_session():
        return {
            "logged_in": True,
            "method": "browser",
            "message": "Browser session exists (API operations require token)"
        }
    
    return {"logged_in": False, "message": "Not logged in"}


def get_browser_session():
    """
    Get or create a browser session for automation.
    Returns (browser, context) tuple or (None, None) if not available.
    
    Note: The browser window will stay open (visible, headless=False).
    The playwright instance is kept globally to prevent garbage collection
    which would otherwise close the browser unexpectedly.
    """
    global _browser_instance, _context_instance, _playwright_instance
    
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return None, None
    
    # If we already have an active session, return it
    if _browser_instance and _context_instance:
        return _browser_instance, _context_instance
    
    # Try to load saved session
    auth_state_file = get_auth_state_file()
    if not os.path.exists(auth_state_file):
        return None, None
    
    try:
        _playwright_instance = sync_playwright().start()  # Keep reference globally
        _browser_instance = _playwright_instance.chromium.launch(headless=False)  # Visible browser
        _context_instance = _browser_instance.new_context(storage_state=auth_state_file)
        
        print("🌐 浏览器会话已恢复（窗口保持打开）")
        return _browser_instance, _context_instance
    except Exception as e:
        print(f"Failed to restore browser session: {e}")
        return None, None


def close_browser_session():
    """Close the browser session and cleanup resources"""
    global _browser_instance, _context_instance, _playwright_instance
    
    if _context_instance:
        try:
            _context_instance.close()
        except:
            pass
        _context_instance = None
    if _browser_instance:
        try:
            _browser_instance.close()
        except:
            pass
        _browser_instance = None
    if _playwright_instance:
        try:
            _playwright_instance.stop()
        except:
            pass
        _playwright_instance = None
    print("✓ 浏览器会话已关闭")


def logout():
    """Remove stored credentials"""
    global _browser_instance, _context_instance
    
    # Use centralized clear_credentials function
    removed = clear_credentials()
    
    # Also close any active browser session
    close_browser_session()
    
    if removed:
        return {"success": True, "removed": removed}
    return {"success": True, "message": "No credentials to remove"}


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "check"
    
    if action == "browser":
        result = browser_login()
    elif action == "token":
        if len(sys.argv) < 3:
            print("Usage: python github_login.py token <your_github_token>")
            sys.exit(1)
        result = token_login(sys.argv[2])
    elif action == "check":
        result = check_login()
    elif action == "logout":
        result = logout()
    else:
        print(f"Unknown action: {action}")
        print("Usage: python github_login.py [browser|token|check|logout]")
        sys.exit(1)
    
    print(json.dumps(result, ensure_ascii=False, indent=2))
