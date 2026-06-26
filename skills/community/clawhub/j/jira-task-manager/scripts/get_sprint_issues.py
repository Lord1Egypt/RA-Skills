#!/usr/bin/env python3
"""
get_sprint_issues.py — List all issues in the active sprint for a project.

Usage (CLI):
    python get_sprint_issues.py [--project DS] [--assignee-only]

Options:
    --project        Project key (default: DS)
    --assignee-only  Only show issues assigned to the configured user
    --status         Filter by status name (e.g. "In Progress")
"""

import sys
import os
import json
import argparse
from jira import JIRA

# --- Config (from Skill's references/jira.md) ---
JIRA_URL = os.environ.get("JIRA_BASE_URL", "https://attrix-team.atlassian.net/")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL", "xwang@attrix.ca")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN", "ATATT3xFfGF0gANHYusgbB1HN1O0zjq28HsoA6n9Ic_DAbR55eNqC22RJ6UYrhN5gMtIBWigyGtOnClmkigWkIsS33H6F3pr8cLSZY62o6MSpk3k0_lVqVDQ4bsj4h-VPk1_pxAbVrQUqFlH-FTJmGW2jfnM9dAvGzduxUucHQUjmOVTH1Kaa1w=B3626842")
PRIMARY_PROJECT_KEY = "DS"


def get_sprint_issues(
    project: str = PRIMARY_PROJECT_KEY,
    assignee_only: bool = False,
    status_filter: str = None,
) -> dict:
    """Fetch all issues in the current active sprint for the given project."""
    try:
        jira = JIRA(options={"server": JIRA_URL}, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))

        jql_parts = [f'project = "{project}"', "sprint in openSprints()"]
        if assignee_only:
            jql_parts.append("assignee = currentUser()")
        if status_filter:
            jql_parts.append(f'status = "{status_filter}"')

        jql = " AND ".join(jql_parts) + " ORDER BY rank ASC"
        issues = jira.search_issues(jql, maxResults=100)

        issue_list = []
        for issue in issues:
            f = issue.fields
            issue_list.append({
                "key": issue.key,
                "summary": f.summary,
                "status": f.status.name,
                "status_category": f.status.statusCategory.name,
                "issue_type": f.issuetype.name,
                "assignee": f.assignee.displayName if f.assignee else None,
                "priority": f.priority.name if f.priority else None,
                "url": f"{JIRA_URL.rstrip('/')}/browse/{issue.key}",
            })

        return {
            "success": True,
            "project": project,
            "sprint": "Active Sprint",
            "total": len(issue_list),
            "issues": issue_list,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List issues in the active sprint")
    parser.add_argument("--project", default=PRIMARY_PROJECT_KEY)
    parser.add_argument("--assignee-only", action="store_true")
    parser.add_argument("--status", default=None)
    args = parser.parse_args()

    result = get_sprint_issues(
        project=args.project,
        assignee_only=args.assignee_only,
        status_filter=args.status,
    )
    print(json.dumps(result, indent=2))

