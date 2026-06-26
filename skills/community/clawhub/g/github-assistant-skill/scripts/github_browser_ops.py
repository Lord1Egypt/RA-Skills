#!/usr/bin/env python3
"""
GitHub Browser Operations - 浏览器自动化操作工具

用于处理 GitHub REST API 不支持的操作，例如：
- 查看用户贡献图 (Contribution Graph)
- 查看 Insights / Traffic / Pulse
- 查看用户活动时间线
- 浏览 GitHub Explore
- 查看项目依赖图
- 查看安全告警详情
- 操作 GitHub 设置页面
- 查看用户组织权限详情
- 浏览 GitHub Marketplace
- 查看项目 Projects / Wiki
- 等等...

特点：
- 操作过程可见（headless=False）
- 操作结束后浏览器保持打开，用户可继续手动操作
- 支持已登录的浏览器会话
"""

import json
import sys
import os
import time
import argparse

# Import centralized configuration
from config import (
    get_auth_state_file,
    get_browser_data_dir,
    has_browser_session,
    has_token
)


# Global browser instance - kept open for user interaction
_browser_instance = None
_context_instance = None
_playwright_instance = None
_page_instance = None


def _ensure_browser():
    """
    Ensure browser is launched and ready.
    Returns (browser, context, page, playwright) tuple.
    Browser stays open until explicitly closed.
    """
    global _browser_instance, _context_instance, _playwright_instance, _page_instance
    
    if _browser_instance and _context_instance and _page_instance:
        return _browser_instance, _context_instance, _page_instance, _playwright_instance
    
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("ERROR: playwright not installed.")
        print("Run: pip install playwright && playwright install chromium")
        return None, None, None, None
    
    _playwright_instance = sync_playwright().start()
    
    # Use persistent context for session persistence
    user_data_dir = get_browser_data_dir()
    
    # Check for existing browser session (storage_state file)
    auth_file = get_auth_state_file()
    
    # Launch browser with persistent context
    # Note: launch_persistent_context doesn't support storage_state parameter
    # The user_data_dir already provides persistence
    launch_options = {
        "headless": False,  # Always visible
        "args": [
            '--disable-blink-features=AutomationControlled',
            '--disable-infobars',
            '--no-first-run',
            '--no-default-browser-check',
        ],
        "viewport": {'width': 1280, 'height': 800},
        "user_agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        "ignore_https_errors": True,
    }
    
    # If storage_state exists, we need to use regular launch + new_context
    # because launch_persistent_context doesn't support storage_state
    if os.path.exists(auth_file):
        # Use regular browser with storage_state
        _browser_instance = _playwright_instance.chromium.launch(**launch_options)
        _context_instance = _browser_instance.new_context(storage_state=auth_file)
    else:
        # Use persistent context (stores cookies/session in user_data_dir)
        _context_instance = _playwright_instance.chromium.launch_persistent_context(
            user_data_dir,
            **launch_options
        )
        _browser_instance = _context_instance  # For persistent context, context is the browser
    
    # Get or create page
    pages = _context_instance.pages
    if pages:
        _page_instance = pages[0]
    else:
        _page_instance = _context_instance.new_page()
    
    return _browser_instance, _context_instance, _page_instance, _playwright_instance


def _get_page():
    """Get current page or create new one"""
    browser, context, page, p = _ensure_browser()
    if not page:
        return None
    return page


def close_browser():
    """
    Explicitly close the browser.
    Call this when user wants to end the session.
    """
    global _browser_instance, _context_instance, _playwright_instance, _page_instance
    
    if not _context_instance and not _playwright_instance:
        print("ℹ️  没有运行中的浏览器")
        return
    
    if _context_instance:
        try:
            _context_instance.close()
            print("✅ 浏览器已关闭")
        except Exception as e:
            print(f"⚠️  关闭浏览器时出错: {e}")
    
    if _playwright_instance:
        try:
            _playwright_instance.stop()
        except:
            pass
    
    _browser_instance = None
    _context_instance = None
    _playwright_instance = None
    _page_instance = None


def keep_browser_open(message="浏览器保持打开，您可以继续手动操作。"):
    """
    Keep browser open and inform user.
    Browser will stay open until user closes it or calls close_browser().
    """
    print(f"\n💡 {message}")
    print("   浏览器将保持打开状态，您可以继续手动操作。")
    print("   如需关闭浏览器，请运行: python3 github_browser_ops.py close")
    print()


# ==================== 浏览器操作函数 ====================

def navigate_to(url, description=None):
    """
    Navigate to a specific URL.
    
    Args:
        url: Target URL
        description: Optional description of the page
    
    Returns:
        dict with success status and current URL
    """
    page = _get_page()
    if not page:
        return {"success": False, "error": "无法启动浏览器"}
    
    try:
        print(f"🌐 正在导航到: {url}")
        if description:
            print(f"   📋 {description}")
        
        page.goto(url, timeout=60000, wait_until="domcontentloaded")
        
        # Wait a moment for page to stabilize
        time.sleep(1)
        
        current_url = page.url
        print(f"✅ 页面加载完成: {current_url}")
        
        return {
            "success": True,
            "url": current_url,
            "title": page.title()
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def view_user_profile(username):
    """
    View a user's profile page.
    
    Args:
        username: GitHub username
    """
    url = f"https://github.com/{username}"
    result = navigate_to(url, f"查看用户 @{username} 的个人资料")
    if result["success"]:
        keep_browser_open(f"已打开 @{username} 的个人资料页面")
    return result


def view_contributions(username):
    """
    View a user's contribution graph (not available via API).
    
    Args:
        username: GitHub username
    """
    url = f"https://github.com/{username}"
    result = navigate_to(url, f"查看 @{username} 的贡献图")
    
    if result["success"]:
        print("\n📊 贡献图信息：")
        print("   - 贡献图显示在用户主页")
        print("   - 绿色方块表示当天的提交数量")
        print("   - 可悬停查看具体日期和提交数")
        keep_browser_open("已打开贡献图页面")
    
    return result


def view_user_activity(username):
    """
    View a user's activity feed (not fully available via API).
    
    Args:
        username: GitHub username
    """
    url = f"https://github.com/{username}?tab=overview"
    result = navigate_to(url, f"查看 @{username} 的活动概览")
    
    if result["success"]:
        keep_browser_open("已打开用户活动概览页面")
    
    return result


def view_repo_insights(owner, repo):
    """
    View repository insights (Traffic, Pulse, etc. - requires push access).
    
    Args:
        owner: Repository owner
        repo: Repository name
    """
    url = f"https://github.com/{owner}/{repo}/pulse"
    result = navigate_to(url, f"查看 {owner}/{repo} 的 Pulse 概览")
    
    if result["success"]:
        print("\n📈 Insights 导航：")
        print(f"   - Pulse: https://github.com/{owner}/{repo}/pulse")
        print(f"   - Traffic: https://github.com/{owner}/{repo}/graphs/traffic")
        print(f"   - Contributors: https://github.com/{owner}/{repo}/graphs/contributors")
        print(f"   - Commit activity: https://github.com/{owner}/{repo}/graphs/commit-activity")
        keep_browser_open("已打开仓库 Insights 页面")
    
    return result


def view_repo_traffic(owner, repo):
    """
    View repository traffic (requires push access).
    
    Args:
        owner: Repository owner
        repo: Repository name
    """
    url = f"https://github.com/{owner}/{repo}/graphs/traffic"
    result = navigate_to(url, f"查看 {owner}/{repo} 的流量统计")
    
    if result["success"]:
        keep_browser_open("已打开仓库流量统计页面")
    
    return result


def view_repo_network(owner, repo):
    """
    View repository network graph (fork network).
    
    Args:
        owner: Repository owner
        repo: Repository name
    """
    url = f"https://github.com/{owner}/{repo}/network"
    result = navigate_to(url, f"查看 {owner}/{repo} 的 Fork 网络")
    
    if result["success"]:
        keep_browser_open("已打开仓库网络图页面")
    
    return result


def view_repo_dependents(owner, repo):
    """
    View repository dependents (who depends on this repo).
    
    Args:
        owner: Repository owner
        repo: Repository name
    """
    url = f"https://github.com/{owner}/{repo}/network/dependents"
    result = navigate_to(url, f"查看 {owner}/{repo} 的依赖者")
    
    if result["success"]:
        keep_browser_open("已打开仓库依赖者页面")
    
    return result


def view_repo_security(owner, repo):
    """
    View repository security advisories and alerts.
    
    Args:
        owner: Repository owner
        repo: Repository name
    """
    url = f"https://github.com/{owner}/{repo}/security"
    result = navigate_to(url, f"查看 {owner}/{repo} 的安全信息")
    
    if result["success"]:
        keep_browser_open("已打开仓库安全页面")
    
    return result


def view_repo_settings(owner, repo):
    """
    View repository settings (requires admin access).
    
    Args:
        owner: Repository owner
        repo: Repository name
    """
    url = f"https://github.com/{owner}/{repo}/settings"
    result = navigate_to(url, f"查看 {owner}/{repo} 的设置")
    
    if result["success"]:
        keep_browser_open("已打开仓库设置页面")
    
    return result


def view_user_settings():
    """
    View user settings page.
    """
    url = "https://github.com/settings/profile"
    result = navigate_to(url, "查看用户设置")
    
    if result["success"]:
        print("\n⚙️ 设置导航：")
        print("   - Profile: https://github.com/settings/profile")
        print("   - Account: https://github.com/settings/admin")
        print("   - Emails: https://github.com/settings/emails")
        print("   - Notifications: https://github.com/settings/notifications")
        print("   - Billing: https://github.com/settings/billing")
        print("   - Security: https://github.com/settings/security")
        print("   - Keys: https://github.com/settings/keys")
        print("   - Tokens: https://github.com/settings/tokens")
        keep_browser_open("已打开用户设置页面")
    
    return result


def view_user_organizations():
    """
    View user's organizations page.
    """
    url = "https://github.com/settings/organizations"
    result = navigate_to(url, "查看用户组织")
    
    if result["success"]:
        keep_browser_open("已打开组织页面")
    
    return result


def view_notifications():
    """
    View notifications page with full UI.
    """
    url = "https://github.com/notifications"
    result = navigate_to(url, "查看通知页面")
    
    if result["success"]:
        keep_browser_open("已打开通知页面")
    
    return result


def view_explore():
    """
    View GitHub Explore page.
    """
    url = "https://github.com/explore"
    result = navigate_to(url, "浏览 GitHub Explore")
    
    if result["success"]:
        keep_browser_open("已打开 GitHub Explore 页面")
    
    return result


def view_marketplace():
    """
    View GitHub Marketplace.
    """
    url = "https://github.com/marketplace"
    result = navigate_to(url, "浏览 GitHub Marketplace")
    
    if result["success"]:
        keep_browser_open("已打开 GitHub Marketplace 页面")
    
    return result


def view_repo_projects(owner, repo):
    """
    View repository projects (if any).
    
    Args:
        owner: Repository owner
        repo: Repository name
    """
    url = f"https://github.com/{owner}/{repo}/projects"
    result = navigate_to(url, f"查看 {owner}/{repo} 的 Projects")
    
    if result["success"]:
        keep_browser_open("已打开仓库 Projects 页面")
    
    return result


def view_repo_wiki(owner, repo):
    """
    View repository wiki (if any).
    
    Args:
        owner: Repository owner
        repo: Repository name
    """
    url = f"https://github.com/{owner}/{repo}/wiki"
    result = navigate_to(url, f"查看 {owner}/{repo} 的 Wiki")
    
    if result["success"]:
        keep_browser_open("已打开仓库 Wiki 页面")
    
    return result


def view_discussions(owner, repo=None):
    """
    View GitHub Discussions.
    
    Args:
        owner: Repository owner or organization name
        repo: Optional repository name
    """
    if repo:
        url = f"https://github.com/{owner}/{repo}/discussions"
        desc = f"查看 {owner}/{repo} 的 Discussions"
    else:
        url = f"https://github.com/orgs/{owner}/discussions"
        desc = f"查看组织 {owner} 的 Discussions"
    
    result = navigate_to(url, desc)
    
    if result["success"]:
        keep_browser_open("已打开 Discussions 页面")
    
    return result


def view_sponsors(username):
    """
    View GitHub Sponsors page for a user.
    
    Args:
        username: GitHub username
    """
    url = f"https://github.com/sponsors/{username}"
    result = navigate_to(url, f"查看 @{username} 的赞助页面")
    
    if result["success"]:
        keep_browser_open("已打开赞助页面")
    
    return result


def view_user_stars(username):
    """
    View user's starred repositories page.
    
    Args:
        username: GitHub username
    """
    url = f"https://github.com/{username}?tab=stars"
    result = navigate_to(url, f"查看 @{username} 的 Star 列表")
    
    if result["success"]:
        keep_browser_open("已打开 Star 列表页面")
    
    return result


def view_user_followers(username):
    """
    View user's followers page.
    
    Args:
        username: GitHub username
    """
    url = f"https://github.com/{username}?tab=followers"
    result = navigate_to(url, f"查看 @{username} 的粉丝列表")
    
    if result["success"]:
        keep_browser_open("已打开粉丝列表页面")
    
    return result


def view_user_following(username):
    """
    View user's following page.
    
    Args:
        username: GitHub username
    """
    url = f"https://github.com/{username}?tab=following"
    result = navigate_to(url, f"查看 @{username} 的关注列表")
    
    if result["success"]:
        keep_browser_open("已打开关注列表页面")
    
    return result


def search_on_github(query, type="repositories"):
    """
    Open GitHub search in browser.
    
    Args:
        query: Search query
        type: Type of search (repositories, users, issues, code, etc.)
    """
    url = f"https://github.com/search?q={query}&type={type}"
    result = navigate_to(url, f"在 GitHub 上搜索: {query}")
    
    if result["success"]:
        keep_browser_open("已打开搜索结果页面")
    
    return result


def view_gist(gist_id=None, username=None):
    """
    View Gist page.
    
    Args:
        gist_id: Optional specific gist ID
        username: Optional username to view their gists
    """
    if gist_id:
        url = f"https://gist.github.com/{gist_id}"
        desc = f"查看 Gist: {gist_id}"
    elif username:
        url = f"https://gist.github.com/{username}"
        desc = f"查看 @{username} 的 Gists"
    else:
        url = "https://gist.github.com/"
        desc = "浏览 Gists"
    
    result = navigate_to(url, desc)
    
    if result["success"]:
        keep_browser_open("已打开 Gist 页面")
    
    return result


def view_actions_workflows(owner, repo):
    """
    View repository Actions workflows in browser.
    
    Args:
        owner: Repository owner
        repo: Repository name
    """
    url = f"https://github.com/{owner}/{repo}/actions"
    result = navigate_to(url, f"查看 {owner}/{repo} 的 Actions")
    
    if result["success"]:
        keep_browser_open("已打开 Actions 页面")
    
    return result


def view_code_search(owner, repo, query):
    """
    Search code within a repository using GitHub's code search UI.
    
    Args:
        owner: Repository owner
        repo: Repository name
        query: Search query
    """
    url = f"https://github.com/{owner}/{repo}/search?q={query}"
    result = navigate_to(url, f"在 {owner}/{repo} 中搜索代码: {query}")
    
    if result["success"]:
        keep_browser_open("已打开代码搜索结果页面")
    
    return result


def view_commit(owner, repo, commit_sha):
    """
    View a specific commit in browser.
    
    Args:
        owner: Repository owner
        repo: Repository name
        commit_sha: Commit SHA
    """
    url = f"https://github.com/{owner}/{repo}/commit/{commit_sha}"
    result = navigate_to(url, f"查看提交 {commit_sha[:7]}")
    
    if result["success"]:
        keep_browser_open("已打开提交详情页面")
    
    return result


def view_compare(owner, repo, base, head):
    """
    View commit comparison in browser.
    
    Args:
        owner: Repository owner
        repo: Repository name
        base: Base branch/commit
        head: Head branch/commit
    """
    url = f"https://github.com/{owner}/{repo}/compare/{base}...{head}"
    result = navigate_to(url, f"比较 {base}...{head}")
    
    if result["success"]:
        keep_browser_open("已打开代码比较页面")
    
    return result


def view_blame(owner, repo, path, branch="main"):
    """
    View git blame for a file in browser.
    
    Args:
        owner: Repository owner
        repo: Repository name
        path: File path
        branch: Branch name
    """
    url = f"https://github.com/{owner}/{repo}/blame/{branch}/{path}"
    result = navigate_to(url, f"查看 {path} 的 Blame 信息")
    
    if result["success"]:
        keep_browser_open("已打开 Blame 页面")
    
    return result


def view_history(owner, repo, path, branch="main"):
    """
    View commit history for a file in browser.
    
    Args:
        owner: Repository owner
        repo: Repository name
        path: File path
        branch: Branch name
    """
    url = f"https://github.com/{owner}/{repo}/commits/{branch}/{path}"
    result = navigate_to(url, f"查看 {path} 的提交历史")
    
    if result["success"]:
        keep_browser_open("已打开提交历史页面")
    
    return result


# ==================== 通用浏览器操作 ====================

def execute_browser_action(action_description):
    """
    Execute a browser action based on natural language description.
    This is a helper for AI Agent to perform arbitrary browser operations.
    
    Args:
        action_description: Natural language description of the action
    
    Returns:
        dict with success status and current page info
    """
    print(f"\n🎯 执行浏览器操作: {action_description}")
    print("=" * 60)
    
    page = _get_page()
    if not page:
        return {"success": False, "error": "无法启动浏览器"}
    
    print("\n💡 浏览器已打开，请手动完成以下操作：")
    print(f"   {action_description}")
    print("\n   操作完成后，浏览器将保持打开状态。")
    print("   您可以继续手动浏览或执行其他操作。")
    print("=" * 60)
    
    keep_browser_open()
    
    return {
        "success": True,
        "message": f"浏览器已准备就绪，请手动完成: {action_description}",
        "current_url": page.url,
        "title": page.title()
    }


# ==================== 主程序 ====================

def print_usage():
    print("""GitHub Browser Operations - 浏览器自动化操作工具

用法: python3 github_browser_ops.py <操作> [参数...]

用户操作:
  profile <username>          查看用户个人资料
  contributions <username>    查看用户贡献图
  activity <username>         查看用户活动概览
  stars <username>            查看用户 Star 列表
  followers <username>        查看用户粉丝列表
  following <username>        查看用户关注列表
  sponsors <username>         查看用户赞助页面
  settings                    查看用户设置页面
  organizations               查看用户组织页面

仓库操作:
  insights <owner/repo>       查看仓库 Insights (Pulse)
  traffic <owner/repo>        查看仓库流量统计
  network <owner/repo>        查看 Fork 网络图
  dependents <owner/repo>     查看依赖者列表
  security <owner/repo>       查看安全信息
  settings <owner/repo>       查看仓库设置
  projects <owner/repo>       查看 Projects
  wiki <owner/repo>           查看 Wiki
  discussions <owner/repo>    查看 Discussions
  actions <owner/repo>        查看 Actions

代码操作:
  blame <owner/repo> <path> [branch]     查看文件 Blame
  history <owner/repo> <path> [branch]   查看文件历史
  commit <owner/repo> <sha>              查看提交详情
  compare <owner/repo> <base> <head>     比较分支/提交
  codesearch <owner/repo> <query>        在仓库中搜索代码

导航操作:
  goto <url>                  导航到指定 URL
  notifications               打开通知页面
  explore                     打开 Explore 页面
  marketplace                 打开 Marketplace 页面
  search <query> [type]       在 GitHub 搜索
  gist [username]             查看 Gists

浏览器控制:
  close                       关闭浏览器
  status                      查看浏览器状态

示例:
  python3 github_browser_ops.py contributions torvalds
  python3 github_browser_ops.py insights facebook/react
  python3 github_browser_ops.py traffic microsoft/vscode
  python3 github_browser_ops.py blame torvalds/linux kernel/sched/core.c
  python3 github_browser_ops.py goto https://github.com/notifications
  python3 github_browser_ops.py close

注意:
  - 浏览器操作过程可见，操作结束后浏览器保持打开
  - 需要先登录（运行 python3 github_login.py browser）
  - 部分功能需要相应权限（如 Traffic 需要仓库 push 权限）
""")


def parse_repo_path(repo_path):
    """Parse owner/repo format"""
    if "/" not in repo_path:
        print("请使用 owner/repo 格式，例如: facebook/react")
        return None, None
    parts = repo_path.split("/", 1)
    return parts[0], parts[1]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
    
    action = sys.argv[1]
    
    # Browser control
    if action == "close":
        close_browser()
        sys.exit(0)
    
    if action == "status":
        if _browser_instance:
            print("✅ 浏览器正在运行")
            print(f"   当前页面: {_page_instance.url if _page_instance else 'N/A'}")
        else:
            print("ℹ️ 浏览器未启动")
        sys.exit(0)
    
    # User operations
    if action == "profile":
        if len(sys.argv) < 3:
            print("请提供用户名")
            sys.exit(1)
        result = view_user_profile(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "contributions":
        if len(sys.argv) < 3:
            print("请提供用户名")
            sys.exit(1)
        result = view_contributions(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "activity":
        if len(sys.argv) < 3:
            print("请提供用户名")
            sys.exit(1)
        result = view_user_activity(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "stars":
        if len(sys.argv) < 3:
            print("请提供用户名")
            sys.exit(1)
        result = view_user_stars(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "followers":
        if len(sys.argv) < 3:
            print("请提供用户名")
            sys.exit(1)
        result = view_user_followers(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "following":
        if len(sys.argv) < 3:
            print("请提供用户名")
            sys.exit(1)
        result = view_user_following(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "sponsors":
        if len(sys.argv) < 3:
            print("请提供用户名")
            sys.exit(1)
        result = view_sponsors(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "settings":
        if len(sys.argv) >= 3 and "/" in sys.argv[2]:
            owner, repo = parse_repo_path(sys.argv[2])
            result = view_repo_settings(owner, repo)
        else:
            result = view_user_settings()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "organizations":
        result = view_user_organizations()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # Repository operations
    if action == "insights":
        if len(sys.argv) < 3:
            print("请提供 owner/repo")
            sys.exit(1)
        owner, repo = parse_repo_path(sys.argv[2])
        result = view_repo_insights(owner, repo)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "traffic":
        if len(sys.argv) < 3:
            print("请提供 owner/repo")
            sys.exit(1)
        owner, repo = parse_repo_path(sys.argv[2])
        result = view_repo_traffic(owner, repo)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "network":
        if len(sys.argv) < 3:
            print("请提供 owner/repo")
            sys.exit(1)
        owner, repo = parse_repo_path(sys.argv[2])
        result = view_repo_network(owner, repo)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "dependents":
        if len(sys.argv) < 3:
            print("请提供 owner/repo")
            sys.exit(1)
        owner, repo = parse_repo_path(sys.argv[2])
        result = view_repo_dependents(owner, repo)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "security":
        if len(sys.argv) < 3:
            print("请提供 owner/repo")
            sys.exit(1)
        owner, repo = parse_repo_path(sys.argv[2])
        result = view_repo_security(owner, repo)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "projects":
        if len(sys.argv) < 3:
            print("请提供 owner/repo")
            sys.exit(1)
        owner, repo = parse_repo_path(sys.argv[2])
        result = view_repo_projects(owner, repo)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "wiki":
        if len(sys.argv) < 3:
            print("请提供 owner/repo")
            sys.exit(1)
        owner, repo = parse_repo_path(sys.argv[2])
        result = view_repo_wiki(owner, repo)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "discussions":
        if len(sys.argv) < 3:
            print("请提供 owner/repo 或组织名")
            sys.exit(1)
        if "/" in sys.argv[2]:
            owner, repo = parse_repo_path(sys.argv[2])
            result = view_discussions(owner, repo)
        else:
            result = view_discussions(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "actions":
        if len(sys.argv) < 3:
            print("请提供 owner/repo")
            sys.exit(1)
        owner, repo = parse_repo_path(sys.argv[2])
        result = view_actions_workflows(owner, repo)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # Code operations
    if action == "blame":
        if len(sys.argv) < 4:
            print("用法: blame <owner/repo> <path> [branch]")
            sys.exit(1)
        owner, repo = parse_repo_path(sys.argv[2])
        path = sys.argv[3]
        branch = sys.argv[4] if len(sys.argv) > 4 else "main"
        result = view_blame(owner, repo, path, branch)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "history":
        if len(sys.argv) < 4:
            print("用法: history <owner/repo> <path> [branch]")
            sys.exit(1)
        owner, repo = parse_repo_path(sys.argv[2])
        path = sys.argv[3]
        branch = sys.argv[4] if len(sys.argv) > 4 else "main"
        result = view_history(owner, repo, path, branch)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "commit":
        if len(sys.argv) < 4:
            print("用法: commit <owner/repo> <sha>")
            sys.exit(1)
        owner, repo = parse_repo_path(sys.argv[2])
        sha = sys.argv[3]
        result = view_commit(owner, repo, sha)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "compare":
        if len(sys.argv) < 5:
            print("用法: compare <owner/repo> <base> <head>")
            sys.exit(1)
        owner, repo = parse_repo_path(sys.argv[2])
        base = sys.argv[3]
        head = sys.argv[4]
        result = view_compare(owner, repo, base, head)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "codesearch":
        if len(sys.argv) < 4:
            print("用法: codesearch <owner/repo> <query>")
            sys.exit(1)
        owner, repo = parse_repo_path(sys.argv[2])
        query = sys.argv[3]
        result = view_code_search(owner, repo, query)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # Navigation operations
    if action == "goto":
        if len(sys.argv) < 3:
            print("请提供 URL")
            sys.exit(1)
        result = navigate_to(sys.argv[2])
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "notifications":
        result = view_notifications()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "explore":
        result = view_explore()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "marketplace":
        result = view_marketplace()
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "search":
        if len(sys.argv) < 3:
            print("请提供搜索关键词")
            sys.exit(1)
        query = sys.argv[2]
        search_type = sys.argv[3] if len(sys.argv) > 3 else "repositories"
        result = search_on_github(query, search_type)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    if action == "gist":
        username = sys.argv[2] if len(sys.argv) > 2 else None
        result = view_gist(username=username)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        sys.exit(0)
    
    # Unknown action
    print(f"未知操作: {action}")
    print_usage()
    sys.exit(1)