#!/usr/bin/env python3
"""
GitHub 搜索工具
支持搜索仓库、用户、代码等
"""

import json
import sys
import os
import requests

# Import centralized configuration
from config import get_stored_token


def _get_token():
    """获取存储的 GitHub Token"""
    token = get_stored_token()
    if token:
        return token
    # 也检查环境变量
    return os.environ.get("GITHUB_TOKEN", "")


def search_repositories(query, sort="stars", order="desc", limit=10):
    """搜索 GitHub 仓库"""
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": sort,
        "order": order,
        "per_page": limit,
    }
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    # 如果有token则使用
    token = _get_token()
    if token:
        headers["Authorization"] = f"token {token}"
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            items = data.get("items", [])
            results = []
            for item in items:
                results.append({
                    "name": item.get("full_name", ""),
                    "url": item.get("html_url", ""),
                    "description": item.get("description", "") or "",
                    "language": item.get("language", "") or "",
                    "stars": item.get("stargazers_count", 0),
                    "forks": item.get("forks_count", 0),
                    "open_issues": item.get("open_issues_count", 0),
                    "watchers": item.get("watchers_count", 0),
                    "topics": item.get("topics", []),
                    "license": item.get("license", {}).get("name", "") if item.get("license") else "",
                    "updated_at": item.get("updated_at", ""),
                    "default_branch": item.get("default_branch", ""),
                })
            return {"success": True, "data": results, "total": data.get("total_count", 0)}
        return {"success": False, "error": f"HTTP {resp.status_code}", "data": []}
    except Exception as e:
        return {"success": False, "error": str(e), "data": []}


def search_users(query, limit=10):
    """搜索 GitHub 用户"""
    url = "https://api.github.com/search/users"
    params = {"q": query, "per_page": limit}
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = _get_token()
    if token:
        headers["Authorization"] = f"token {token}"
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            results = []
            for item in data.get("items", []):
                results.append({
                    "username": item.get("login", ""),
                    "url": item.get("html_url", ""),
                    "avatar": item.get("avatar_url", ""),
                    "type": item.get("type", ""),
                })
            return {"success": True, "data": results}
        return {"success": False, "error": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_repo_info(owner, repo):
    """获取单个仓库详细信息"""
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = _get_token()
    if token:
        headers["Authorization"] = f"token {token}"
    
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        if resp.status_code == 200:
            item = resp.json()
            return {
                "success": True,
                "data": {
                    "name": item.get("full_name", ""),
                    "url": item.get("html_url", ""),
                    "description": item.get("description", "") or "",
                    "language": item.get("language", "") or "",
                    "stars": item.get("stargazers_count", 0),
                    "forks": item.get("forks_count", 0),
                    "watchers": item.get("watchers_count", 0),
                    "open_issues": item.get("open_issues_count", 0),
                    "topics": item.get("topics", []),
                    "license": item.get("license", {}).get("name", "") if item.get("license") else "",
                    "created_at": item.get("created_at", ""),
                    "updated_at": item.get("updated_at", ""),
                    "pushed_at": item.get("pushed_at", ""),
                    "default_branch": item.get("default_branch", ""),
                    "homepage": item.get("homepage", "") or "",
                    "size": item.get("size", 0),
                    "network_count": item.get("network_count", 0),
                    "subscribers_count": item.get("subscribers_count", 0),
                    "archived": item.get("archived", False),
                    "disabled": item.get("disabled", False),
                    "private": item.get("private", False),
                    "owner_avatar": item.get("owner", {}).get("avatar_url", ""),
                }
            }
        return {"success": False, "error": f"HTTP {resp.status_code}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "repos"
    
    if action == "repos":
        q = sys.argv[2] if len(sys.argv) > 2 else "stars:>1000"
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 10
        print(json.dumps(search_repositories(q, limit=limit), ensure_ascii=False, indent=2))
    elif action == "users":
        q = sys.argv[2] if len(sys.argv) > 2 else ""
        print(json.dumps(search_users(q), ensure_ascii=False, indent=2))
    elif action == "info":
        owner = sys.argv[2] if len(sys.argv) > 2 else ""
        repo = sys.argv[3] if len(sys.argv) > 3 else ""
        print(json.dumps(get_repo_info(owner, repo), ensure_ascii=False, indent=2))
