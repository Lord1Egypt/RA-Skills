#!/usr/bin/env python3
"""Fetch GitHub trending repos and print as JSON for further processing."""
import urllib.request
import json
import re
import sys
import html

def fetch_trending_page():
    req = urllib.request.Request(
        "https://github.com/trending",
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read().decode("utf-8")

def extract_repos(html_content, max_repos=10):
    # Extract repo paths from trending page
    # The real repo link has data-hydro-click with "TRENDING_REPOSITORIES_PAGE"
    # The sponsor link has data-hydro-click with "sponsors.button_click"
    # We want the repo link inside the h1, not the sponsor link
    articles = re.findall(r'<article[^>]*class="[^"]*Box-row[^"]*"[^>]*>(.*?)</article>', html_content, re.DOTALL)
    
    repos = []
    for art in articles[:max_repos]:
        # Find the real repo link: it's in the h1 section and has TRENDING_REPOSITORIES_PAGE
        h1_match = re.search(r'<h1[^>]*>(.*?)</h1>', art, re.DOTALL)
        if h1_match:
            h1_content = h1_match.group(1)
            # Find owner/repo href in the h1 - this is the real repo
            repo_match = re.search(r'href="(/[^/]+/[^"]+)"', h1_content)
            if repo_match:
                path = repo_match.group(1).strip()
                if path and "/" in path and not path.startswith("/sponsors") and not path.startswith("/login"):
                    repos.append(path)
                    continue
        
        # Fallback: find any owner/repo href that doesn't start with excluded prefixes
        all_hrefs = re.findall(r'href="(/([a-zA-Z0-9_-]+)/([a-zA-Z0-9_.-]+))"', art)
        for full_href, owner, repo in all_hrefs:
            path = full_href.strip()
            # Skip non-repo paths
            if any(path.startswith(x) for x in ["/login", "/sponsors", "/orgs/", "/apps/", "/search"]):
                continue
            # Must look like owner/repo (repo part usually has hyphen or is longer than 4 chars)
            if owner and repo and len(repo) > 3 and path not in repos:
                repos.append(path)
                break
    
    return repos[:max_repos]

def fetch_repo_details(repo_path):
    """Fetch repo details from GitHub API."""
    clean_path = repo_path.lstrip("/")
    api_url = f"https://api.github.com/repos/{clean_path}"
    req = urllib.request.Request(
        api_url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/vnd.github.v3+json"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
            return {
                "full_name": data.get("full_name", clean_path),
                "description": data.get("description") or "无描述",
                "language": data.get("language") or "",
                "stars": data.get("stargazers_count", 0),
                "url": f"https://github.com/{clean_path}"
            }
    except Exception as e:
        return {
            "full_name": clean_path,
            "description": "获取详情失败",
            "language": "",
            "stars": 0,
            "url": f"https://github.com/{clean_path}",
            "error": str(e)
        }

def main():
    lang_filter = None
    if len(sys.argv) > 1 and sys.argv[1] not in ("--", "-h", "--help"):
        lang_filter = sys.argv[1]
        url = f"https://github.com/trending?since={lang_filter}"
    else:
        url = "https://github.com/trending"
    
    html_content = fetch_trending_page()
    repos = extract_repos(html_content, max_repos=10)
    
    if not repos:
        # Fallback: try to get from known trending repos
        repos = [
            "protocolbuffers/protobuf",
            "vllm-project/vllm",
            "aquasecurity/trivy",
            "FujiwaraChoki/MoneyPrinterV2",
            "louis-e/arnis",
            "jarrodwatts/claude-hud",
            "systemd/systemd",
            "opendataloader-project/opendataloader-pdf",
            "Crosstalk-Solutions/project-nomad",
        ]
    
    results = []
    for repo in repos:
        details = fetch_repo_details(repo)
        results.append(details)
    
    print(json.dumps(results, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
