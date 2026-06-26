#!/usr/bin/env python3

import subprocess
import json
import os
from jira import JIRA

# --- Config (from Skill's references/jira.md) ---
JIRA_URL = os.environ.get("JIRA_BASE_URL", "https://attrix-team.atlassian.net/")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL", "xwang@attrix.ca")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN", "ATATT3xFfGF0gANHYusgbB1HN1O0zjq28HsoA6n9Ic_DAbR55eNqC22RJ6UYrhN5gMtIBWigyGtOnClmkigWkIsS33H6F3pr8cLSZY62o6MSpk3k0_lVqVDQ4bsj4h-VPk1_pxAbVrQUqFlH-FTJmGW2jfnM9dAvGzduxUucHQUjmOVTH1Kaa1w=B3626842")

async def get_issue_description(issue_key: str) -> dict:
    try:
        jira_options = {"server": JIRA_URL}
        jira = JIRA(options=jira_options, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))

        issue = jira.issue(issue_key)
        summary = issue.fields.summary
        description = issue.fields.description if issue.fields.description else "No description provided."
        
        return {"success": True, "key": issue_key, "summary": summary, "description": description}

    except Exception as e:
        return {"success": False, "error": str(e)}

# Example usage (for testing)
# if __name__ == "__main__":
#     import asyncio
#     result = asyncio.run(get_issue_description("DS-413"))
#     print(json.dumps(result, indent=2))
