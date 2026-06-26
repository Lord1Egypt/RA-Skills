#!/usr/bin/env python3
"""
update_issue.py — Update fields on an existing Jira issue.

Usage (CLI):
    python update_issue.py --key DS-123 [field options]

Field options (at least one required):
    --summary     New summary/title
    --description New description text
    --priority    New priority name (e.g. High / Medium / Low)
    --assignee    Assignee account ID (use 'none' to unassign)
    --labels      Comma-separated labels (replaces existing labels)
    --due-date    Due date in YYYY-MM-DD format
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


def update_issue(
    issue_key: str,
    summary: str = None,
    description: str = None,
    priority: str = None,
    assignee_id: str = None,
    labels: list = None,
    due_date: str = None,
) -> dict:
    """Update one or more fields on an existing Jira issue."""
    try:
        jira = JIRA(options={"server": JIRA_URL}, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))
        issue = jira.issue(issue_key.upper())

        fields = {}
        if summary is not None:
            fields["summary"] = summary
        if description is not None:
            fields["description"] = description
        if priority is not None:
            fields["priority"] = {"name": priority}
        if labels is not None:
            fields["labels"] = labels
        if due_date is not None:
            fields["duedate"] = due_date

        if fields:
            issue.update(fields=fields)

        # Assignee requires separate call
        if assignee_id is not None:
            if assignee_id.lower() == "none":
                jira.assign_issue(issue, None)
            else:
                jira.assign_issue(issue, assignee_id)

        if not fields and assignee_id is None:
            return {"success": False, "error": "No fields provided to update."}

        return {
            "success": True,
            "key": issue_key.upper(),
            "updated_fields": list(fields.keys()) + (["assignee"] if assignee_id else []),
            "url": f"{JIRA_URL.rstrip('/')}/browse/{issue_key.upper()}",
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update a Jira issue")
    parser.add_argument("--key", required=True, help="Issue key, e.g. DS-123")
    parser.add_argument("--summary", default=None)
    parser.add_argument("--description", default=None)
    parser.add_argument("--priority", default=None)
    parser.add_argument("--assignee", default=None)
    parser.add_argument("--labels", default=None)
    parser.add_argument("--due-date", dest="due_date", default=None)
    args = parser.parse_args()

    labels_list = [l.strip() for l in args.labels.split(",")] if args.labels else None
    result = update_issue(
        issue_key=args.key,
        summary=args.summary,
        description=args.description,
        priority=args.priority,
        assignee_id=args.assignee,
        labels=labels_list,
        due_date=args.due_date,
    )
    print(json.dumps(result, indent=2))

