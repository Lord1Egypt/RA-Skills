#!/usr/bin/env python3
"""
分析单个 GitHub 仓库
用法: python3 analyze_repo.py "owner/repo"
"""
import sys
import json
import os
import urllib.request
import urllib.parse

TOKEN = os.environ.get("GITHUB_TOKEN", "")
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "github-analyzer/1.0"
}

def gh_get(url):
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": str(e), "url": url}

def get_readme(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    data = gh_get(url)
    if "error" in data:
        return ""
    import base64
    content = data.get("content", "")
    try:
        decoded = base64.b64decode(content).decode("utf-8", errors="ignore")
        # 只取前 3000 字符
        return decoded[:3000]
    except Exception:
        return ""

def get_languages(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/languages"
    data = gh_get(url)
    if "error" in data:
        return {}
    return data

def get_contributors_count(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page=1&anon=true"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            # 从 Link header 获取总页数
            link = r.getheader("Link", "")
            if 'rel="last"' in link:
                import re
                m = re.search(r'page=(\d+)>; rel="last"', link)
                if m:
                    return int(m.group(1))
            items = json.loads(r.read())
            return len(items)
    except Exception:
        return 0

def analyze_repo(full_name: str):
    owner, repo = full_name.strip("/").split("/")[-2:]

    # 基础信息
    repo_data = gh_get(f"https://api.github.com/repos/{owner}/{repo}")
    if "error" in repo_data:
        return {"error": f"仓库不存在或无法访问: {full_name}"}

    # README
    readme = get_readme(owner, repo)

    # 语言统计
    languages = get_languages(owner, repo)
    lang_list = sorted(languages.items(), key=lambda x: -x[1])
    top_langs = [l[0] for l in lang_list[:5]]

    # 贡献者数量
    contributors = get_contributors_count(owner, repo)

    result = {
        "full_name": repo_data["full_name"],
        "url": repo_data["html_url"],
        "description": repo_data.get("description") or "",
        "stars": repo_data["stargazers_count"],
        "forks": repo_data["forks_count"],
        "watchers": repo_data["watchers_count"],
        "open_issues": repo_data["open_issues_count"],
        "language": repo_data.get("language") or "Unknown",
        "languages": top_langs,
        "topics": repo_data.get("topics", []),
        "license": (repo_data.get("license") or {}).get("spdx_id", "Unknown"),
        "created_at": repo_data["created_at"][:10],
        "updated_at": repo_data["updated_at"][:10],
        "pushed_at": repo_data["pushed_at"][:10],
        "size_kb": repo_data.get("size", 0),
        "default_branch": repo_data.get("default_branch", "main"),
        "homepage": repo_data.get("homepage") or "",
        "has_wiki": repo_data.get("has_wiki", False),
        "has_pages": repo_data.get("has_pages", False),
        "contributors_approx": contributors,
        "readme_excerpt": readme,
        "clone_url": repo_data["clone_url"],
        "zip_url": f"https://github.com/{owner}/{repo}/archive/refs/heads/{repo_data.get('default_branch','main')}.zip",
    }

    return result

def main():
    if len(sys.argv) < 2:
        print("用法: python3 analyze_repo.py owner/repo [owner/repo ...]")
        sys.exit(1)

    results = []
    for arg in sys.argv[1:]:
        # 支持完整 URL 或 owner/repo
        if "github.com" in arg:
            parts = arg.rstrip("/").split("github.com/")[-1].split("/")
            full_name = "/".join(parts[:2])
        else:
            full_name = arg
        results.append(analyze_repo(full_name))

    if len(results) == 1:
        print(json.dumps(results[0], ensure_ascii=False, indent=2))
    else:
        print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
