#!/usr/bin/env python3
"""
搜索 GitHub 仓库
用法: python3 search_github.py "关键词" [--limit 10]
"""
import sys
import json
import os
import urllib.request
import urllib.parse
import argparse

TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "github-analyzer/1.0"
}

def gh_get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())

def search_repos(query: str, limit: int = 10):
    encoded = urllib.parse.quote(query)
    url = f"https://api.github.com/search/repositories?q={encoded}&sort=stars&order=desc&per_page={min(limit * 2, 30)}"
    data = gh_get(url)
    items = data.get("items", [])

    results = []
    for repo in items:
        # 过滤
        if repo.get("fork"):
            continue
        if repo.get("archived"):
            continue
        if repo.get("stargazers_count", 0) < 50:
            continue

        results.append({
            "full_name": repo["full_name"],
            "url": repo["html_url"],
            "description": repo.get("description") or "",
            "stars": repo["stargazers_count"],
            "forks": repo["forks_count"],
            "language": repo.get("language") or "Unknown",
            "updated_at": repo["updated_at"][:10],
            "topics": repo.get("topics", []),
            "license": (repo.get("license") or {}).get("spdx_id", "Unknown"),
            "open_issues": repo.get("open_issues_count", 0),
        })

        if len(results) >= limit:
            break

    return results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument("--limit", type=int, default=10)
    args = parser.parse_args()

    results = search_repos(args.query, args.limit)
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
