---
name: pre-publish-security
description: Multi-layered security audit system for GitHub/ClawHub releases. Prevents credential leaks, detects vulnerabilities, validates documentation. Frequency-aware scanning (quick/history/dependencies). Blocks bad pushes automatically.
version: 2.0.0
author: solmas
homepage: https://github.com/solmas/openclaw-pre-publish-security
license: MIT
tags:
  - security
  - git
  - audit
  - credentials
  - publishing
  - dependencies
  - cve
metadata:
  openclaw:
    requires: 
      bins: [git, jq, grep]
      optional: [npm, pip, safety, shellcheck]
    install:
      - { id: jq, kind: apt, package: jq }
user-invocable: true
---

# Pre-Publish Security Protocol

**Prevents security breaches like exposed credentials in open-source releases.**

## Features

✅ **Multi-Level Scanning**
- Quick scan: Every push (~5s)
- History scan: Monthly deep dive (~2-5min)
- Dependency CVE: Weekly npm/Python check (~30s)
- Full audit: On-demand comprehensive (~3-6min)

✅ **Smart Frequency Management**
- State tracking knows when each scan last ran
- Auto-determines which scans to run
- Prevents redundant checks

✅ **What It Catches**
- GitHub PATs, API keys, passwords, private keys
- Secrets in git history (even if "deleted")
- npm/Python dependency CVEs
- Unsafe code patterns (eval, exec)
- Documentation placeholders (`[ORG]`, `example.com`)
- Missing LICENSE/README files
- Exported environment variables with secrets

✅ **Automated Protection**
- Git pre-push hook blocks bad commits
- Severity-based exit codes (CRITICAL/HIGH/MEDIUM/LOW)
- Markdown reports with actionable fixes

## Quick Start

### Install Pre-Push Hook
```bash
# Automatic protection on every push
./install-hooks.sh /path/to/your/repo
```

### Run First History Scan
```bash
# One-time deep dive (or monthly)
./audit-full.sh /path/to/repo history
```

### Check Status
```bash
# See when scans last ran
./schedule.sh status
```

### Run Scheduled Audits
```bash
# Auto-determines what to run based on time
./schedule.sh run /path/to/repo
```

## Manual Scans

```bash
# Quick scan (every push)
./audit-simple.sh /path/to/repo

# Git history scan (monthly)
./audit-full.sh /path/to/repo history

# Dependency scan (weekly)
./audit-full.sh /path/to/repo dependencies

# Full audit (before releases)
./audit-full.sh /path/to/repo full
```

## What Gets Scanned

### Quick Scan (Every Push)
- Current file secret patterns
- Documentation placeholders
- Basic license/README presence
- **Runtime:** ~5 seconds

### History Scan (Monthly)
- Full git commit history
- Deleted-but-accessible credentials
- Historical security issues
- **Runtime:** 2-5 minutes

### Dependency Scan (Weekly)
- npm audit (Node.js CVEs)
- Python safety check
- Known vulnerabilities
- **Runtime:** ~30 seconds

### Full Audit (On-Demand)
- All of the above
- Environment variable leaks
- Pre-commit hook verification
- Code quality patterns
- **Runtime:** 3-6 minutes

## Severity Levels

- **CRITICAL** → Blocks push (secrets, credentials)
- **HIGH** → Requires approval (vulnerabilities, missing LICENSE)
- **MEDIUM** → Warning (TODOs, missing README)
- **LOW** → Informational

## Integration

### Pre-Push Hook (Recommended)
```bash
./install-hooks.sh ~/my-repo
git push  # Automatic security check
```

### Weekly Cron
```bash
# Add to OpenClaw cron
openclaw cron add \
  --name "weekly-repo-scan" \
  --cron "0 3 * * 1" \
  --announce \
  --message "Run: ~/.openclaw/workspace/skills/pre-publish-security/schedule.sh run ~/repo"
```

### Manual Pre-Publish
```bash
# Before clawhub publish
./audit-full.sh ~/skills/my-skill full
clawhub publish skills/my-skill --version 1.0.1
```

## Files

- `audit-simple.sh` - Fast pre-push scan
- `audit-full.sh` - Complete scanner with tracking
- `schedule.sh` - Status & smart automation
- `install-hooks.sh` - Git hook installer
- `audit-state.json` - State tracking (auto-created)
- `AUDIT-SCHEDULE.md` - Detailed frequency guide
- `README.md` - Full documentation
- `agents/` - Sub-agent definitions (future use)

## Requirements

**Required:**
- git
- jq
- grep

**Optional (enhanced detection):**
- npm (Node.js dependency scanning)
- pip + safety (Python dependency scanning)
- shellcheck (bash script validation)

## State Tracking

Automatically tracks:
- Last run timestamp for each scan type
- Total scan counts
- Cumulative findings by severity

View with: `./schedule.sh status`

## Exit Codes

- `0` - Passed (no issues or low/medium only)
- `1` - Critical issues (blocks push)
- `2` - High issues (requires review)

## Real-World Example

**Problem:** Accidentally pushed GitHub PAT in git remote URL  
**Solution:** This tool caught it and blocked the push  
**Result:** Credential never exposed publicly

## Use Cases

1. **Individual Developers:** Pre-push hook prevents accidents
2. **Open-Source Projects:** Protects against contributor mistakes
3. **ClawHub Skills:** Validates before publishing
4. **CI/CD:** Add to GitHub Actions for automated checks
5. **Security Audits:** Comprehensive repository review

## Why This Exists

On 2026-03-15, a GitHub PAT was accidentally exposed in a git config file. This protocol ensures it never happens again - to anyone.

## License

MIT - Use it, improve it, share it.

## Contributing

Issues & PRs welcome at: https://github.com/solmas/pre-publish-security
