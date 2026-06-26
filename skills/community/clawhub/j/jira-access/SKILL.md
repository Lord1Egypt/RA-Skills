---
name: jira-access
description: Access a Jira workspace (omeshkshatriya.atlassian.net) using provided email and API token to list, create, and transition issues. Use when the user wants to interact with their Jira instance via commands like "list open bugs" or "create a task". Trigger on any request that mentions Jira operations.
---

# Jira Access Skill

## Overview
This skill provides a thin wrapper around Jira's REST API. It enables the assistant to:
- List issues with JQL filters
- Create new issues
- Transition issues between statuses
- Add comments or attachments

All operations are performed using the credentials supplied via environment variables to avoid storing secrets in source control.

## Setup
1. **Set environment variables** in the runtime where the skill runs.
   *For PowerShell (recommended):*
   ```powershell
   $env:JIRA_DOMAIN = "omeshkshatriya.atlassian.net"
   $env:JIRA_EMAIL = "omeshkshatriya@gmail.com"
   $env:JIRA_API_TOKEN = "ATATT3xFfGF0cks7fxnFIDe..."   # full token (do not truncate)
   ```
   *For Command Prompt (cmd.exe):*
   ```cmd
   set JIRA_DOMAIN=omeshkshatriya.atlassian.net
   set JIRA_EMAIL=omeshkshatriya@gmail.com
   set JIRA_API_TOKEN=ATATT3xFfGF0cks7fxnFIDe...   # full token (do not truncate)
   ```
   > **Security note:** Do not commit these values to the repository. Keep them in a secure profile, a `.env` file, or a CI secret store.

2. Ensure Python 3.9+ is installed on Windows and install the required dependency:
   ```powershell
   pip install requests
   ```

## Usage
The skill is invoked through the `jira` command (a simple batch wrapper) followed by a sub‑command:
- `jira list "project = OMESH"` – List issues matching a JQL query.
- `jira create "Bug" "Summary" "Description"` – Create a new issue of type *Bug*.
- `jira transition <ISSUE-KEY> <STATUS>` – Move an issue to a new status.
- `jira comment <ISSUE-KEY> "Your comment"` – Add a comment.

### Example
Create a small batch wrapper `jira.bat` in the `jira-access` folder to forward arguments to the Python script:
```bat
@echo off
python "%~dp0scripts\jira_cli.py" %*
```
```bash
jira list "assignee = currentUser() AND status = Open"
```
Will output a table of open issues assigned to the current user.

## Implementation Details
The core logic lives in `scripts/jira_cli.py`. It reads the environment variables, builds HTTP requests, and prints JSON‑formatted results. The script is deliberately minimal to keep the skill lightweight.

### Extending the Skill
- Add more sub‑commands in `jira_cli.py` for bulk operations.
- Create reference files under `references/` for advanced JQL patterns.
- Store reusable payload templates in `assets/` if needed.

## When Not to Use
If the user asks for actions outside Jira (e.g., Confluence, Bitbucket) this skill should not be triggered.

---

# References
- [Jira REST API documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)

---
