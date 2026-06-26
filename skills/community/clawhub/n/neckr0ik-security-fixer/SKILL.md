---
name: neckr0ik-security-fixer
version: 1.0.0
description: Auto-fix security vulnerabilities in OpenClaw skills. Works with neckr0ik-security-scanner to automatically remediate hardcoded secrets, shell injection risks, prompt injection, and path traversal issues. Generates secure code replacements and environment variable templates.
---

# Security Fixer

Automatically fixes security vulnerabilities found by neckr0ik-security-scanner.

## Quick Start

```bash
# Scan and fix in one command
neckr0ik-security-fixer fix /path/to/skill --auto

# Interactive fix (confirm each change)
neckr0ik-security-fixer fix /path/to/skill

# Generate .env.example only
neckr0ik-security-fixer env /path/to/skill
```

## What This Fixes

### Critical Issues (Auto-fixable)

| Issue | Fix Applied |
|-------|-------------|
| **Hardcoded Secrets** | Replaces with `os.environ.get()` + generates `.env.example` |
| **Shell Injection** | Converts to `subprocess.run()` with `shell=False` |
| **eval/exec** | Wraps with safe alternatives or flags for review |

### High Issues (Auto-fixable)

| Issue | Fix Applied |
|-------|-------------|
| **Prompt Injection** | Adds sanitization wrapper |
| **Path Traversal** | Adds `pathlib` validation |

## How It Works

1. Runs security scan on target skill
2. For each vulnerability, generates fix
3. Applies fix automatically (with `--auto`) or prompts for confirmation
4. Creates `.env.example` with detected secret placeholders
5. Updates `.gitignore` to exclude `.env`

## Example Fixes

### Hardcoded API Key

**Before:**
```python
api_key = "sk-abc123def456..."
```

**After:**
```python
import os
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable required")
```

**Generated .env.example:**
```
OPENAI_API_KEY=your-key-here
```

### Shell Injection

**Before:**
```python
os.system(f"convert {filename} output.png")
```

**After:**
```python
import subprocess
result = subprocess.run(
    ["convert", filename, "output.png"],
    capture_output=True,
    check=True
)
```

### Prompt Injection

**Before:**
```python
prompt = f"User says: {user_input}"
```

**After:**
```python
import re
def sanitize_for_prompt(text: str) -> str:
    return re.sub(r'[<>\{\}\[\]\\]', '', text[:1000])

prompt = f"User says: {sanitize_for_prompt(user_input)}"
```

## Commands

### fix

```bash
neckr0ik-security-fixer fix <skill-path> [options]

Options:
  --auto        Apply all fixes without prompting
  --dry-run     Show what would be fixed without making changes
  --backup      Create .bak files before modifying
```

### env

```bash
neckr0ik-security-fixer env <skill-path>

Generates:
  - .env.example (template with placeholders)
  - Updates .gitignore to exclude .env
```

### report

```bash
neckr0ik-security-fixer report <skill-path> --format json

Outputs a detailed fix report with:
  - Original vulnerable code
  - Fixed code
  - Files modified
  - Manual review items
```

## Safety Features

- **Backup files** created by default (can disable with `--no-backup`)
- **Dry-run mode** shows changes without applying
- **Manual review flagging** for complex issues that need human judgment
- **Git integration** - shows diff before applying

## See Also

- `neckr0ik-security-scanner` - Scan for vulnerabilities first
- `references/fix-templates.md` - Complete fix template library
- `scripts/fixer.py` - Main fixer script