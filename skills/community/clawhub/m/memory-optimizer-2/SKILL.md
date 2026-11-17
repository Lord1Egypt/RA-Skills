# 🧠 Agent Memory Optimizer

**Version:** 1.0.0 | **Price:** $3.99 | **Author:** Peru 🇵🇪

## Description

Analyzes an AI agent's memory files (MEMORY.md, memory/*.md), detects duplicates, stale information, missing indexes, and structural issues. Generates an optimization report with specific recommendations and can auto-fix common issues.

## Features

- **Duplicate Detection** — Fuzzy matching to find repeated information across files
- **Staleness Analysis** — Identifies outdated dates, metrics, and references
- **Structure Audit** — Checks heading hierarchy, link integrity, section organization
- **Memory Efficiency Score** — 0-100 rating of memory health
- **Auto-Fix** — Can automatically deduplicate, re-index, and reorganize
- **Detailed Reports** — Markdown report with specific, actionable recommendations

## Requirements

- `python3` (3.8+)
- Python packages: `difflib` (stdlib), `re` (stdlib), `pathlib` (stdlib)
- No external dependencies! Uses only Python standard library.

## Installation

Copy this skill folder to your workspace. No pip install needed.

```bash
chmod +x analyze.py optimize.py
```

## Usage

### Analyze Memory

```bash
# Analyze current workspace (auto-detects MEMORY.md and memory/ folder)
python3 analyze.py

# Analyze a specific directory
python3 analyze.py --path /path/to/workspace

# Output report to file
python3 analyze.py --output report.md

# JSON output
python3 analyze.py --json
```

### Apply Optimizations

```bash
# Preview changes (dry run — default)
python3 optimize.py

# Apply all recommended fixes
python3 optimize.py --apply

# Apply only deduplication
python3 optimize.py --apply --only dedup

# Apply only re-indexing
python3 optimize.py --apply --only reindex

# Backup before applying
python3 optimize.py --apply --backup
```

### All Options

```
analyze.py [OPTIONS]
  --path DIR      Workspace directory to analyze (default: current dir)
  --output FILE   Save report to file
  --json          Output as JSON
  --verbose       Show detailed analysis
  --help          Show help

optimize.py [OPTIONS]
  --path DIR       Workspace directory (default: current dir)
  --apply          Apply fixes (default: dry run)
  --only TYPE      Only apply: dedup, reindex, stale, structure
  --backup         Create .bak files before modifying
  --help           Show help
```

## Output Format

### Analysis Report

```markdown
# 🧠 Memory Optimization Report
Workspace: /root/.openclaw/workspace
Analyzed: 2026-02-14 03:00 UTC

## Memory Efficiency Score: 72/100

### Summary
- Files scanned: 15
- Total entries: 234
- Duplicates found: 12
- Stale entries: 8
- Missing indexes: 3
- Structure issues: 5

## 🔴 Critical Issues
1. **12 duplicate entries** across MEMORY.md and memory/2026-02-10.md
   - "GitHub token configured" appears 3 times
   - "TTS setup complete" appears 2 times

## 🟡 Warnings
1. **8 stale entries** with dates older than 30 days
   - memory/2025-12-15.md: "Current project: X" (60 days old)

## 🟢 Suggestions
1. Consider merging memory/2026-02-01.md through memory/2026-02-05.md (low activity)
2. Add table of contents to MEMORY.md (>50 entries)

## Recommended Actions
- [ ] Remove 12 duplicate entries (saves ~2.4KB)
- [ ] Archive 8 stale entries
- [ ] Add index headers to 3 files
- [ ] Fix 5 structural issues
```

## How It Works

1. **File Discovery** — Scans for MEMORY.md, memory/*.md, and related files
2. **Content Parsing** — Extracts entries, headers, dates, metrics from markdown
3. **Duplicate Detection** — Uses SequenceMatcher for fuzzy matching (>80% similarity)
4. **Staleness Check** — Parses dates and flags entries older than configurable threshold
5. **Structure Analysis** — Validates heading hierarchy, checks for orphan sections
6. **Scoring** — Calculates efficiency score based on weighted issue counts
7. **Report Generation** — Compiles findings into actionable markdown report

## Example

```bash
$ python3 analyze.py --path /root/.openclaw/workspace
🧠 Agent Memory Optimizer v1.0.0
Scanning workspace: /root/.openclaw/workspace
Found 12 memory files (45.2 KB total)
Analyzing...

Memory Efficiency Score: 72/100 ⚠️

Issues found:
  🔴 Critical: 2
  🟡 Warning: 5
  🟢 Suggestion: 3

Report saved to: memory_report.md
Run `python3 optimize.py --apply` to fix issues.
```
