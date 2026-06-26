#!/usr/bin/env python3
"""
GitHub Issue 提交脚本
用法: python3 submit_issue.py --title "标题" --body "内容" [--patch issue_number]
"""
import argparse
import requests
import json
import sys

TOKEN = "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"
REPO = "openclaw/openclaw"
BASE_URL = f"https://api.github.com/repos/{REPO}"

HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github+json",
    "Content-Type": "application/vnd.github+json",
}


def create_issue(title, body):
    url = f"{BASE_URL}/issues"
    data = {"title": title, "body": body}
    resp = requests.post(url, headers=HEADERS, json=data)
    if resp.status_code == 201:
        issue = resp.json()
        print(f"✅ Issue 创建成功: #{issue['number']}")
        print(f"   {issue['html_url']}")
        return issue["number"]
    else:
        print(f"❌ 创建失败: {resp.status_code}")
        print(resp.text)
        sys.exit(1)


def update_issue(number, title=None, body=None):
    url = f"{BASE_URL}/issues/{number}"
    data = {}
    if title:
        data["title"] = title
    if body:
        data["body"] = body
    resp = requests.patch(url, headers=HEADERS, json=data)
    if resp.status_code == 200:
        print(f"✅ Issue #{number} 更新成功")
    else:
        print(f"❌ 更新失败: {resp.status_code}")
        print(resp.text)
        sys.exit(1)


def search_issues(query):
    url = f"https://api.github.com/search/issues"
    params = {"q": f"{query} repo:{REPO}"}
    resp = requests.get(url, headers=HEADERS, params=params)
    if resp.status_code == 200:
        data = resp.json()
        print(f"找到 {data['total_count']} 个结果:")
        for item in data.get("items", []):
            print(f"  #{item['number']}: {item['title']}")
        return data.get("items", [])
    else:
        print(f"❌ 搜索失败: {resp.status_code}")
        return []


def main():
    parser = argparse.ArgumentParser(description="GitHub Issue 提交工具")
    parser.add_argument("--title", "-t", required=True, help="Issue 标题")
    parser.add_argument("--body", "-b", required=True, help="Issue 内容")
    parser.add_argument("--patch", "-p", type=int, help="更新已有 issue")
    parser.add_argument("--search", "-s", help="搜索现有 issue（不提交）")

    args = parser.parse_args()

    if args.search:
        search_issues(args.search)
    elif args.patch:
        update_issue(args.patch, args.title, args.body)
    else:
        create_issue(args.title, args.body)


if __name__ == "__main__":
    main()
