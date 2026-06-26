---
name: log-scrubber
description: Automatically redacts API keys, tokens, and secrets from workspace logs and memory files.
homepage: https://github.com/Heather-Herbert/openclaw-log-scrubber
metadata:
  clawdbot:
    requires:
      env: []
    files: ["scripts/*"]
---

# Log Scrubber

This skill automatically scans your `/root/.openclaw/workspace/` environment, logs, and memory files to detect and redact sensitive information like API keys, tokens, and credentials.

## Features
- **Proactive Scanning**: Scans for known patterns (regex) of common secrets.
- **Automated Redaction**: Sanitizes files in-place while keeping backups of original files (e.g., `.bak` extension).
- **Dry-Run Mode**: Allows you to simulate redaction without modifying files.
- **Security**: Ensures your secrets don't accidentally end up in logs sent to providers or stored in plain-text memory files.

## Usage
To perform a dry-run (check proposed changes without modification):
`python3 /root/.openclaw/workspace/skills/log-scrubber/scripts/scrub.py --dry-run`

To apply changes:
`python3 /root/.openclaw/workspace/skills/log-scrubber/scripts/scrub.py`

## External Endpoints
- This skill does not call any external endpoints. It operates entirely locally.

## Security & Privacy
- This skill performs all redaction operations locally on your machine. No data is sent to external servers.

## Model Invocation
- This skill runs locally and does not autonomously invoke models beyond the standard OpenClaw agent execution.

## Trust Statement
- By using this skill, you agree that it will overwrite files in your workspace with redacted versions. Always ensure you have backups of important data.
