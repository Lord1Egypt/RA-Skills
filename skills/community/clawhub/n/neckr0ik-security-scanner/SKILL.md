---
name: neckr0ik-security-scanner
version: 1.0.0
description: Security audit tool for OpenClaw skills. Scans skill directories for common vulnerabilities including hardcoded secrets, unsafe shell commands, prompt injection risks, unauthorized network access, and code execution dangers. Use when auditing skills before installation, reviewing skill code for security issues, or validating skills for ClawHub publication.
---

# Skill Security Audit

Scan OpenClaw skills for security vulnerabilities before installation or publication.

## Quick Start

```bash
# Audit a single skill
skill-security-audit audit /path/to/skill-folder

# Audit all installed skills
skill-security-audit audit-all

# Generate security report
skill-security-audit report /path/to/skill-folder --format json
```

## What This Detects

### Critical Issues (Block Installation)

| Issue | Description | Risk Level |
|-------|-------------|------------|
| **Hardcoded Secrets** | API keys, tokens, passwords in code | Critical |
| **Shell Injection** | Unsanitized input to shell commands | Critical |
| **Code Execution** | eval(), exec(), dynamic code execution | Critical |
| **Unauthorized Network** | Calls to unknown/suspicious domains | Critical |

### High Issues (Review Required)

| Issue | Description | Risk Level |
|-------|-------------|------------|
| **Prompt Injection** | User input in system prompts without sanitization | High |
| **File Path Traversal** | Unchecked file paths from user input | High |
| **Excessive Permissions** | Requests unnecessary system access | High |

### Medium Issues (Warnings)

| Issue | Description | Risk Level |
|-------|-------------|------------|
| **Outdated Dependencies** | Packages with known CVEs | Medium |
| **Unpinned Versions** | Floating dependency versions | Medium |
| **Missing License** | No license file for distribution | Medium |

## Security Patterns

### Good Pattern: Environment Variables

```python
# CORRECT: Load secrets from environment
import os
api_key = os.environ.get("OPENAI_API_KEY")
```

### Bad Pattern: Hardcoded Secrets

```python
# DANGEROUS: Secret in code
api_key = "sk-abc123def456..."  # NEVER DO THIS
```

### Good Pattern: Sanitized Input

```python
# CORRECT: Validate and sanitize
import re
def safe_filename(name):
    return re.sub(r'[^a-zA-Z0-9_-]', '', name)
```

### Bad Pattern: Shell Injection

```python
# DANGEROUS: User input to shell
os.system(f"convert {user_file} output.png")  # NEVER DO THIS
```

## Running Audits

### Important: Self-Scan Results

When running `skill-security-audit audit skill-security-audit/`, you will see findings for the pattern definitions themselves. This is expected — the scanner detects the example patterns in its own documentation. These are not real vulnerabilities.

For actual skill audits, this produces accurate results.

### Single Skill Audit

```bash
skill-security-audit audit ./my-skill/
```

Output:
- Pass/Fail status
- List of vulnerabilities found
- Severity ratings
- Remediation suggestions

### Batch Audit (All Installed Skills)

```bash
skill-security-audit audit-all
```

Scans `~/.openclaw/skills/` and reports on all installed skills.

### Report Formats

```bash
# JSON for CI/CD integration
skill-security-audit audit ./skill/ --format json

# Markdown for documentation
skill-security-audit audit ./skill/ --format markdown

# Summary for quick review
skill-security-audit audit ./skill/ --format summary
```

## CI/CD Integration

Add to your skill publishing pipeline:

```yaml
# .github/workflows/publish.yml
- name: Security Audit
  run: skill-security-audit audit ./skill/
```

Exit codes:
- 0: No issues found
- 1: Medium+ issues found (warnings)
- 2: Critical issues found (block)

## Publishing Secure Skills

Before publishing to ClawHub:

1. Run `skill-security-audit audit ./your-skill/`
2. Fix all critical and high issues
3. Document any required secrets in README
4. Include `.env.example` with placeholder values
5. Re-run audit to confirm clean

## See Also

- `references/vulnerabilities.md` — Complete vulnerability database
- `references/remediation.md` — How to fix common issues
- `scripts/audit.py` — Main audit script