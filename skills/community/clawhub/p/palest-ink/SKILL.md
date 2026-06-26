---
name: palest-ink
description: >
  Track and recall your daily activities including git commits, web browsing,
  shell commands, and VS Code edits. Use this skill whenever the user asks about
  their recent activity, wants a daily report or summary, asks "what did I do
  today/yesterday/this week", wants to find a specific commit or webpage they
  visited, asks about browsing history, needs to recall any past work activity,
  or queries about specific content they viewed online. Also trigger when the
  user mentions palest-ink, activity tracking, daily log, work journal, daily
  report, or activity summary. Trigger for questions like "which website had
  info about X", "when did I commit the code for Y", "show my git activity".
tools: Read, Glob, Grep, Bash
---

# Palest Ink (淡墨) — Activity Tracker & Daily Reporter

> 好记性不如烂笔头 — The faintest ink is better than the strongest memory.

## Overview

Palest Ink tracks the user's daily activities automatically:
- **Git operations**: commits, pushes, pulls, branch switches
- **Web browsing**: Chrome & Safari history with page content summaries
- **Shell commands**: zsh/bash command history with execution duration
- **VS Code edits**: recently opened/edited files
- **App focus**: which application is in the foreground, with time duration
- **File changes**: files modified in watched directories

All data is stored locally at `~/.palest-ink/data/YYYY/MM/DD.jsonl`.

## Setup Check

Before answering any query, first check if Palest Ink is installed:

```bash
test -f ~/.palest-ink/config.json && echo "INSTALLED" || echo "NOT_INSTALLED"
```

If NOT installed, tell the user:
> Palest Ink is not yet set up. To install, run:
> ```bash
> bash <SKILL_PATH>/../../collectors/install.sh
> ```
> This will set up automatic tracking of git, browsing, and shell activity.

Then stop and wait for the user to install.

## Answering Queries

### Daily Report / "What did I do today?"

Run the report generator:

```bash
python3 <SKILL_PATH>/scripts/report.py --date today
```

For yesterday: `--date yesterday`
For a specific date: `--date 2026-03-03`
For the whole week: `--week`

Read the output and present it conversationally to the user. Highlight notable patterns
(focused work sessions, frequent topics, etc).

### Searching for Specific Activities

Use the query tool to search activity records:

```bash
python3 <SKILL_PATH>/scripts/query.py --date today --type git_commit --search "plugin"
```

**Common query patterns:**

| User asks about... | Arguments |
|---------------------|-----------|
| A git commit | `--type git_commit --search "keyword"` |
| A webpage about X | `--type web_visit --search-content "keyword"` |
| Shell commands | `--type shell_command --search "keyword"` |
| VS Code files | `--type vscode_edit --search "keyword"` |
| App focus / screen time | `--type app_focus --summary` |
| File changes in project | `--type file_change --search "project"` |
| Everything today | `--date today --summary` |
| Date range | `--from 2026-03-01 --to 2026-03-07` |

**Important:** When the user searches for web page content (e.g., "which website talked about homebrew"),
use `--search-content` instead of `--search`. This searches within page content summaries and keywords,
not just URLs and titles.

### Status Check

Show collector status and data statistics:

```bash
python3 <SKILL_PATH>/scripts/status.py
```

If the output contains "CLEANUP RECOMMENDED", proactively tell the user:
> "Your palest-ink data is approaching 2 GB. Would you like me to clean up older records?"

If the user agrees, first show a dry-run preview:

```bash
python3 ~/.palest-ink/bin/cleanup.py --dry-run
```

Present the preview (how many files, date range, records count, space to free).
Then ask for explicit confirmation before actually deleting:

```bash
python3 ~/.palest-ink/bin/cleanup.py --force
```

Options:
- `--max-size N` — threshold in GB (default: 2.0)
- `--keep-days N` — always keep the most recent N days (default: 30)
- `--dry-run` — preview only, no changes
- `--force` — skip the interactive prompt (use after user confirms in chat)

## Fallback: Direct File Reading

If scripts fail or for simple lookups, read the JSONL files directly:

1. Construct the file path: `~/.palest-ink/data/YYYY/MM/DD.jsonl`
2. Use Grep to search: `grep "keyword" ~/.palest-ink/data/2026/03/03.jsonl`
3. Each line is a JSON object with fields: `ts`, `type`, `source`, `data`

## Data Schema

### Activity Types

- `git_commit` — data: repo, branch, hash, message, files_changed, insertions, deletions
- `git_push` — data: repo, branch, remote, remote_url
- `git_pull` — data: repo, branch, is_squash
- `git_checkout` — data: repo, from_ref, to_branch
- `web_visit` — data: url, title, visit_duration_seconds, browser, content_summary, content_keywords
- `shell_command` — data: command, duration_seconds (null if not available)
- `vscode_edit` — data: file_path, workspace, language
- `app_focus` — data: app_name, window_title, duration_seconds
- `file_change` — data: path, workspace, language, event

### Web Visit Content

Web visits include a `content_summary` field (up to 800 chars of page text) and
`content_keywords` (extracted keywords). This enables content-based search.

Example: if user browsed a page about "Homebrew installation guide", the content_summary
will contain the actual page text, making it searchable even if the URL/title don't mention it.

## Tips for Good Answers

1. When showing git activity, include the commit message and changed files
2. When showing web visits, include both the title and a brief content summary
3. For "what did I do" questions, give a narrative summary, not just raw data
4. Group related activities together (e.g., "You worked on project X, making 5 commits...")
5. If the search returns too many results, help the user narrow down
6. Mention the time of activities to give temporal context
