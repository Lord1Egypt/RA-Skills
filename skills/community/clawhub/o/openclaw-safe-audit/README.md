# OpenClaw Security Audit

🔒 Security audit and credential hardening toolkit for OpenClaw instances.

## Quick Start

```bash
# Security audit
python audit.py

# Credential hardening (migrate to env vars)
python harden.py
```

## What It Does

### Audit (`audit.py`)
- Scans for sensitive files (.env, .key, .pem)
- Detects credential exposure in config files
- Checks Gateway security configuration
- Generates JSON security reports

### Harden (`harden.py`)
- Backs up your configuration
- Extracts credentials to .env file
- Sanitizes openclaw.json
- Generates platform-specific setup scripts

## Safety First

- ✅ Creates backups before changes
- ✅ Masks credentials in reports
- ✅ No external network calls
- ✅ Respects file permissions

## Requirements

- Python 3.7+
- OpenClaw installed

## License

MIT
