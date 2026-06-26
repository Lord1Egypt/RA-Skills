"""
GitHub Team Collaboration Toolkit
Author: ClawHub Skill
"""

import os
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dateutil import parser

GITHUB_API_BASE = "https://api.github.com"


def get_github_token() -> str:
    """Get GitHub token from environment variable"""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable not set")
    return token


def get_headers() -> Dict[str, str]:
    """Get request headers with authentication"""
    return {
        "Authorization": f"token {get_github_token()}",
        "Accept": "application/vnd.github.v3+json"
    }


def list_open_prs(owner: str, repo: str) -> List[Dict]:
    """
    List all open pull requests in a repository.
    
    Args:
        owner: Repository owner/organization
        repo: Repository name
    
    Returns:
        List of pull request dictionaries
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls"
    params = {"state": "open", "per_page": 100}
    
    response = requests.get(url, headers=get_headers(), params=params)
    
    if response.status_code == 200:
        return response.json()
    else:
        return [{"error": response.text, "status_code": response.status_code}]


def assign_reviewers(owner: str, repo: str, pr_number: int, reviewers: List[str]) -> Dict:
    """
    Assign reviewers to a pull request.
    
    Args:
        owner: Repository owner/organization
        repo: Repository name
        pr_number: Pull request number
        reviewers: List of reviewer usernames
    
    Returns:
        Response dictionary
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls/{pr_number}/requested_reviewers"
    data = {"reviewers": reviewers}
    
    response = requests.post(url, headers=get_headers(), json=data)
    
    if response.status_code == 201:
        return {"status": "success", "reviewers_assigned": reviewers}
    else:
        return {"error": response.text, "status_code": response.status_code}


def get_milestone_progress(owner: str, repo: str, milestone_title: str) -> Dict:
    """
    Get progress statistics for a milestone.
    
    Args:
        owner: Repository owner/organization
        repo: Repository name
        milestone_title: Title of the milestone
    
    Returns:
        Dictionary with milestone progress data
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/milestones"
    params = {"state": "all", "per_page": 100}
    
    response = requests.get(url, headers=get_headers(), params=params)
    
    if response.status_code == 200:
        milestones = response.json()
        for milestone in milestones:
            if milestone["title"] == milestone_title:
                return {
                    "title": milestone["title"],
                    "state": milestone["state"],
                    "total_issues": milestone["open_issues"] + milestone["closed_issues"],
                    "open_issues": milestone["open_issues"],
                    "closed_issues": milestone["closed_issues"],
                    "progress_percent": (milestone["closed_issues"] / 
                        (milestone["open_issues"] + milestone["closed_issues"]) * 100)
                        if (milestone["open_issues"] + milestone["closed_issues"]) > 0 else 0,
                    "due_on": milestone.get("due_on"),
                    "html_url": milestone["html_url"]
                }
        return {"error": f"Milestone '{milestone_title}' not found"}
    else:
        return {"error": response.text, "status_code": response.status_code}


def get_team_metrics(owner: str, repo: str, days: int = 30) -> Dict:
    """
    Calculate team collaboration metrics.
    
    Args:
        owner: Repository owner/organization
        repo: Repository name
        days: Number of days to analyze (default 30)
    
    Returns:
        Dictionary with team metrics
    """
    since = (datetime.now() - timedelta(days=days)).isoformat()
    
    # Get closed PRs
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/pulls"
    params = {"state": "closed", "per_page": 100, "sort": "updated", "direction": "desc"}
    
    response = requests.get(url, headers=get_headers(), params=params)
    
    if response.status_code != 200:
        return {"error": response.text, "status_code": response.status_code}
    
    prs = response.json()
    
    # Filter by date
    recent_prs = [pr for pr in prs 
                  if pr.get("closed_at") and parser.parse(pr["closed_at"]) > parser.parse(since)]
    
    if not recent_prs:
        return {"message": "No closed PRs in the specified time period"}
    
    # Calculate metrics
    review_times = []
    contributor_counts = {}
    
    for pr in recent_prs:
        created = parser.parse(pr["created_at"])
        closed = parser.parse(pr["closed_at"])
        review_time = (closed - created).total_seconds() / 3600  # Hours
        review_times.append(review_time)
        
        user = pr["user"]["login"]
        contributor_counts[user] = contributor_counts.get(user, 0) + 1
    
    return {
        "period_days": days,
        "total_prs_closed": len(recent_prs),
        "avg_review_time_hours": round(sum(review_times) / len(review_times), 2),
        "median_review_time_hours": round(sorted(review_times)[len(review_times)//2], 2),
        "contributors": contributor_counts,
        "top_contributor": max(contributor_counts.items(), key=lambda x: x[1]) if contributor_counts else None
    }


def list_issues(owner: str, repo: str, state: str = "open") -> List[Dict]:
    """
    List issues in a repository.
    
    Args:
        owner: Repository owner/organization
        repo: Repository name
        state: Issue state (open, closed, all)
    
    Returns:
        List of issue dictionaries
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues"
    params = {"state": state, "per_page": 100}
    
    response = requests.get(url, headers=get_headers(), params=params)
    
    if response.status_code == 200:
        # Filter out pull requests
        issues = [issue for issue in response.json() if "pull_request" not in issue]
        return issues
    else:
        return [{"error": response.text, "status_code": response.status_code}]


def create_issue(owner: str, repo: str, title: str, body: str = "", 
                 labels: List[str] = None, assignees: List[str] = None) -> Dict:
    """
    Create a new issue.
    
    Args:
        owner: Repository owner/organization
        repo: Repository name
        title: Issue title
        body: Issue description
        labels: List of label names
        assignees: List of assignee usernames
    
    Returns:
        Created issue dictionary
    """
    url = f"{GITHUB_API_BASE}/repos/{owner}/{repo}/issues"
    data = {"title": title, "body": body}
    
    if labels:
        data["labels"] = labels
    if assignees:
        data["assignees"] = assignees
    
    response = requests.post(url, headers=get_headers(), json=data)
    
    if response.status_code == 201:
        return response.json()
    else:
        return {"error": response.text, "status_code": response.status_code}


if __name__ == "__main__":
    print("GitHub Team Collaboration Toolkit")
    print("=" * 50)
    
    # Test functions (requires GITHUB_TOKEN)
    try:
        token = get_github_token()
        print(f"GitHub token found: {token[:10]}...")
    except ValueError as e:
        print(f"Warning: {e}")
