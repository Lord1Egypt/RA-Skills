#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitLab Code Review - Fetch Commits

Get unreviewed commits and save to pending files.
"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json
import urllib.parse
import os
from pathlib import Path
from datetime import datetime

# Clear any cached environment variables
for key in ["GITLAB_URL", "GITLAB_TOKEN", "GITLAB_PROJECT", "GITLAB_BRANCH"]:
    os.environ.pop(key, None)

# Load .env file
# Script: workspace/skills/gitlab-code-review/scripts/fetch_commits.py
# .env: workspace/.env
WORKSPACE_DIR = Path(__file__).parent.parent.parent.parent  # Go up 4 levels to workspace
ENV_FILE = WORKSPACE_DIR / ".env"

try:
    from dotenv import load_dotenv
    load_dotenv(ENV_FILE, override=True)
except ImportError:
    if ENV_FILE.exists():
        with open(ENV_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()

# Read config from environment
GITLAB_URL = os.getenv("GITLAB_URL", "https://gitlab.example.com")
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN", "")
PROJECT_PATH = os.getenv("GITLAB_PROJECT", "")
BRANCH = os.getenv("GITLAB_BRANCH", "main")

OUTPUT_DIR = WORKSPACE_DIR / "memory"
STATE_FILE = OUTPUT_DIR / "gitlab_review_state.json"


def validate_config():
    """Validate configuration"""
    missing = []
    if not GITLAB_TOKEN:
        missing.append("GITLAB_TOKEN")
    if not PROJECT_PATH:
        missing.append("GITLAB_PROJECT")

    if missing:
        print(f"Error: Missing config: {', '.join(missing)}")
        print(f"Please configure in {ENV_FILE}")
        return False
    return True


def load_state():
    """Load state"""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"last_check": None, "last_reviewed_commit_id": None}


def save_state(state):
    """Save state"""
    state["last_check"] = datetime.now().isoformat()
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)


def get_project_id(headers):
    """Get project ID"""
    encoded_path = urllib.parse.quote(PROJECT_PATH, safe="")
    url = f"{GITLAB_URL}/api/v4/projects/{encoded_path}"
    response = requests.get(url, headers=headers, timeout=10, proxies={"http": None, "https": None})
    data = response.json()
    if "id" not in data:
        print(f"Error: {data.get('error', 'Unknown error')}")
        print(f"Response: {response.text[:200]}")
        return None
    return data["id"]


def get_commits(project_id, headers, limit=50):
    """Get recent commits"""
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/repository/commits"
    response = requests.get(
        url, headers=headers, params={"per_page": limit, "ref_name": BRANCH}, timeout=10, proxies={"http": None, "https": None}
    )
    return response.json()


def get_commit_diff(project_id, commit_id, headers):
    """Get commit diff"""
    url = f"{GITLAB_URL}/api/v4/projects/{project_id}/repository/commits/{commit_id}/diff"
    response = requests.get(url, headers=headers, timeout=10, proxies={"http": None, "https": None})
    return response.json()


def prepare_commit_data(project_id, commit, headers):
    """Prepare commit data for review"""
    diffs = get_commit_diff(project_id, commit["id"], headers)

    review_data = {
        "project": PROJECT_PATH,
        "project_id": project_id,
        "branch": BRANCH,
        "commit": {
            "id": commit["id"],
            "short_id": commit["short_id"],
            "title": commit["title"],
            "author": commit["author_name"],
            "time": commit["created_at"],
            "message": commit["message"],
            "url": commit["web_url"],
        },
        "changes": [],
    }

    for diff in diffs:
        review_data["changes"].append(
            {
                "file": diff["new_path"],
                "new_file": diff.get("new_file", False),
                "deleted_file": diff.get("deleted_file", False),
                "renamed_file": diff.get("renamed_file", False),
                "diff": diff["diff"],
            }
        )

    return review_data


def main():
    if not validate_config():
        return

    headers = {"Private-Token": GITLAB_TOKEN}

    state = load_state()
    last_reviewed_id = state.get("last_reviewed_commit_id")

    print(f"GitLab URL: {GITLAB_URL}")
    print(f"Project: {PROJECT_PATH}")
    print(f"Branch: {BRANCH}")
    print(f"Last reviewed: {last_reviewed_id}")
    print()

    project_id = get_project_id(headers)
    if not project_id:
        return

    print(f"Project ID: {project_id}")

    commits = get_commits(project_id, headers)

    if not commits:
        print("No commits found")
        return

    print(f"Found {len(commits)} commits in branch")

    new_commits = []
    for commit in commits:
        if commit["id"] == last_reviewed_id:
            break
        new_commits.append(commit)

    # First run: only get the latest 2 commits
    if last_reviewed_id is None and len(new_commits) > 2:
        new_commits = new_commits[:2]
        print("(First run: only fetching latest 2 commits)")

    if not new_commits:
        print("No new commits to review")
        return

    new_commits.reverse()
    print(f"Found {len(new_commits)} new commit(s) to review")

    for i, commit in enumerate(new_commits, 1):
        print(f"Processing {i}/{len(new_commits)}: {commit['short_id']}")

        commit_data = prepare_commit_data(project_id, commit, headers)

        output_file = OUTPUT_DIR / f"pending_review_{commit['short_id']}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(commit_data, f, ensure_ascii=False, indent=2)

        print(f"  Saved: {commit['short_id']}")

    state["last_reviewed_commit_id"] = commits[0]["id"]
    save_state(state)

    print(f"\nDone: {len(new_commits)} commit(s) prepared for review")
    print(f"Updated last reviewed to: {commits[0]['short_id']}")


if __name__ == "__main__":
    main()
