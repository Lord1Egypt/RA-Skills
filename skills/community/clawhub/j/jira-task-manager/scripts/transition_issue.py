#!/usr/bin/env python3
"""
transition_issue.py — Transition a Jira issue to a new status.

Usage (CLI):
    python transition_issue.py --key DS-123 --status "In Progress"
    python transition_issue.py --key DS-123 --list        # list available transitions

Common status names: "To Do", "In Progress", "In Review", "Done"
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


def list_transitions(issue_key: str) -> dict:
    """List all available transitions for an issue."""
    try:
        jira = JIRA(options={"server": JIRA_URL}, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))
        transitions = jira.transitions(issue_key.upper())
        return {
            "success": True,
            "key": issue_key.upper(),
            "transitions": [{"id": t["id"], "name": t["name"]} for t in transitions],
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def transition_issue(issue_key: str, target_status: str) -> dict:
    """Transition an issue to the target status name (case-insensitive match)."""
    try:
        jira = JIRA(options={"server": JIRA_URL}, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))
        transitions = jira.transitions(issue_key.upper())

        target_lower = target_status.strip().lower()
        matched = next(
            (t for t in transitions if t["name"].strip().lower() == target_lower), None
        )
        if not matched:
            available = [t["name"] for t in transitions]
            return {
                "success": False,
                "error": f"No transition named '{target_status}' found.",
                "available_transitions": available,
            }

        jira.transition_issue(issue_key.upper(), matched["id"])
        return {
            "success": True,
            "key": issue_key.upper(),
            "new_status": matched["name"],
            "url": f"{JIRA_URL.rstrip('/')}/browse/{issue_key.upper()}",
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Transition a Jira issue status")
    parser.add_argument("--key", required=True, help="Issue key, e.g. DS-123")
    parser.add_argument("--status", default=None, help="Target status name")
    parser.add_argument("--list", action="store_true", help="List available transitions")
    args = parser.parse_args()

    if args.list:
        result = list_transitions(args.key)
    elif args.status:
        result = transition_issue(args.key, args.status)
    else:
        result = {"success": False, "error": "Provide --status <name> or --list"}
    print(json.dumps(result, indent=2))

