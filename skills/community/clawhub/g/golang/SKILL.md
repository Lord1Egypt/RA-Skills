---
name: golang
version: "2.0.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [golang, tool, utility]
description: "Build, test, lint, and format Go projects with integrated dev tooling. Use when compiling binaries, running tests, linting code, or formatting files."
---

# Golang

Developer toolkit for checking, validating, generating, formatting, linting, converting, and managing Go development entries. All operations are logged with timestamps and stored locally for full traceability.

## Commands

| Command | Usage | Description |
|---------|-------|-------------|
| `check` | `golang check <input>` | Record a check entry or view recent checks |
| `validate` | `golang validate <input>` | Record a validation entry or view recent validations |
| `generate` | `golang generate <input>` | Record a generate entry or view recent generations |
| `format` | `golang format <input>` | Record a format entry or view recent formatting operations |
| `lint` | `golang lint <input>` | Record a lint entry or view recent lint results |
| `explain` | `golang explain <input>` | Record an explain entry or view recent explanations |
| `convert` | `golang convert <input>` | Record a convert entry or view recent conversions |
| `template` | `golang template <input>` | Record a template entry or view recent templates |
| `diff` | `golang diff <input>` | Record a diff entry or view recent diffs |
| `preview` | `golang preview <input>` | Record a preview entry or view recent previews |
| `fix` | `golang fix <input>` | Record a fix entry or view recent fixes |
| `report` | `golang report <input>` | Record a report entry or view recent reports |
| `stats` | `golang stats` | Show summary statistics across all entry types |
| `export <fmt>` | `golang export json\|csv\|txt` | Export all entries to JSON, CSV, or plain text |
| `search <term>` | `golang search <term>` | Search across all log files for a keyword |
| `recent` | `golang recent` | Show the 20 most recent history entries |
| `status` | `golang status` | Health check — version, entry count, disk usage, last activity |
| `help` | `golang help` | Show help with all available commands |
| `version` | `golang version` | Print version string |

Each command (check, validate, generate, format, lint, explain, convert, template, diff, preview, fix, report) works the same way:

- **With arguments:** Saves the input with a timestamp to `<command>.log` and logs to `history.log`.
- **Without arguments:** Displays the 20 most recent entries from `<command>.log`.

## Data Storage

All data is stored locally at `~/.local/share/golang/`:

- `<command>.log` — Timestamped entries for each command (e.g., `check.log`, `lint.log`, `format.log`)
- `history.log` — Unified activity log across all commands
- `export.json`, `export.csv`, `export.txt` — Generated export files

No cloud, no network calls, no API keys required. Fully offline.

## Requirements

- Bash 4+ (uses `set -euo pipefail`)
- Standard Unix utilities (`date`, `wc`, `du`, `grep`, `head`, `tail`, `sed`)
- No external dependencies

## When to Use

1. **Logging Go build and test results** — Use `golang check "go build ./... passed"` or `golang validate "all tests green on v1.4.2"` to record build/test outcomes with timestamps for CI audit trails.
2. **Tracking lint and format operations** — Use `golang lint "golangci-lint found 3 issues in pkg/handler"` and `golang format "gofmt applied to cmd/"` to maintain a history of code quality actions.
3. **Recording code generation and templates** — Use `golang generate "protobuf stubs for api/v2"` and `golang template "new service boilerplate created"` to log what was generated and when.
4. **Searching past development notes** — Use `golang search "handler"` to find all entries across every log file mentioning a specific package, file, or concept.
5. **Exporting development logs for review** — Use `golang export json` to extract all logged entries as structured JSON for team reviews, retrospectives, or integration with project management tools.

## Examples

```bash
# Record a check entry
golang check "go vet ./... clean on main branch"

# Record a lint finding
golang lint "unused variable in internal/cache/store.go:88"

# Log a format operation
golang format "goimports applied to all .go files"

# Record code generation
golang generate "mockgen interfaces for service layer"

# Log a fix
golang fix "resolved nil pointer in middleware/auth.go"

# View recent lint entries (no args = list mode)
golang lint

# Search all logs for a keyword
golang search "middleware"

# Export everything to JSON
golang export json

# Export to CSV for spreadsheet analysis
golang export csv

# View summary statistics
golang stats

# Health check
golang status

# View recent activity across all commands
golang recent
```

## How It Works

Golang stores all data locally in `~/.local/share/golang/`. Each command logs activity with timestamps in the format `YYYY-MM-DD HH:MM|<input>`, enabling full traceability. The unified `history.log` records every operation with `MM-DD HH:MM <command>: <input>` format for cross-command auditing.

---

Powered by BytesAgain | bytesagain.com | hello@bytesagain.com
