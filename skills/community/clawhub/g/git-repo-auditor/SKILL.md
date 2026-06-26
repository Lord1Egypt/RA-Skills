---
name: git-repo-auditor
description: Audit Git repositories for security issues, large files, sensitive data, and repository health metrics.
version: 1.0.0
author: skill-factory
metadata:
  openclaw:
    requires:
      bins:
        - git
        - python3
---

# Git Repository Auditor

## What This Does

A CLI tool to audit Git repositories for security issues, code quality problems, and repository health. Scan repositories for secrets, large files, sensitive data, and common security anti-patterns.

Key features:
- **Secrets detection**: Scan Git history for API keys, passwords, tokens, and other sensitive data using regex patterns
- **Large file detection**: Identify large files (>10MB) in repository history that may impact performance
- **Security anti-patterns**: Detect hardcoded credentials, insecure configuration files, and dangerous permissions
- **Repository health**: Check for merge conflicts, stale branches, and other repository hygiene issues
- **Compliance reporting**: Generate security compliance reports for audits and team reviews
- **Multiple output formats**: Human-readable, JSON, and CSV output for integration with other tools
- **Custom scanning**: Configure custom regex patterns and file extensions to scan
- **Historical analysis**: Scan entire Git history or specific time ranges
- **Remediation guidance**: Suggest fixes for identified security issues

## When To Use

- You need to audit a Git repository for security compliance
- You want to detect accidental commits of secrets or sensitive data
- You're preparing a repository for open-source release
- You need to identify performance issues (large files in history)
- You're onboarding new developers and want to ensure repository hygiene
- You need to generate security audit reports for compliance requirements
- You want to automate security scanning in CI/CD pipelines
- You're cleaning up old repositories and need to identify issues

## Usage

Basic commands:

```bash
# Scan current directory repository
python3 scripts/main.py scan .

# Scan specific repository path
python3 scripts/main.py scan /path/to/repo

# Scan with custom secrets patterns file
python3 scripts/main.py scan . --patterns custom-patterns.json

# Generate JSON report for automation
python3 scripts/main.py scan . --json

# Check only for large files (>50MB)
python3 scripts/main.py scan . --check large-files --threshold 50

# Scan specific branch or commit range
python3 scripts/main.py scan . --branch main --since "2024-01-01"

# Generate remediation report with suggested fixes
python3 scripts/main.py scan . --remediation

# List all branches with last commit age
python3 scripts/main.py branches .
```

## Examples

### Example 1: Basic security scan

```bash
python3 scripts/main.py scan ~/projects/my-app
```

Output:
```
🔍 Scanning repository: /home/user/projects/my-app
📊 Repository info: 247 commits, 5 branches, 3 contributors

🔐 SECURITY ISSUES FOUND (3):
⚠️  High: AWS_ACCESS_KEY_ID found in commit abc123 (2024-02-15)
    File: config/old-config.env
    Pattern: AWS_ACCESS_KEY_ID=AKIA.*
    Remediation: Rotate key immediately, remove from history with BFG

⚠️  Medium: Hardcoded database password in commit def456 (2024-01-20)
    File: src/database.js
    Pattern: password: "secret123"
    Remediation: Move to environment variables, use secret manager

⚠️  Low: Private key file extension in commit ghi789 (2023-12-05)
    File: backup/id_rsa.old
    Pattern: Private key file (.pem, .key, .ppk, id_rsa)
    Remediation: Remove file from repository history

💾 LARGE FILES FOUND (2):
📦 42MB: assets/video/demo.mp4 (commit xyz123)
📦 18MB: database/backup.sql (commit uvw456)

✅ Repository health: Good
⏰ Stale branches: 2 branches older than 90 days
```

### Example 2: JSON output for CI/CD integration

```bash
python3 scripts/main.py scan . --json > security-report.json
```

Output (excerpt):
```json
{
  "repository": "/home/user/projects/my-app",
  "scan_date": "2024-03-06T10:30:00Z",
  "security_issues": [
    {
      "severity": "high",
      "type": "aws_access_key",
      "commit": "abc123",
      "date": "2024-02-15",
      "file": "config/old-config.env",
      "pattern": "AWS_ACCESS_KEY_ID=AKIA.*",
      "remediation": "Rotate key immediately, remove from history with BFG"
    }
  ],
  "large_files": [
    {
      "size_mb": 42,
      "path": "assets/video/demo.mp4",
      "commit": "xyz123"
    }
  ],
  "summary": {
    "total_issues": 3,
    "by_severity": {"high": 1, "medium": 1, "low": 1},
    "large_files_count": 2,
    "total_size_mb": 60
  }
}
```

### Example 3: Check repository health

```bash
python3 scripts/main.py health .
```

Output:
```
📈 Repository Health Report: /home/user/projects/my-app

📊 Basic Metrics:
- Commits: 1,247
- Branches: 12 (3 active, 9 stale)
- Contributors: 8
- First commit: 2022-05-15
- Last commit: 2024-03-06

⚠️  Health Issues:
- Stale branches: 9 branches with no commits in >90 days
- Large files: 2 files >10MB in history
- Binary files: 45 binary files (consider Git LFS)
- Merge conflicts: 3 unresolved merge markers in code

✅ Good Practices:
- .gitignore present and comprehensive
- No secrets detected in recent commits
- Regular commit activity (avg 15 commits/week)
- Meaningful commit messages (87% good)

💡 Recommendations:
1. Clean up stale branches: git branch -d branch1 branch2...
2. Consider Git LFS for binary files
3. Resolve merge conflicts in: src/app.js, config/settings.yaml
```

### Example 4: Large files detection only

```bash
python3 scripts/main.py scan . --check large-files --threshold 20
```

Output:
```
💾 Large Files (>20MB) in Repository History:

1. assets/videos/presentation.mp4
   - Size: 42MB
   - Commit: xyz123 (2024-01-15)
   - Author: Jane Doe
   - Message: "Add presentation video"

2. database/backup/archive.sql.gz
   - Size: 38MB
   - Commit: uvw456 (2023-12-20)
   - Author: John Smith
   - Message: "Database backup"

Total: 2 files, 80MB
Recommendation: Consider using Git LFS for files >20MB
```

## Requirements

- Git 2.20+ installed and available in PATH
- Python 3.x
- No external Python dependencies required (uses standard library)

## Limitations

- Scanning large repositories with extensive history may be slow
- Secrets detection uses regex patterns; may have false positives/negatives
- Does not automatically remove secrets from history (requires manual remediation)
- Limited to Git repositories (does not work with other VCS)
- No support for scanning encrypted repositories
- Large file detection scans entire history; may miss files in ignored directories
- Does not integrate with external secret managers (Vault, AWS Secrets Manager, etc.)
- No real-time monitoring; scans only historical commits
- Limited to text file scanning; cannot detect secrets in binary files
- May not detect all secret patterns; custom patterns may be needed
- Performance depends on repository size and history depth
- No support for scanning Git submodules automatically
- No built-in integration with secret management systems (Vault, AWS Secrets Manager)
- Limited to text file scanning; cannot detect secrets in binary files
- No support for custom Git hooks or pre-commit integration
- Performance may be impacted on repositories with millions of commits
- No support for distributed scanning across multiple repositories
- Limited error handling for corrupted Git repositories
- No support for scanning Git worktrees or shallow clones
- Cannot scan remote repositories without local clone
- No built-in notification system for new issues

## Directory Structure

The tool works with any local Git repository. No special configuration directories are required, but you can provide custom patterns files for secrets detection.

## Error Handling

- Invalid repository paths show helpful error messages with suggestions
- Git command failures show the underlying error and suggest troubleshooting steps
- Permission errors suggest checking repository access rights
- Pattern file parsing errors show line numbers and validation issues
- Memory errors suggest using smaller commit ranges or more specific scanning

## Contributing

This is a skill built by the Skill Factory. Issues and improvements should be reported through the OpenClaw project.