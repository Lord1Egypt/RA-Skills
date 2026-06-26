# Git Repository Auditor

Audit Git repositories for security issues, large files, sensitive data, and repository health metrics.

## Features

- Scan Git history for secrets (API keys, passwords, tokens)
- Detect large files impacting repository performance
- Check repository health (stale branches, binary files, .gitignore)
- Multiple output formats (human-readable, JSON)
- No external dependencies (Git + Python 3 only)

## Quick Start

```bash
# Scan a repository for security issues
python3 scripts/main.py scan /path/to/repo

# Get repository health report
python3 scripts/main.py health /path/to/repo

# List all branches with commit info
python3 scripts/main.py branches /path/to/repo

# Output JSON for automation
python3 scripts/main.py scan /path/to/repo --json
```

## Installation

This skill requires:
- Git 2.20+ installed and in PATH
- Python 3.x

No additional Python packages required.

## Usage Examples

### Basic security scan
```bash
python3 scripts/main.py scan ~/projects/my-app
```

### Scan with custom large file threshold
```bash
python3 scripts/main.py scan . --threshold 50
```

### Generate JSON report for CI/CD
```bash
python3 scripts/main.py scan . --json > security-report.json
```

### Check repository health
```bash
python3 scripts/main.py health .
```

## Output

The tool provides color-coded output:
- 🔍 Scanning progress
- ⚠️  Security issues found
- 💾 Large files detected
- ✅ No issues found
- 📊 Health metrics

## Limitations

- Scanning large repositories may be slow
- Secrets detection uses regex patterns (may have false positives)
- Does not automatically remove secrets from history
- Requires local Git repository (cannot scan remote directly)

## License

This skill is part of the OpenClaw Skill Factory portfolio.