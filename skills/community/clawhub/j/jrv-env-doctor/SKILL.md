---
name: jrv-env-doctor
description: Validate .env files for common issues — detect leaked secrets (AWS keys, GitHub tokens, Stripe keys, JWTs), find duplicate variables, flag empty values, compare against .env.example templates, and catch syntax errors. Use when asked to check .env files, audit environment variables, scan for leaked secrets, validate env configuration, or compare .env against .env.example. No external dependencies.
---

# Env Doctor

Validate and audit .env files for secrets, duplicates, syntax issues, and missing variables.

## Quick Start

```bash
python3 scripts/env_doctor.py .env
python3 scripts/env_doctor.py .env --example .env.example
python3 scripts/env_doctor.py .env --strict --json
```

## Features

- **Secret scanning** — detects AWS keys, GitHub tokens, Stripe keys, Slack tokens, Google API keys, JWTs, private key blocks, and more
- **Duplicate detection** — flags variables defined more than once
- **Example comparison** — compares .env against .env.example to find missing or extra vars
- **Syntax validation** — catches malformed lines, unquoted values with spaces
- **Placeholder detection** — warns about values like "changeme", "your-api-key-here"
- **Exit codes** — 0 = healthy, 1 = issues, 2 = secret leaks (CI-friendly)
- **No dependencies** — Python stdlib only

## Options

| Flag | Description |
|------|-------------|
| `--example PATH` | .env.example file for comparison |
| `--json` | Output structured JSON |
| `--strict` | Treat empty values as errors |

## Secret Patterns Detected

AWS Access/Secret Keys, GitHub Tokens (ghp_, gho_, ghs_, ghu_, github_pat_), Slack Tokens, Stripe Keys, Google API Keys, Private Key Blocks, JWTs, Twilio Tokens, SendGrid Keys, Heroku API Keys, and generic high-entropy secrets.
