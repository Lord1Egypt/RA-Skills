# Proof of Work — Task Completion Verification for AI Agents

A lightweight, zero-dependency shell script that verifies AI agent task outputs meet essential structural and content requirements. Perfect for automated monitoring of agent deliverables in production workflows.

## What It Does

Proof of Work validates that task completion files:

- **Exist and contain content** — File presence and non-empty checks
- **Meet timing requirements** — Files modified within specified time windows (24h, 7d, etc.)
- **Contain required sections** — Validates presence of headers, markers, or structural elements
- **Meet content standards** — Checks minimum length and filters placeholder/incomplete text
- **Maintain quality gates** — Optional AI-powered assessment via Ollama integration (Heartbeat Kit)

Perfect for CI/CD pipelines, cron-based monitoring, or real-time validation of agent outputs.

## Features

- **Pure bash** — No Python, npm, pip, or external dependencies
- **Cross-platform** — Works on macOS, Linux, and any POSIX environment
- **Configurable** — JSON-based configuration for different workflows
- **Multiple check modes** — Single file, directory recursion, continuous monitoring
- **Structured reporting** — Text output with pass/fail summary and detailed reasons
- **Cron-ready** — Designed for automated scheduled checks
- **Extensible** — Optional Ollama/Heartbeat Kit integration for AI quality checks

## Quick Start

### Installation

```bash
curl -L https://example.com/proof-of-work/install.sh | bash
```

Or manual install:

```bash
git clone https://github.com/your-org/proof-of-work.git
cd proof-of-work
./install.sh
```

### First Use

```bash
# Initialize with sample config and directory structure
proof-of-work init

# Check a single file
proof-of-work check ~/agent-workspace/outputs/task-001.md

# Check all files in a directory
proof-of-work check-dir ~/agent-workspace/outputs/

# Generate a summary report
proof-of-work report

# Continuous monitoring (for cron)
proof-of-work watch
```

## Usage Examples

### Check a Single File

```bash
$ proof-of-work check ~/outputs/agent-summary.md
```

Output:
```
✓ File exists and is non-empty
✓ Last modified: 2h ago (within 24h limit)
✓ Contains required section: ## Summary
✓ Contains required section: ## Result
✓ Content length: 450 bytes (minimum: 100)
✗ File contains placeholder text: TODO found in line 23

File: ~/outputs/agent-summary.md
Status: FAIL
Reasons: Placeholder text detected
```

### Check a Directory

```bash
$ proof-of-work check-dir ~/agent-workspace/outputs/
```

Output:
```
Checking 5 files in ~/agent-workspace/outputs/

task-001.md        ✓ PASS
task-002.md        ✓ PASS
task-003.md        ✗ FAIL (outdated: 72h old)
incomplete.txt     ✗ FAIL (missing required sections)
notes.md           ⚠ WARN (placeholder text)

Summary: 2 passed, 2 failed, 1 warning
Details logged to ~/.proof-of-work/checks.log
```

### Generate Report

```bash
$ proof-of-work report
```

Produces a detailed report of all recent checks with trends and failure analysis.

### Watch Mode (Cron)

```bash
$ proof-of-work watch
Watching: /home/user/agent-workspace/outputs/
Checking every 60 seconds...
[2026-03-28 14:23:01] task-004.md: PASS
[2026-03-28 14:24:15] task-005.md: FAIL - missing sections
```

## Configuration

### Default Config Location

`~/.proof-of-work/config.json`

### Config Options

```json
{
  "check_paths": [
    "~/agent-workspace/outputs/",
    "~/agent-workspace/handoffs/"
  ],
  "required_sections": [
    "## Summary",
    "## Result"
  ],
  "min_content_length": 100,
  "max_age_hours": 48,
  "placeholder_patterns": [
    "TODO",
    "TBD",
    "PLACEHOLDER",
    "FIXME"
  ],
  "output_format": "text",
  "log_file": "~/.proof-of-work/checks.log",
  "enable_json_validation": false,
  "enable_markdown_validation": true
}
```

### Configuration Details

| Option | Type | Description |
|--------|------|-------------|
| `check_paths` | Array | Directories to monitor |
| `required_sections` | Array | Text markers/headers that must be present |
| `min_content_length` | Number | Minimum file size in bytes |
| `max_age_hours` | Number | Maximum age of files (0 = no limit) |
| `placeholder_patterns` | Array | Patterns indicating incomplete work |
| `output_format` | String | "text" or "json" |
| `log_file` | String | Path for check logs |
| `enable_json_validation` | Boolean | Validate JSON file structure |
| `enable_markdown_validation` | Boolean | Validate markdown syntax |

## Advanced: AI-Powered Checks

When Ollama is available and configured, enable AI quality assessment:

```bash
proof-of-work check ~/outputs/summary.md --ai-check
```

This activates:

- **Quality Assessment** — Is content meaningful or filler text?
- **Coherence Check** — Does output match the original task?
- **Completeness Scoring** — What percentage complete is the deliverable?

Requires Ollama running with Heartbeat Kit integration. Falls back to structural checks if unavailable.

## Cron Setup

### Monitor Every Hour

```bash
0 * * * * ~/.proof-of-work/proof-of-work.sh watch >> ~/.proof-of-work/cron.log 2>&1
```

### Monitor Every 30 Minutes

```bash
*/30 * * * * ~/.proof-of-work/proof-of-work.sh watch >> ~/.proof-of-work/cron.log 2>&1
```

### Daily Report Generation

```bash
0 8 * * * ~/.proof-of-work/proof-of-work.sh report > ~/.proof-of-work/daily-report.txt 2>&1
```

### Email Alert on Failures

```bash
*/15 * * * * ~/.proof-of-work/proof-of-work.sh watch | grep FAIL | mail -s "PoW Check Failures" alerts@example.com
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | All checks passed |
| 1 | One or more checks failed |
| 2 | Configuration error |
| 3 | File or directory not found |

## Troubleshooting

### Config not found

```
Error: Config file not found at ~/.proof-of-work/config.json
Run: proof-of-work init
```

### Permission denied

```bash
chmod +x ~/.proof-of-work/proof-of-work.sh
```

### Ollama not responding

AI checks will be skipped automatically. Enable verbose output with `-v`:

```bash
proof-of-work check file.md --ai-check -v
```

## Performance

- Checking 100 files: ~1-2 seconds
- Full report generation: ~5-10 seconds
- Continuous watch mode: Minimal CPU (checks every 60s by default)

## Files & Directories

```
~/.proof-of-work/
├── proof-of-work.sh       # Main executable
├── config.json            # Configuration
├── checks.log             # Check history
└── reports/               # Generated reports
```

## License

Free and open-source. Use in any workflow.

## Support

For issues, questions, or feature requests, refer to the main project repository.
