---
name: paycheck
version: "2.0.0"
author: BytesAgain
homepage: https://bytesagain.com
source: https://github.com/bytesagain/ai-skills
license: MIT-0
tags: [paycheck, tool, utility]
description: "Calculate salary breakdowns with taxes and deductions. Use when estimating take-home pay, checking withholdings, comparing deductions, analyzing components."
---

# Paycheck

Paycheck v2.0.0 — a versatile utility toolkit for recording, tracking, and managing paycheck-related data entries across multiple categories. Each command logs timestamped entries to local files, supports searching, exporting in multiple formats, and reviewing activity history. All data is stored locally with no network access required.

## Commands

| Command | Description |
|---------|-------------|
| `paycheck run <input>` | Record a run entry (no args: show recent run entries) |
| `paycheck check <input>` | Record a check entry (no args: show recent check entries) |
| `paycheck convert <input>` | Record a convert entry (no args: show recent convert entries) |
| `paycheck analyze <input>` | Record an analyze entry (no args: show recent analyze entries) |
| `paycheck generate <input>` | Record a generate entry (no args: show recent generate entries) |
| `paycheck preview <input>` | Record a preview entry (no args: show recent preview entries) |
| `paycheck batch <input>` | Record a batch entry (no args: show recent batch entries) |
| `paycheck compare <input>` | Record a compare entry (no args: show recent compare entries) |
| `paycheck export <input>` | Record an export entry (no args: show recent export entries) |
| `paycheck config <input>` | Record a config entry (no args: show recent config entries) |
| `paycheck status <input>` | Record a status entry (no args: show recent status entries) |
| `paycheck report <input>` | Record a report entry (no args: show recent report entries) |
| `paycheck stats` | Show summary statistics across all log files |
| `paycheck search <term>` | Search all entries for a keyword (case-insensitive) |
| `paycheck recent` | Show the 20 most recent history entries |
| `paycheck help` | Show usage information |
| `paycheck version` | Show version (v2.0.0) |

Note: The script also has utility-level `_export <fmt>` (json/csv/txt) and `_status` (health check) functions accessible via the helper paths in the case statement.

## Data Storage

All data is stored locally in `~/.local/share/paycheck/`:

- **`{command}.log`** — One file per command (e.g., `run.log`, `check.log`, `analyze.log`, `convert.log`). Each line is `timestamp|value`.
- **`history.log`** — Unified activity log with timestamps for every recorded action.
- **`export.{json|csv|txt}`** — Generated export files when using the utility-level export:
  - **JSON** — Array of `{type, time, value}` objects
  - **CSV** — Header row `type,time,value` followed by data rows
  - **TXT** — Sections grouped by command name with all entries

The `stats` command reads all `.log` files and reports per-file entry counts, total count, and disk usage. The `search` command performs case-insensitive grep across all log files and displays matches grouped by category.

## Requirements

- **bash 4+** (uses `local`, `set -euo pipefail`)
- Standard POSIX utilities: `date`, `wc`, `du`, `tail`, `head`, `grep`, `sed`, `basename`, `cut`, `cat`
- No external dependencies, no API keys, no network access

## When to Use

1. **Logging paycheck calculations** — Record each salary computation with `paycheck run <description>` to maintain a timestamped audit trail of pay calculations.
2. **Tracking pay comparisons** — Use `paycheck compare <details>` to log side-by-side comparisons of different pay structures, tax brackets, or benefit options.
3. **Analyzing deductions** — Record analysis entries with `paycheck analyze <breakdown>` to document detailed deduction reviews for each pay period.
4. **Generating payroll reports** — Use `paycheck report <summary>` to log periodic payroll summaries, then `paycheck search` to find specific entries later.
5. **Exporting pay records** — Use `paycheck stats` for a quick summary of all recorded entries, or the utility-level export to generate JSON/CSV/TXT files for external use.

## Examples

```bash
# Record a paycheck run entry
paycheck run "Monthly salary: gross 15000, tax 2250, insurance 1500, net 11250"
#   [Paycheck] run: Monthly salary: gross 15000, tax 2250, insurance 1500, net 11250
#   Saved. Total run entries: 1

# View recent run entries (no arguments)
paycheck run
# Recent run entries:
#   2025-03-18 10:00|Monthly salary: gross 15000, tax 2250, insurance 1500, net 11250

# Record an analyze entry for deduction breakdown
paycheck analyze "Q1 average deductions: federal 15%, state 5%, 401k 6%, health 3%"
#   [Paycheck] analyze: Q1 average deductions...
#   Saved. Total analyze entries: 1

# Compare two pay structures
paycheck compare "Offer A: 120k base + 10k bonus vs Offer B: 110k base + 20k bonus"

# Search all entries for a keyword
paycheck search "bonus"
# Searching for: bonus
#   --- compare ---
#     2025-03-18 10:15|Offer A: 120k base + 10k bonus vs Offer B: 110k base + 20k bonus

# View summary statistics
paycheck stats
# === Paycheck Stats ===
#   run: 1 entries
#   analyze: 1 entries
#   compare: 1 entries
#   ---
#   Total: 3 entries
#   Data size: 4.0K

# Show recent activity from the unified history log
paycheck recent
# === Recent Activity ===
#   03-18 10:00 run: Monthly salary: gross 15000...
#   03-18 10:05 analyze: Q1 average deductions...
#   03-18 10:15 compare: Offer A vs Offer B...
```

## Output

All results are printed to stdout. Every action that records data also appends to `history.log` for unified tracking. Redirect output with `paycheck <command> > output.txt` if needed.

## Configuration

The data directory defaults to `~/.local/share/paycheck/`. It is created automatically on first run.

---

*Powered by BytesAgain | bytesagain.com | hello@bytesagain.com*
