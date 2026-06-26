---
name: git-log-intelligence
description: Fetch, filter, and summarize GitHub repository activity without cloning. Use whenever the user asks what changed in a repo, wants a changelog summary, asks about recent commits or PRs, or wants to tune out noisy commit patterns. Maintains a persistent ignore list to hide bot/CI/chore noise automatically.
metadata: { "openclaw": { "requires": { "bins": ["gh"], "env": ["GITHUB_PERSONAL_ACCESS_TOKEN"] } } }
---

## Prerequisites
- `gh` CLI installed. Authenticate via one of:
  - `GITHUB_PERSONAL_ACCESS_TOKEN` environment variable (required)
- For read-only public repo access, grant only the `public_repo` scope.
  For private repos, use `repo` scope.
- Note: this skill creates `.config/git_filters.json` relative to the script's
  location to persist ignore patterns. Delete this file to reset to defaults.

## Compatibility
- **Required tools:** `gh`
- **Environment variables:**
  - `GITHUB_PERSONAL_ACCESS_TOKEN` (required): GitHub Personal Access Token. Grant minimal scopes: `public_repo` for public repos, `repo` for private repos.

## Directory Structure
- `git_log_intelligence.py`: The primary script containing execution logic.
- `.config/git_filters.json`: The persistent memory of ignore patterns.

## Capabilities

### 1. Summarize Repo Changes
Fetches the last N days of commits and filters them against the "Ignore List."
Command: `python3 skills/git_log_intelligence.py summarize OWNER/REPO DAYS`

### Agent Logic:
Call the script with the repo name and timeframe.
Receive a filtered list of "Important" commits.
Present a natural language summary to the user, noting how many noisy commits were hidden.

### 2. Maintaining and Updating the Ignore List
The agent can add new patterns to the ignore list based on user feedback.
Command: `python3 skills/git_log_intelligence.py ignore "PATTERN"`

The agent can also show the current ignore patterns or remove specific ones.
Command: `python3 skills/git_log_intelligence.py show`

The agent can remove a pattern with:
Command: `python3 skills/git_log_intelligence.py remove "PATTERN"`

### Usage Example:
  1. User: "Claw, stop showing me commits from 'GitHub Actions' or anything starting with 'ci:'."
  2. Agent: Runs python3 skills/git_log_intelligence.py ignore "GitHub Actions" and python3 skills/git_log_intelligence.py ignore "^ci:".

  3. User: "Show me the current ignore patterns."
  4. Agent: Runs python3 skills/git_log_intelligence.py show

  5. User: "Remove the ignore pattern for 'GitHub Actions'."
  6. Agent: Runs python3 skills/git_log_intelligence.py remove "GitHub Actions"


### Technical implementation:
See the `git_log_intelligence.py` script for the full code, but the key functions are:

1. Quick Scan (Default):
  `python3 skills/git_log_intelligence.py summarize OWNER/REPO DAYS`

2. Deep Context (Full Messages):
  `python3 skills/git_log_intelligence.py summarize OWNER/REPO DAYS --full`

Note to Agent:

Use --full when the user asks for a "detailed summary," "technical breakdown," or "why" things were changed. Use the default mode for a "quick list" or "recent activity check."
You can also ask the user if they want the full context after showing the quick summary.


## How It Works
The script uses `gh api` to fetch commits via the GitHub REST API
(`/repos/{owner}/{repo}/commits`), filters them client-side against
`.config/git_filters.json`, and outputs structured text for the agent
to summarize.


### Troubleshooting
If the script exits non-zero, check gh auth status first.


## User Interaction Flow
  1. Request: "What's new in tailscale/tailscale this week?"
  2. Execution: Agent runs `python3 skills/git_log_intelligence.py summarize tailscale/tailscale 7`.
  3. Feedback: "Too much noise from the build bot."
  4. Learning: Agent runs `python3 skills/git_log_intelligence.py ignore "build bot"`.
  5. Next Time: The build bot commits are gone forever.
