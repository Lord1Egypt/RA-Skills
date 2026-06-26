#!/usr/bin/env python3
"""
GitHub Stars Tracker - 监控 GitHub 仓库的 stars 变化
"""
import os
import sys
import json
import time
import argparse
from datetime import datetime

DATA_FILE = os.path.expanduser("~/.github-stars-tracker.json")

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {"repos": {}, "history": []}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_github_token():
    return os.environ.get("GITHUB_TOKEN", "")

def fetch_repo_info(owner, repo):
    import urllib.request
    import urllib.error
    
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    token = get_github_token()
    if token:
        headers["Authorization"] = f"token {token}"
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return {
                "stars": data.get("stargazers_count", 0),
                "forks": data.get("forks_count", 0),
                "watchers": data.get("watchers_count", 0),
                "description": data.get("description", ""),
                "language": data.get("language", ""),
                "updated": data.get("updated_at", ""),
            }
    except urllib.error.HTTPError as e:
        print(f"❌ 请求失败: {e.code} - {e.reason}")
        return None
    except Exception as e:
        print(f"❌ 错误: {e}")
        return None

def cmd_add(args):
    data = load_data()
    owner, repo = args.repo.split("/")
    
    print(f"🔍 正在获取 {owner}/{repo} 信息...")
    info = fetch_repo_info(owner, repo)
    
    if info:
        data["repos"][args.repo] = {
            "added_at": datetime.now().isoformat(),
            "last_stars": info["stars"],
            "last_forks": info["forks"],
        }
        save_data(data)
        print(f"✅ 已添加 {args.repo}")
        print(f"   ⭐ Stars: {info['stars']}")
        print(f"   🍴 Forks: {info['forks']}")
        print(f"   📝 语言: {info['language'] or 'N/A'}")
    else:
        print(f"❌ 无法获取仓库信息")

def cmd_status(args):
    data = load_data()
    owner, repo = args.repo.split("/")
    
    info = fetch_repo(owner, repo)
    if info and args.repo in data["repos"]:
        last = data["repos"][args.repo]
        stars_change = info["stars"] - last["last_stars"]
        
        print(f"📊 {args.repo}")
        print(f"   ⭐ Stars: {info['stars']} ({stars_change:+d})")
        print(f"   🍴 Forks: {info['forks']}")
        print(f"   📝 描述: {info['description'][:60]}...")
    elif args.repo not in data["repos"]:
        print(f"❌ 未追踪此仓库，先用 add 添加")
    else:
        print(f"❌ 无法获取信息")

def cmd_list(args):
    data = load_data()
    if not data["repos"]:
        print("📭 暂无追踪的仓库")
        return
    
    print("📋 追踪的仓库列表：")
    for repo in data["repos"]:
        print(f"   • {repo}")

def cmd_check(args):
    data = load_data()
    if not data["repos"]:
        print("📭 暂无追踪的仓库")
        return
    
    print("🔄 检查变化...\n")
    
    for repo in data["repos"]:
        owner, name = repo.split("/")
        info = fetch_repo_info(owner, name)
        
        if info:
            last = data["repos"][repo]
            stars_change = info["stars"] - last["last_stars"]
            
            if stars_change != 0:
                emoji = "📈" if stars_change > 0 else "📉"
                print(f"{emoji} {repo}: {last['last_stars']} → {info['stars']} ({stars_change:+d})")
                
                # 更新数据
                data["repos"][repo]["last_stars"] = info["stars"]
                data["repos"][repo]["last_forks"] = info["forks"]
    
    save_data(data)
    print("\n✅ 检查完成")

def main():
    parser = argparse.ArgumentParser(description="GitHub Stars Tracker")
    subparsers = parser.add_subparsers()
    
    p_add = subparsers.add_parser("add", help="添加要追踪的仓库")
    p_add.add_argument("repo", help="仓库名 (owner/repo)")
    p_add.set_defaults(func=cmd_add)
    
    p_status = subparsers.add_parser("status", help="查看仓库状态")
    p_status.add_argument("repo", help="仓库名 (owner/repo)")
    p_status.set_defaults(func=cmd_status)
    
    p_list = subparsers.add_parser("list", help="列出所有追踪的仓库")
    p_list.set_defaults(func=cmd_list)
    
    p_check = subparsers.add_parser("check", help="检查所有仓库的变化")
    p_check.set_defaults(func=cmd_check)
    
    args = parser.parse_args()
    
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
