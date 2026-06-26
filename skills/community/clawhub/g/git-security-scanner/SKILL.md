---
name: "Git Security Scanner"
description: "Unified security scanner that catches leaked secrets, credentials, and code vulnerabilities before they reach your remote. Wraps gitleaks (400+ secret patterns) and shipguard (48+ SAST rules) into a single tool with pre-commit hooks, on-demand scans, and full git history audits."
version: "1.0.0"
emoji: "🛡️"
homepage: "https://github.com/celstnblacc"
user-invocable: true
disable-model-invocation: false

requires:
  bins: ["gitleaks", "python3"]
  anyBins: ["shipguard"]
  env: []
---

# Git Security Scanner

Scan your git repositories for leaked secrets, credentials, and security vulnerabilities in one command. Combines **gitleaks** (pattern-based secret detection) and **shipguard** (48+ SAST rules across 7 security layers) into a unified scanner with merged reporting.

## What You Get

### Two Scanning Engines

| Engine | What it does | Rules |
|--------|-------------|-------|
| **gitleaks** | Pattern-based secret detection across files and git history | 400+ built-in rules, custom `.gitleaks.toml` support |
| **shipguard** | Static analysis for secrets, shell injection, code injection, supply chain, config issues | 48+ rules: SEC-001–015, SHELL-001–009, PY-001–012, JS-001–008, GHA-001–005, CFG-001–003, SC-001–006 |

### Scanning Modes

| Mode | Command | What it checks |
|------|---------|---------------|
| **Quick scan** | `git-security-scan` | Current working tree |
| **Staged only** | `git-security-scan --staged-only` | Only staged files — for pre-commit hooks |
| **Full history** | `git-security-scan --full-history` | Entire git history — finds secrets in old commits |
| **Custom severity** | `git-security-scan --severity critical` | Filter by minimum severity level |

### What It Catches

**Secrets (gitleaks + shipguard SEC rules):**
- API keys (AWS, GCP, Azure, OpenAI, Anthropic, Stripe, GitHub, Slack, etc.)
- Database connection strings with embedded passwords
- SSH private keys and PEM files
- JWT tokens and session secrets
- Hardcoded passwords in config files
- `.env` files accidentally staged
- Credentials in comments or docstrings

**Code vulnerabilities (shipguard SAST rules):**
- Shell command injection (`SHELL-001–009`)
- Python code injection: `eval()`, `exec()`, unsafe pickle, SQL injection (`PY-001–012`)
- JavaScript injection: `innerHTML`, `eval()`, prototype pollution (`JS-001–008`)
- GitHub Actions injection: script injection, unpinned actions (`GHA-001–005`)
- Config issues: debug mode in production, permissive CORS, exposed admin routes (`CFG-001–003`)
- Supply chain: unpinned dependencies, missing lockfiles, unsigned artifacts (`SC-001–006`)

### Output Formats

| Format | Flag | Use case |
|--------|------|----------|
| **Terminal** (default) | `--format terminal` | Color-coded findings with severity icons |
| **Markdown** | `--format markdown` | PR comments, documentation, reports |
| **JSON** | `--format json` | CI/CD integration, programmatic analysis |
| **SARIF** | `--format sarif` | GitHub Security tab integration |

## Installation

### Prerequisites

```bash
# macOS
brew install gitleaks
pipx install shipguard  # or: pip install shipguard

# Linux
# gitleaks: download from https://github.com/gitleaks/gitleaks/releases
# shipguard:
pipx install shipguard
```

### Install the Skill

```bash
clawhub install git-security-scanner
```

This adds the `git-security-scan` wrapper script and the skill definition.

### Set Up Pre-Commit Hook

```bash
git-security-scan --install-hooks
```

This installs a pre-commit hook in the current repo that runs `git-security-scan --staged-only --severity high` on every commit. Commits with critical or high severity findings are blocked.

## Usage

### CLI

```bash
# Scan current directory
git-security-scan

# Scan a specific project
git-security-scan /path/to/project

# Pre-commit mode (staged files only, block on high+)
git-security-scan --staged-only --severity high

# Full git history audit
git-security-scan --full-history

# Generate a markdown report
git-security-scan --format markdown --output report.md

# JSON for CI pipelines
git-security-scan --format json --output .security-reports/scan.json

# Skip one engine
git-security-scan --skip-gitleaks   # shipguard only
git-security-scan --skip-shipguard  # gitleaks only
```

### AI Assistant Prompts

**Quick scan:**
> "Scan this repo for leaked secrets and security vulnerabilities"

**Pre-commit setup:**
> "Set up pre-commit hooks to block secrets before they're committed"

**Full history audit:**
> "Audit the entire git history for any credentials that were ever committed"

**Custom rules:**
> "Add a gitleaks rule to catch hardcoded Proxmox API tokens"

**Targeted scan:**
> "Run shipguard on just the Python files with severity high or above"

## Configuration

### gitleaks (`.gitleaks.toml`)

Create in your repo root to add custom secret patterns:

```toml
[extend]
useDefault = true

[[rules]]
id = "proxmox-api-token"
description = "Proxmox API Token"
regex = '''PVEAPIToken=[A-Za-z0-9@!]+:[A-Za-z0-9-]+'''
```

### shipguard (`.shipguard.yml`)

Create in your repo root to configure SAST rules:

```yaml
severity_threshold: medium
exclude_paths:
  - tests/fixtures/
  - node_modules/
  - "*.min.js"
disable_rules:
  - JS-008   # skip specific rule
```

### Pre-commit config (`.shipguard-precommit.yml`)

Stricter settings for the pre-commit hook:

```yaml
severity_threshold: high
exclude_paths:
  - tests/
  - docs/
```

## Report Example

Terminal output:

```
============================================================
  Git Security Scan Report
============================================================
  Directory: /home/user/my-project
  Timestamp: 2026-03-19T10:30:00Z
  Tools:     gitleaks (2 findings)
             shipguard (3 findings)

  Findings: 5  critical: 1  high: 1  medium: 3

  🔴 [CRITICAL] aws-access-key-id (gitleaks)
     config/settings.py:42
     AWS access key ID detected
     > AKIAIOSFODNN7EXAMPLE
     Fix: Rotate this credential immediately. Remove from git history.

  🟠 [HIGH] SEC-003 (shipguard)
     src/api.py:18
     Hardcoded database password in connection string
     > db_url = "postgres://admin:p4ssw0rd@localhost/app"
     Fix: Use environment variables instead of hardcoded credentials.

  🟡 [MEDIUM] PY-003 (shipguard)
     src/utils.py:55
     Use of eval() with user-controlled input
     > result = eval(user_expression)
     Fix: Use ast.literal_eval() or a safe expression parser.
```

## Remediation Workflow

When critical/high findings are detected:

1. **Rotate the credential** — Assume it's compromised if it was ever in git history
2. **Remove from history** — `git filter-repo --invert-paths --path <file>` or BFG Repo Cleaner
3. **Add to `.gitignore`** — Prevent re-staging of secret files
4. **Use environment variables** — Move secrets to `.env` (excluded from git) or a secret manager
5. **Re-scan** — Run `git-security-scan --full-history` to confirm the fix

## Troubleshooting

| Problem | Fix |
|---------|-----|
| VirusTotal "suspicious" warning on install | This is a false positive — the skill *describes* secret patterns and vulnerability types, which triggers pattern detection. Use `clawhub install git-security-scanner --force` to proceed. Review the SKILL.md yourself to confirm. |
| `gitleaks` not found | `brew install gitleaks` (macOS) or download from [gitleaks releases](https://github.com/gitleaks/gitleaks/releases) |
| `shipguard` not found | `pipx install shipguard` or `pip install shipguard` |
| No findings but secrets exist | Check if `.gitleaks.toml` or `.shipguard.yml` is excluding the path. Try `--severity low` to see all findings. |
| Scan is slow | `--full-history` scans every commit. Use default mode (working tree only) for quick checks. |

## Links

- **gitleaks:** https://github.com/gitleaks/gitleaks
- **shipguard:** https://github.com/celstnblacc (part of ai_spec_sec)
- **License:** MIT-0 (this skill) / Apache 2.0 (source tools)

---

*Built by [celstnblacc](https://github.com/celstnblacc) — gitleaks 8.30.0 + shipguard 0.3.2 (48+ SAST rules, 4 output formats).*
