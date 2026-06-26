#!/usr/bin/env python3
"""
GitHub Track - 追踪 GitHub 仓库动态
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests

# 配置路径
CONFIG_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
CONFIG_FILE = CONFIG_DIR / "github-track-config.json"
DATA_FILE = CONFIG_DIR / "github-track-data.json"

# GitHub API
API_BASE = "https://api.github.com"


def load_config():
    """加载配置"""
    if not CONFIG_FILE.exists():
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        config = {"repos": [], "last_check": None}
        save_config(config)
        return config
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_config(config):
    """保存配置"""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def load_data():
    """加载追踪数据"""
    if not DATA_FILE.exists():
        return {}
    
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data):
    """保存追踪数据"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def get_github_token():
    """获取 GitHub Token"""
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    
    # 尝试从 TOOLS.md 读取
    tools_file = Path.home() / ".openclaw" / "workspace" / "TOOLS.md"
    if tools_file.exists():
        content = tools_file.read_text(encoding="utf-8")
        for line in content.split("\n"):
            if "GITHUB_TOKEN" in line and ":" in line:
                token = line.split(":", 1)[1].strip()
                if token:
                    return token
    
    return None


def make_request(url):
    """发送 GitHub API 请求"""
    token = get_github_token()
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    if token:
        headers["Authorization"] = f"token {token}"
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 403:
        print("⚠️ API rate limit exceeded. Consider using GITHUB_TOKEN")
        return None
    
    if response.status_code != 200:
        print(f"⚠️ Request failed: {response.status_code}")
        return None
    
    return response.json()


def get_repo_info(owner, repo):
    """获取仓库基本信息"""
    url = f"{API_BASE}/repos/{owner}/{repo}"
    return make_request(url)


def get_issues(owner, repo, state="all", limit=5):
    """获取 Issues"""
    url = f"{API_BASE}/repos/{owner}/{repo}/issues?state={state}&sort=updated&per_page={limit}"
    data = make_request(url)
    if data:
        # 过滤掉 PRs
        return [item for item in data if "pull_request" not in item]
    return []


def get_pull_requests(owner, repo, state="all", limit=5):
    """获取 Pull Requests"""
    url = f"{API_BASE}/repos/{owner}/{repo}/pulls?state={state}&sort=updated&per_page={limit}"
    return make_request(url) or []


def track_repo(owner, repo):
    """追踪指定仓库"""
    print(f"\n🔍 正在追踪 {owner}/{repo}...")
    
    # 获取仓库信息
    repo_info = get_repo_info(owner, repo)
    if not repo_info:
        print(f"❌ 无法获取 {owner}/{repo} 的信息，请检查仓库是否存在")
        return None
    
    # 获取 issues
    issues = get_issues(owner, repo, "all", 5)
    
    # 获取 PRs
    prs = get_pull_requests(owner, repo, "all", 5)
    
    # 构建数据
    now = datetime.utcnow().isoformat() + "Z"
    data = {
        "last_check": now,
        "stars": repo_info.get("stargazers_count", 0),
        "forks": repo_info.get("forks_count", 0),
        "open_issues": repo_info.get("open_issues_count", 0),
        "subscribers_count": repo_info.get("subscribers_count", 0),
        "recent_issues": [
            {
                "number": issue["number"],
                "title": issue["title"],
                "state": issue["state"],
                "updated_at": issue["updated_at"],
                "comments": issue["comments"],
                "labels": [label["name"] for label in issue.get("labels", [])]
            }
            for issue in issues[:5]
        ],
        "recent_prs": [
            {
                "number": pr["number"],
                "title": pr["title"],
                "state": pr["state"],
                "merged_at": pr.get("merged_at"),
                "updated_at": pr["updated_at"],
                "draft": pr.get("draft", False)
            }
            for pr in prs[:5]
        ]
    }
    
    return data


def compare_changes(old_data, new_data):
    """对比变化"""
    changes = []
    
    # Stars 变化
    if old_data and "stars" in old_data:
        diff = new_data["stars"] - old_data["stars"]
        if diff > 0:
            changes.append(f"⭐ Stars +{diff}")
        elif diff < 0:
            changes.append(f"⭐ Stars {diff}")
    
    # Forks 变化
    if old_data and "forks" in old_data:
        diff = new_data["forks"] - old_data["forks"]
        if diff > 0:
            changes.append(f"🍴 Forks +{diff}")
    
    # Open issues 变化
    if old_data and "open_issues" in old_data:
        diff = new_data["open_issues"] - old_data["open_issues"]
        if diff > 0:
            changes.append(f"🐛 Open Issues +{diff}")
        elif diff < 0:
            changes.append(f"🐛 Open Issues {diff}")
    
    # 新 Issue 检测
    if old_data and "recent_issues" in old_data:
        old_issue_numbers = {issue["number"] for issue in old_data["recent_issues"]}
        new_issues = [issue for issue in new_data["recent_issues"] 
                      if issue["number"] not in old_issue_numbers]
        if new_issues:
            changes.append(f"📝 新增 {len(new_issues)} 个 Issue")
    
    # 新 PR 检测
    if old_data and "recent_prs" in old_data:
        old_pr_numbers = {pr["number"] for pr in old_data["recent_prs"]}
        new_prs = [pr for pr in new_data["recent_prs"] 
                   if pr["number"] not in old_pr_numbers]
        if new_prs:
            changes.append(f"📥 新增 {len(new_prs)} 个 PR")
    
    return changes


def format_report(repo_key, data, changes):
    """格式化追踪报告"""
    stars = data.get("stars", 0)
    forks = data.get("forks", 0)
    open_issues = data.get("open_issues", 0)
    
    report = []
    report.append(f"\n## 🎯 {repo_key}")
    report.append("")
    report.append("**📊 当前状态**")
    report.append(f"- ⭐ Stars: {stars:,}")
    report.append(f"- 🍴 Forks: {forks:,}")
    report.append(f"- 🐛 Open Issues: {open_issues}")
    report.append("")
    
    # 最近 Issues
    if data.get("recent_issues"):
        report.append("**🐛 最近 Issues**")
        for issue in data["recent_issues"][:5]:
            state_emoji = "✅" if issue["state"] == "closed" else "🐛"
            comments = f" ({issue['comments']} comments)" if issue["comments"] > 0 else ""
            labels = f" [{', '.join(issue['labels'][:2])}]" if issue.get("labels") else ""
            report.append(f"- {state_emoji} [#{issue['number']}](https://github.com/{repo_key}/issues/{issue['number']}) - {issue['title']}{comments}{labels}")
        report.append("")
    
    # 最近 PRs
    if data.get("recent_prs"):
        report.append("**📥 最近 PRs**")
        for pr in data["recent_prs"][:5]:
            if pr.get("merged_at"):
                state_emoji = "✅ merged"
            elif pr["state"] == "closed":
                state_emoji = "❌ closed"
            elif pr.get("draft"):
                state_emoji = "📝 draft"
            else:
                state_emoji = "📥 open"
            report.append(f"- {state_emoji} [#{pr['number']}](https://github.com/{repo_key}/pull/{pr['number']}) - {pr['title']}")
        report.append("")
    
    # 变化
    if changes:
        report.append("**✨ 变化**")
        for change in changes:
            report.append(f"- {change}")
    
    return "\n".join(report)


def add_repo(owner, repo):
    """添加追踪仓库"""
    config = load_config()
    repo_key = f"{owner}/{repo}"
    
    # 检查是否已存在
    for repo_config in config["repos"]:
        if f"{repo_config['owner']}/{repo_config['repo']}" == repo_key:
            print(f"⚠️ {repo_key} 已经在追踪列表中")
            return
    
    # 添加到配置
    config["repos"].append({
        "owner": owner,
        "repo": repo,
        "track_stars": True,
        "track_issues": True,
        "track_prs": True
    })
    save_config(config)
    
    # 获取初始数据
    data = track_repo(owner, repo)
    if data:
        all_data = load_data()
        all_data[repo_key] = data
        save_data(all_data)
        print(f"✅ 已添加 {repo_key} 到追踪列表")


def remove_repo(owner, repo):
    """移除追踪仓库"""
    config = load_config()
    repo_key = f"{owner}/{repo}"
    
    # 从配置中移除
    config["repos"] = [r for r in config["repos"] 
                       if f"{r['owner']}/{r['repo']}" != repo_key]
    save_config(config)
    
    # 从数据中移除
    all_data = load_data()
    if repo_key in all_data:
        del all_data[repo_key]
        save_data(all_data)
    
    print(f"✅ 已从追踪列表移除 {repo_key}")


def list_repos():
    """列出所有追踪的仓库"""
    config = load_config()
    all_data = load_data()
    
    if not config["repos"]:
        print("📭 暂无追踪的仓库")
        return
    
    print("\n📋 追踪的仓库列表:")
    for repo_config in config["repos"]:
        repo_key = f"{repo_config['owner']}/{repo_config['repo']}"
        data = all_data.get(repo_key, {})
        stars = data.get("stars", 0)
        print(f"  - {repo_key}: ⭐ {stars:,}")


def refresh_repo(owner, repo):
    """刷新仓库追踪数据"""
    repo_key = f"{owner}/{repo}"
    old_data = load_data().get(repo_key)
    
    new_data = track_repo(owner, repo)
    if new_data:
        all_data = load_data()
        all_data[repo_key] = new_data
        save_data(all_data)
        
        # 对比变化
        changes = compare_changes(old_data, new_data)
        
        # 输出报告
        print(format_report(repo_key, new_data, changes))


def refresh_all():
    """刷新所有追踪的仓库"""
    config = load_config()
    
    if not config["repos"]:
        print("📭 暂无追踪的仓库")
        return
    
    print("🔄 刷新所有追踪的仓库...")
    for repo_config in config["repos"]:
        refresh_repo(repo_config["owner"], repo_config["repo"])


def search_issues(owner, repo, keyword, state="all", limit=10):
    """搜索 Issues 中的关键词"""
    print(f"\n🔍 在 {owner}/{repo} 中搜索 issue: {keyword}")
    
    issues = get_issues(owner, repo, state, 30)
    
    if not issues:
        print("未找到相关 issues")
        return
    
    # 关键词匹配
    keyword_lower = keyword.lower()
    matched = [
        issue for issue in issues
        if keyword_lower in issue["title"].lower() or 
           keyword_lower in issue.get("body", "").lower()
    ][:limit]
    
    if not matched:
        print(f"未找到包含关键词 '{keyword}' 的 issue")
        return
    
    print(f"\n找到 {len(matched)} 条匹配的 issue:")
    for issue in matched:
        state_emoji = "✅" if issue["state"] == "closed" else "🐛"
        comments = f" ({issue['comments']} comments)" if issue["comments"] > 0 else ""
        labels_list = [l["name"] for l in issue.get("labels", [])[:2]]
        labels = f" [{', '.join(labels_list)}]" if labels_list else ""
        print(f"\n{state_emoji} [#{issue['number']}](https://github.com/{owner}/{repo}/issues/{issue['number']})")
        print(f"   {issue['title']}{comments}{labels}")
        if issue.get("body"):
            body_preview = issue["body"][:200] + "..." if len(issue.get("body", "")) > 200 else issue.get("body", "")
            print(f"   📝 {body_preview}")


def search_prs(owner, repo, keyword, state="all", limit=10):
    """搜索 PRs 中的关键词"""
    print(f"\n🔍 在 {owner}/{repo} 中搜索 PR: {keyword}")
    
    prs = get_pull_requests(owner, repo, state, 30)
    
    if not prs:
        print("未找到相关 PRs")
        return
    
    # 关键词匹配
    keyword_lower = keyword.lower()
    matched = [
        pr for pr in prs
        if keyword_lower in pr["title"].lower() or 
           keyword_lower in pr.get("body", "").lower()
    ][:limit]
    
    if not matched:
        print(f"未找到包含关键词 '{keyword}' 的 PR")
        return
    
    print(f"\n找到 {len(matched)} 条匹配的 PR:")
    for pr in matched:
        if pr.get("merged_at"):
            state_emoji = "✅ merged"
        elif pr["state"] == "closed":
            state_emoji = "❌ closed"
        elif pr.get("draft"):
            state_emoji = "📝 draft"
        else:
            state_emoji = "📥 open"
        
        print(f"\n{state_emoji} [#{pr['number']}](https://github.com/{owner}/{repo}/pull/{pr['number']})")
        print(f"   {pr['title']}")
        if pr.get("body"):
            body_preview = pr["body"][:200] + "..." if len(pr.get("body", "")) > 200 else pr.get("body", "")
            print(f"   📝 {body_preview}")


def get_issue_by_number(owner, repo, issue_number):
    """获取指定编号的 Issue"""
    url = f"{API_BASE}/repos/{owner}/{repo}/issues/{issue_number}"
    return make_request(url)


def get_pr_by_number(owner, repo, pr_number):
    """获取指定编号的 PR"""
    url = f"{API_BASE}/repos/{owner}/{repo}/pulls/{pr_number}"
    return make_request(url)


def show_issue(owner, repo, issue_number):
    """显示指定 Issue 详情"""
    print(f"\n🔍 获取 {owner}/{repo} issue #{issue_number}...")
    
    issue = get_issue_by_number(owner, repo, issue_number)
    
    if not issue:
        print(f"❌ Issue #{issue_number} 不存在")
        return
    
    state_emoji = "✅" if issue["state"] == "closed" else "🐛"
    labels = ", ".join([l["name"] for l in issue.get("labels", [])]) or "无"
    created = issue.get("created_at", "")[:10]
    updated = issue.get("updated_at", "")[:10]
    
    print(f"\n## {state_emoji} [#{issue['number']}]({issue['html_url']})")
    print(f"**{issue['title']}**")
    print(f"\n- 状态: {issue['state']}")
    print(f"- 标签: {labels}")
    print(f"- 评论数: {issue['comments']}")
    print(f"- 创建时间: {created}")
    print(f"- 更新时间: {updated}")
    print(f"- 作者: {issue['user']['login']}")
    
    if issue.get("body"):
        print(f"\n**内容:**\n{issue['body']}")
    
    # 获取评论
    comments_url = f"{API_BASE}/repos/{owner}/{repo}/issues/{issue_number}/comments"
    comments = make_request(comments_url)
    if comments:
        print(f"\n**评论 ({len(comments)} 条):**")
        for comment in comments[:5]:
            comment_date = comment["created_at"][:10]
            print(f"\n- {comment['user']['login']} ({comment_date}):")
            print(f"  {comment['body'][:300]}")


def show_pr(owner, repo, pr_number):
    """显示指定 PR 详情"""
    print(f"\n🔍 获取 {owner}/{repo} PR #{pr_number}...")
    
    pr = get_pr_by_number(owner, repo, pr_number)
    
    if not pr:
        print(f"❌ PR #{pr_number} 不存在")
        return
    
    if pr.get("merged_at"):
        state_emoji = "✅ merged"
    elif pr["state"] == "closed":
        state_emoji = "❌ closed"
    elif pr.get("draft"):
        state_emoji = "📝 draft"
    else:
        state_emoji = "📥 open"
    
    created = pr.get("created_at", "")[:10]
    updated = pr.get("updated_at", "")[:10]
    
    print(f"\n## {state_emoji} [#{pr['number']}]({pr['html_url']})")
    print(f"**{pr['title']}**")
    print(f"\n- 状态: {state_emoji}")
    print(f"- 是否草稿: {pr.get('draft', False)}")
    print(f"- 评论数: {pr.get('comments', 0)}")
    print(f"- 创建时间: {created}")
    print(f"- 更新时间: {updated}")
    print(f"- 作者: {pr['user']['login']}")
    print(f"- 源分支: {pr.get('head', {}).get('ref', 'N/A')} → {pr.get('base', {}).get('ref', 'N/A')}")
    
    if pr.get("body"):
        print(f"\n**内容:**\n{pr['body']}")


def main():
    parser = argparse.ArgumentParser(description="GitHub Track - 仓库动态追踪")
    parser.add_argument("command", choices=["add", "remove", "list", "refresh", "track", "search-issue", "search-pr", "show-issue", "show-pr"],
                        help="命令")
    parser.add_argument("--owner", help="仓库所有者")
    parser.add_argument("--repo", help="仓库名称")
    parser.add_argument("--keyword", "-k", help="搜索关键词")
    parser.add_argument("--number", "-n", type=int, help="Issue/PR 编号")
    parser.add_argument("--state", default="all", choices=["open", "closed", "all"], help="状态过滤")
    parser.add_argument("--limit", type=int, default=10, help="结果数量限制")
    
    args = parser.parse_args()
    
    if args.command == "add":
        if not args.owner or not args.repo:
            print("❌ 请指定 --owner 和 --repo")
            sys.exit(1)
        add_repo(args.owner, args.repo)
    
    elif args.command == "remove":
        if not args.owner or not args.repo:
            print("❌ 请指定 --owner 和 --repo")
            sys.exit(1)
        remove_repo(args.owner, args.repo)
    
    elif args.command == "list":
        list_repos()
    
    elif args.command == "refresh":
        if args.owner and args.repo:
            refresh_repo(args.owner, args.repo)
        else:
            refresh_all()
    
    elif args.command == "track":
        if not args.owner or not args.repo:
            print("❌ 请指定 --owner 和 --repo")
            sys.exit(1)
        refresh_repo(args.owner, args.repo)
    
    elif args.command == "search-issue":
        if not args.owner or not args.repo or not args.keyword:
            print("❌ 请指定 --owner, --repo 和 --keyword")
            sys.exit(1)
        search_issues(args.owner, args.repo, args.keyword, args.state, args.limit)
    
    elif args.command == "search-pr":
        if not args.owner or not args.repo or not args.keyword:
            print("❌ 请指定 --owner, --repo 和 --keyword")
            sys.exit(1)
        search_prs(args.owner, args.repo, args.keyword, args.state, args.limit)
    
    elif args.command == "show-issue":
        if not args.owner or not args.repo or not args.number:
            print("❌ 请指定 --owner, --repo 和 --number")
            sys.exit(1)
        show_issue(args.owner, args.repo, args.number)
    
    elif args.command == "show-pr":
        if not args.owner or not args.repo or not args.number:
            print("❌ 请指定 --owner, --repo 和 --number")
            sys.exit(1)
        show_pr(args.owner, args.repo, args.number)


if __name__ == "__main__":
    main()
