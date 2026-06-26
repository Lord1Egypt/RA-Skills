#!/usr/bin/env python3
"""
Search OpenClaw GitHub repository for relevant information.
This script uses the GitHub CLI (gh) to search issues, PRs, and code.
"""

import subprocess
import sys
import json
from typing import List, Dict

def search_github_repo(query: str, search_type: str = "code") -> List[Dict]:
    """
    Search the OpenClaw GitHub repository.
    
    Args:
        query: Search query string
        search_type: Type of search - 'code', 'issues', 'prs', 'discussions'
    
    Returns:
        List of search results with relevant information
    """
    repo = "openclaw/openclaw"
    
    if search_type == "code":
        # Search code in the repository
        cmd = ["gh", "search", "code", "--repo", repo, query]
    elif search_type == "issues":
        # Search issues
        cmd = ["gh", "search", "issues", "--repo", repo, query]
    elif search_type == "prs":
        # Search pull requests  
        cmd = ["gh", "search", "prs", "--repo", repo, query]
    elif search_type == "discussions":
        # Search discussions
        cmd = ["gh", "search", "discussions", "--repo", repo, query]
    else:
        raise ValueError(f"Unknown search type: {search_type}")
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return {"success": True, "output": result.stdout, "error": None}
    except subprocess.CalledProcessError as e:
        return {"success": False, "output": None, "error": e.stderr}
    except FileNotFoundError:
        return {"success": False, "output": None, "error": "GitHub CLI (gh) not found. Please install it."}

def get_file_content(file_path: str) -> str:
    """
    Get specific file content from the repository.
    """
    cmd = ["gh", "api", f"repos/openclaw/openclaw/contents/{file_path}"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        if "content" in data:
            import base64
            return base64.b64decode(data["content"]).decode("utf-8")
        return ""
    except Exception as e:
        return f"Error fetching file: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 search_github.py <query> [search_type]")
        print("Search types: code, issues, prs, discussions")
        sys.exit(1)
    
    query = sys.argv[1]
    search_type = sys.argv[2] if len(sys.argv) > 2 else "code"
    
    results = search_github_repo(query, search_type)
    if results["success"]:
        print(results["output"])
    else:
        print(f"Error: {results['error']}")