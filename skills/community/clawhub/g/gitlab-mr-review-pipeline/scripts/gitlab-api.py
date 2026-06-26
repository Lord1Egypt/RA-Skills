#!/usr/bin/env python3
"""
GitLab API 工具脚本
提供简单的 API 调用功能，不包含业务逻辑
"""

import json
import sys
import argparse
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path

CONFIG_FILE = Path.home() / ".config" / "gitlab-mr-review-pipeline" / "config.json"


def load_config():
    """加载配置"""
    if not CONFIG_FILE.exists():
        print(f"ERROR: 配置文件不存在：{CONFIG_FILE}", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR: 配置文件格式错误：{e}", file=sys.stderr)
        sys.exit(1)


def api_call(endpoint, config):
    """调用 GitLab API"""
    host = config["gitlab"]["host"]
    token = config["gitlab"]["access_token"]
    
    url = f"{host}/api/v4/{endpoint}"
    req = urllib.request.Request(
        url,
        headers={"PRIVATE-TOKEN": token}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"ERROR: API 调用失败 ({e.code}): {e.reason}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return None


def mr_list(repo):
    """获取 MR 列表"""
    config = load_config()
    endpoint = f"projects/{urllib.parse.quote(repo, safe='')}/merge_requests?state=opened"
    mrs = api_call(endpoint, config)
    
    if mrs:
        print(json.dumps(mrs, indent=2, ensure_ascii=False))
    else:
        sys.exit(1)


def mr_diff(repo, mr_id):
    """获取 MR diff"""
    config = load_config()
    endpoint = f"projects/{urllib.parse.quote(repo, safe='')}/merge_requests/{mr_id}/changes"
    changes = api_call(endpoint, config)
    
    if changes:
        # 输出为纯文本 diff 格式
        for change in changes.get("changes", []):
            print(f"diff --git a/{change['old_path']} b/{change['new_path']}")
            print(f"--- a/{change['old_path']}")
            print(f"+++ b/{change['new_path']}")
            print(change.get("diff", ""))
            print()
    else:
        sys.exit(1)


def mr_commits(repo, mr_id):
    """获取 MR commits"""
    config = load_config()
    endpoint = f"projects/{urllib.parse.quote(repo, safe='')}/merge_requests/{mr_id}/commits"
    commits = api_call(endpoint, config)
    
    if commits:
        print(json.dumps(commits, indent=2, ensure_ascii=False))
    else:
        sys.exit(1)


def repo_check(repo):
    """验证仓库是否可访问"""
    config = load_config()
    endpoint = f"projects/{urllib.parse.quote(repo, safe='')}"
    project = api_call(endpoint, config)
    
    if project:
        print(f"OK: {project.get('name', repo)}")
        return True
    else:
        print(f"FAIL: {repo}")
        return False


def main():
    parser = argparse.ArgumentParser(description="GitLab API 工具")
    subparsers = parser.add_subparsers(dest="command", help="命令")
    
    # mr-list 命令
    mr_list_parser = subparsers.add_parser("mr-list", help="获取 MR 列表")
    mr_list_parser.add_argument("--repo", required=True, help="仓库名称")
    
    # mr-diff 命令
    mr_diff_parser = subparsers.add_parser("mr-diff", help="获取 MR diff")
    mr_diff_parser.add_argument("--repo", required=True, help="仓库名称")
    mr_diff_parser.add_argument("--mr-id", required=True, help="MR ID")
    
    # mr-commits 命令
    mr_commits_parser = subparsers.add_parser("mr-commits", help="获取 MR commits")
    mr_commits_parser.add_argument("--repo", required=True, help="仓库名称")
    mr_commits_parser.add_argument("--mr-id", required=True, help="MR ID")
    
    # repo-check 命令
    repo_check_parser = subparsers.add_parser("repo-check", help="验证仓库")
    repo_check_parser.add_argument("--repo", required=True, help="仓库名称")
    
    args = parser.parse_args()
    
    if args.command == "mr-list":
        mr_list(args.repo)
    elif args.command == "mr-diff":
        mr_diff(args.repo, args.mr_id)
    elif args.command == "mr-commits":
        mr_commits(args.repo, args.mr_id)
    elif args.command == "repo-check":
        success = repo_check(args.repo)
        sys.exit(0 if success else 1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
