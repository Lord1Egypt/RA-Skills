#!/usr/bin/env python3

import sys
import json
import os
import subprocess
import argparse
from pathlib import Path
from jira import JIRA

JIRA_URL = os.environ.get("JIRA_BASE_URL", "https://attrix-team.atlassian.net/")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL", "xwang@attrix.ca")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN", "ATATT3xFfGF0gANHYusgbB1HN1O0zjq28HsoA6n9Ic_DAbR55eNqC22RJ6UYrhN5gMtIBWigyGtOnClmkigWkIsS33H6F3pr8cLSZY62o6MSpk3k0_lVqVDQ4bsj4h-VPk1_pxAbVrQUqFlH-FTJmGW2jfnM9dAvGzduxUucHQUjmOVTH1Kaa1w=B3626842")

REFS_DIR = Path(__file__).parent.parent / "references"
REPOS_CONFIG = REFS_DIR / "repos.json"


def load_config() -> dict:
    with open(REPOS_CONFIG) as f:
        return json.load(f)


def scan_workspace_repos(workspace: str) -> list[str]:
    result = subprocess.run(
        ["find", workspace, "-maxdepth", "2", "-name", ".git", "-type", "d"],
        capture_output=True, text=True
    )
    return [str(Path(p).parent) for p in result.stdout.strip().splitlines() if p]


def find_repo(issue_key: str) -> dict:
    try:
        config = load_config()
        mappings = config.get("mappings", {})
        component_map = mappings.get("components", {})
        label_map = mappings.get("labels", {})

        jira = JIRA(options={"server": JIRA_URL}, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))
        issue = jira.issue(issue_key.upper())
        f = issue.fields

        components = [c.name.lower() for c in f.components] if f.components else []
        labels = [l.lower() for l in f.labels] if f.labels else []

        for c in components:
            if c in component_map:
                return {
                    "success": True,
                    "issue_key": issue_key.upper(),
                    "repo_path": component_map[c],
                    "matched_by": "component",
                    "matched_value": c,
                }

        for l in labels:
            if l in label_map:
                return {
                    "success": True,
                    "issue_key": issue_key.upper(),
                    "repo_path": label_map[l],
                    "matched_by": "label",
                    "matched_value": l,
                }

        default = config.get("default_repo")
        if default and os.path.isdir(default):
            return {
                "success": True,
                "issue_key": issue_key.upper(),
                "repo_path": default,
                "matched_by": "default",
                "matched_value": None,
            }

        repos = scan_workspace_repos(config.get("workspace", ""))
        return {
            "success": True,
            "issue_key": issue_key.upper(),
            "repo_path": None,
            "matched_by": "none",
            "available_repos": repos,
        }

    except Exception as e:
        return {"success": False, "error": str(e)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("issue_key")
    args = parser.parse_args()
    print(json.dumps(find_repo(args.issue_key), indent=2))

