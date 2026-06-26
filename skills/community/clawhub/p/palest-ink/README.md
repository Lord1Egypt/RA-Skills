# Palest Ink (淡墨)

> 好记性不如烂笔头 — The faintest ink is better than the strongest memory.

A Claude Code skill that automatically tracks your daily development activities and helps you recall what you've done — without lifting a finger.

## Features

### Data Collection (automatic, every 15 seconds via launchd)

| Collector | What it tracks |
|-----------|---------------|
| **Git** | Commits, pushes, pulls, branch switches (via global git hooks + periodic scan) |
| **Browser** | Chrome & Safari history with full page content summaries |
| **Shell** | zsh/bash command history with execution duration |
| **VS Code** | Recently opened/edited files |
| **App Focus** | Which application is in the foreground and how long |
| **File Changes** | Files modified in your watched project directories |

### Reports

Ask Claude *"What did I do today?"* and get a structured daily report including:

- **Timeline** — chronological activity across morning / afternoon / evening / night
- **Git Activity** — commits per repo with line change stats
- **Top Websites** — domains visited with visit counts
- **Files Edited** — VS Code edits grouped by language
- **专注时段 (Focus Sessions)** — continuous blocks of focus on a single app (e.g. "09:00–11:15 Cursor 2h15m")
- **应用使用时长 (App Usage)** — Top 5 apps by time + breakdown by category (development / browser / communication)
- **Shell 命令统计 (Shell Stats)** — most-used commands + slowest commands by duration
- **跨域关联 (Cross-domain Correlation)** — web research topics detected in the 2 hours before each git commit

### Natural Language Search

| You ask | How it's answered |
|---------|-------------------|
| "Which commit touched the auth code?" | Searches `git_commit` records by keyword |
| "Which website had info about Homebrew?" | Searches **page content summaries**, not just titles/URLs |
| "How long did I use Cursor today?" | Queries `app_focus` records and sums duration |
| "What shell commands took more than 30 seconds?" | Queries `shell_command` with `duration_seconds` |
| "What files changed in the palest-ink project?" | Queries `file_change` records |
| "Show my activity from last Monday to Wednesday" | Date-range query across multiple days |

## Installation

### 1. Install the collectors

```bash
bash collectors/install.sh
```

This will:
- Create `~/.palest-ink/` for storing activity data
- Write a default `config.json`
- Install git hooks globally (`post-commit`, `post-merge`, `post-checkout`, `pre-push`)
- Install a **launchd agent** that runs every 15 seconds (replaces cron)

### 2. Grant permissions

**Full Disk Access** (for Safari history):
> System Settings → Privacy & Security → Full Disk Access → enable Terminal.app

**Accessibility** (for app focus tracking):
> System Settings → Privacy & Security → Accessibility → enable Terminal.app

### 3. Install as a Claude Code skill

Add the skill to your Claude Code settings by pointing to the `skills/` directory, or follow Claude Code's plugin installation instructions.

### 4. (Optional) Configure watched directories

Edit `~/.palest-ink/config.json` to set which directories to monitor for file changes:

```json
"watched_dirs": ["/Users/you/projects/myapp", "/Users/you/work"]
```

If `watched_dirs` is empty, the file change collector falls back to `tracked_repos`.

## Usage Examples

Once installed, just talk to Claude:

```
"今天做了什么？"
"What did I do today?"
"Show my git activity this week"
"Which website had information about JWT authentication?"
"How long was I in Cursor vs Chrome today?"
"What files did I change in the palest-ink project today?"
"Which shell commands took the longest to run this week?"
"Show me what I researched before my last commit"
```

## Data Storage

All data stays local on your machine — nothing leaves your machine.

```
~/.palest-ink/
├── config.json            # Configuration and collector state
├── data/
│   └── YYYY/MM/DD.jsonl   # Activity records (one JSON object per line)
├── reports/               # Saved report files
├── hooks/                 # Git hook scripts
├── bin/                   # Collector scripts (copied from collectors/)
├── tmp/                   # Lock files, marker files, temp files
└── cron.log               # Collection log
```

Each record follows a common schema:

```json
{
  "ts": "2026-03-03T09:14:22+00:00",
  "type": "git_commit",
  "source": "git_hook",
  "data": { ... }
}
```

Supported types: `git_commit`, `git_push`, `git_pull`, `git_checkout`, `web_visit`, `shell_command`, `vscode_edit`, `app_focus`, `file_change`.

See [`skills/palest-ink/references/schema.md`](skills/palest-ink/references/schema.md) for full field definitions.

## Configuration

`~/.palest-ink/config.json` — key fields:

```json
{
  "collectors": {
    "chrome": true,
    "safari": true,
    "shell": true,
    "vscode": true,
    "git_hooks": true,
    "git_scan": true,
    "content": true,
    "app": true,
    "fsevent": true
  },
  "tracked_repos": ["/path/to/repo"],
  "watched_dirs": [],
  "exclude_patterns": {
    "urls": ["chrome://", "chrome-extension://", "about:", "file://"],
    "commands": ["^ls$", "^cd ", "^clear$", "^pwd$", "^exit$", "^history"]
  },
  "content_fetch": {
    "max_urls_per_run": 50,
    "summary_max_chars": 800,
    "timeout_seconds": 10
  },
  "app": {
    "min_focus_seconds": 600,
    "exclude": ["loginwindow", "Dock", "SystemUIServer", "Finder", "ScreenSaverEngine"]
  },
  "app_categories": {
    "development": ["Cursor", "Code", "Xcode", "Terminal", "iTerm2", "Warp"],
    "browser": ["Google Chrome", "Safari", "Firefox", "Arc"],
    "communication": ["Slack", "WeChat", "Discord", "Zoom"]
  }
}
```

## Uninstallation

```bash
bash collectors/uninstall.sh
```

Removes the launchd agent, restores git hooks, and optionally deletes collected data.

## Privacy

- All data is stored **locally** — nothing is sent anywhere
- URL exclusion patterns filter out browser-internal and sensitive pages
- Command exclusion patterns filter out noise (`ls`, `cd`, `clear`, etc.)
- App focus collection skips the lock screen (`loginwindow`, `ScreenSaverEngine`)
- Accessible only to your local user account

## License

MIT
