---
name: openclaw-security-audit
description: Security audit and credential hardening tool for OpenClaw instances. Scan for sensitive files, detect credential exposure, check gateway configuration, and migrate credentials to environment variables. Essential for maintaining a secure OpenClaw deployment.
version: 1.0.0
author: Community
license: MIT
tags: [security, audit, credentials, hardening, privacy]
---

# OpenClaw Security Audit

A comprehensive security toolkit for OpenClaw instances. Protect your credentials, audit your configuration, and maintain best security practices.

## Features

- **Sensitive File Scanning** - Detect .env, .key, .pem files and other sensitive artifacts
- **Credential Exposure Detection** - Find API keys, secrets, tokens, and passwords in config files
- **Gateway Security Check** - Verify gateway bind mode and authentication settings
- **Credential Hardening** - Automatically migrate credentials from config files to environment variables
- **JSON Reports** - Generate detailed audit reports for review

## Installation

```bash
# Clone to your OpenClaw skills directory
cd ~/.openclaw/skills
git clone <repository> openclaw-security-audit

# Or manually copy the skill files
```

## Usage

### Security Audit

Run a comprehensive security audit:

```bash
python ~/.openclaw/skills/openclaw-security-audit/audit.py
```

This will:
1. Scan for sensitive files
2. Check for credential exposure in openclaw.json
3. Verify gateway security configuration
4. Generate a JSON report with findings

### Credential Hardening

Migrate credentials to environment variables:

```bash
python ~/.openclaw/skills/openclaw-security-audit/harden.py
```

This will:
1. Backup your current configuration
2. Extract credentials from openclaw.json
3. Create .env file with credentials
4. Sanitize openclaw.json (replace with placeholders)
5. Generate setup scripts for Windows/macOS/Linux

**IMPORTANT**: After running harden.py, you must set environment variables before OpenClaw can access credentials.

### Custom Configuration

Edit `config.json` to customize scanning behavior:

```json
{
  "exclude_dirs": ["node_modules", ".git", "__pycache__"],
  "whitelist": ["secret-input.ts"],
  "sensitive_extensions": [".env", ".key", ".pem"],
  "sensitive_keywords": ["password", "secret", "credentials"]
}
```

## Security Checks

### What We Check

| Check | Description | Risk Level |
|-------|-------------|------------|
| Sensitive files | .env, .key, .pem files | MEDIUM |
| Credential exposure | API keys, secrets in config | HIGH/CRITICAL |
| Gateway bind mode | 0.0.0.0 exposure | CRITICAL |
| Gateway auth | Missing authentication | HIGH |
| File permissions | Config file permissions | INFO |

### Risk Levels

- **CRITICAL**: Immediate action required
- **HIGH**: Fix within 24 hours
- **MEDIUM**: Fix within a week
- **LOW**: Monitor and review
- **INFO**: For awareness

## Best Practices

1. **Run audit weekly** - Schedule regular security checks
2. **Harden immediately** - Migrate credentials to env vars on first run
3. **Backup before hardening** - Always backup configs before changes
4. **Secure .env files** - Never commit .env to version control
5. **Rotate credentials** - Regularly update API keys and tokens

## Report Location

Audit reports are saved to:
- `~/.openclaw/security-tools/security_report_YYYYMMDD_HHMMSS.json`

## Supported Platforms

- Windows (PowerShell scripts)
- macOS (Bash scripts)
- Linux (Bash scripts)

## Privacy & Safety

This tool:
- ✅ Only reads your OpenClaw configuration
- ✅ Does not transmit data externally
- ✅ Masks credential values in reports
- ✅ Creates backups before modifications
- ✅ Respects file permissions

This tool does NOT:
- ❌ Send data to external servers
- ❌ Modify system files outside ~/.openclaw
- ❌ Store or log actual credential values
- ❌ Require elevated permissions

## Requirements

- Python 3.7+
- OpenClaw installed
- Read access to ~/.openclaw directory

## License

MIT License - Feel free to use, modify, and distribute.

## Contributing

Contributions welcome! Please ensure:
- Code follows Python PEP 8
- No hardcoded credentials or paths
- Privacy-respecting practices
- Clear documentation

## Disclaimer

This tool is for security auditing your own OpenClaw instance. Always review changes before applying them. The authors are not responsible for misconfiguration or data loss.
