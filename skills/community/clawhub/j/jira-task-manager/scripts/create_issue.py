#!/usr/bin/env python3
"""
create_issue.py — Create a new Jira issue.

Usage (CLI):
    python create_issue.py --project DS --type Task --summary "My task title" [options]

Options:
    --project     Project key (e.g. DS)            [required]
    --type        Issue type (Task/Bug/Story/Epic)  [required]
    --summary     Issue summary/title               [required]
    --description Issue description text            [optional]
    --priority    Priority name (e.g. High/Medium)  [optional]
    --assignee    Assignee account ID or email      [optional]
    --labels      Comma-separated labels            [optional]
    --parent      Parent issue key for subtasks     [optional]
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


def create_issue(
    project: str,
    issue_type: str,
    summary: str,
    description: str = None,
    priority: str = None,
    assignee_id: str = None,
    labels: list = None,
    parent_key: str = None,
) -> dict:
    """Create a new Jira issue and return the created issue key and URL."""
    try:
        jira = JIRA(options={"server": JIRA_URL}, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))

        fields = {
            "project": {"key": project},
            "issuetype": {"name": issue_type},
            "summary": summary,
        }
        if description:
            fields["description"] = description
        if priority:
            fields["priority"] = {"name": priority}
        if assignee_id:
            fields["assignee"] = {"id": assignee_id}
        if labels:
            fields["labels"] = labels
        if parent_key:
            fields["parent"] = {"key": parent_key}

        new_issue = jira.create_issue(fields=fields)
        return {
            "success": True,
            "key": new_issue.key,
            "url": f"{JIRA_URL.rstrip('/')}/browse/{new_issue.key}",
            "summary": summary,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Jira issue")
    parser.add_argument("--project", default=PRIMARY_PROJECT_KEY)
    parser.add_argument("--type", dest="issue_type", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--description", default=None)
    parser.add_argument("--priority", default=None)
    parser.add_argument("--assignee", default=None)
    parser.add_argument("--labels", default=None)
    parser.add_argument("--parent", default=None)
    args = parser.parse_args()

    labels_list = [l.strip() for l in args.labels.split(",")] if args.labels else None
    result = create_issue(
        project=args.project,
        issue_type=args.issue_type,
        summary=args.summary,
        description=args.description,
        priority=args.priority,
        assignee_id=args.assignee,
        labels=labels_list,
        parent_key=args.parent,
    )
    print(json.dumps(result, indent=2))

