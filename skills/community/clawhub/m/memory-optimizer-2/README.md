# 🧠 Agent Memory Optimizer

> Analyze and optimize AI agent memory files. Detects duplicates, stale info, and structural issues.

**Version:** 1.0.0 | **Author:** Peru 🇵🇪 | **Price:** $3.99

---

## ✨ Features

- 🔍 **Duplicate Detection** — Fuzzy matching to find repeated information across files
- ⏰ **Staleness Analysis** — Identifies outdated dates, metrics, and references
- 🏗️ **Structure Audit** — Checks heading hierarchy, link integrity, section organization
- 📊 **Memory Efficiency Score** — 0-100 rating of memory health
- 🔧 **Auto-Fix** — Automatically deduplicate, re-index, and reorganize
- 📋 **Detailed Reports** — Markdown report with specific, actionable recommendations

## 🚀 Installation

```bash
chmod +x analyze.py optimize.py
```

**No external dependencies!** Uses only Python standard library (3.8+).

## 📖 Usage

### Analyze Memory

```bash
# Analyze current workspace (auto-detects MEMORY.md and memory/ folder)
python3 analyze.py

# Analyze a specific directory
python3 analyze.py --path /path/to/workspace

# Save report to file
python3 analyze.py --output report.md

# JSON output for automation
python3 analyze.py --json

# Verbose mode for detailed analysis
python3 analyze.py --verbose
```

### Apply Optimizations

```bash
# Preview changes (dry run — default, safe to run)
python3 optimize.py

# Apply all recommended fixes
python3 optimize.py --apply

# Apply only specific fixes
python3 optimize.py --apply --only dedup      # deduplication only
python3 optimize.py --apply --only reindex    # re-indexing only
python3 optimize.py --apply --only stale      # stale entry removal
python3 optimize.py --apply --only structure  # structure fixes

# Create backups before applying changes
python3 optimize.py --apply --backup
```

## ⚙️ All Options

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

## 📊 Output Example

```
$ python3 analyze.py

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

### Report Format

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

## 🔴 Critical Issues
1. **12 duplicate entries** across MEMORY.md and daily files

## 🟡 Warnings
1. **8 stale entries** with dates older than 30 days

## 🟢 Suggestions
1. Consider merging low-activity daily files
2. Add table of contents to MEMORY.md

## Recommended Actions
- [ ] Remove 12 duplicate entries (saves ~2.4KB)
- [ ] Archive 8 stale entries
```

## 🔧 How It Works

1. **File Discovery** — Scans for MEMORY.md, memory/*.md, and related files
2. **Content Parsing** — Extracts entries, headers, dates, metrics from markdown
3. **Duplicate Detection** — Uses SequenceMatcher for fuzzy matching (>80% similarity)
4. **Staleness Check** — Parses dates and flags entries older than 30 days (configurable)
5. **Structure Analysis** — Validates heading hierarchy, checks for orphan sections
6. **Scoring** — Calculates efficiency score based on weighted issue counts
7. **Report Generation** — Compiles findings into actionable markdown report

## 💡 Tips

- Run `analyze.py` regularly (weekly) to keep memory files healthy
- Use `--backup` flag the first time you run `optimize.py --apply`
- The dry run (default) shows what would change without modifying anything
- Works with any OpenClaw agent workspace structure

## 📄 License

Free for personal and commercial use. Made with ❤️ in Peru.
