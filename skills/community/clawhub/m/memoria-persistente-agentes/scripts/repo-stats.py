#!/usr/bin/env python3
"""Check GitHub repo stats: stars, forks, issues, downloads.

Run periodically to monitor adoption.
"""
import json
import sys
from pathlib import Path

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def check_stats():
    import subprocess
    result = subprocess.run(
        ["C:\\Program Files\\GitHub CLI\\gh.exe", "repo", "view", "renateparma/memoria-persistente-openclaw", "--json", "stargazerCount,forkCount,issues,pullRequests,description"],
        capture_output=True, text=True, encoding="utf-8"
    )
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return
    
    data = json.loads(result.stdout)
    stars = data.get("stargazerCount", 0)
    forks = data.get("forkCount", 0)
    issues = len(data.get("issues", []))
    prs = len(data.get("pullRequests", []))
    
    print(f"⭐ Stars: {stars}")
    print(f"🍴 Forks: {forks}")
    print(f"📋 Issues: {issues}")
    print(f"🔀 PRs: {prs}")
    
    if issues > 0:
        print("\nOpen issues:")
        for issue in data["issues"]:
            print(f"  #{issue['number']} — {issue['title']}")

if __name__ == "__main__":
    check_stats()