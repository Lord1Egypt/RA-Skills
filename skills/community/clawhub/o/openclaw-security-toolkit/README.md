# OpenClaw Security Guard

A comprehensive security tool for OpenClaw users to protect their AI assistant.

## Features

- 🔍 **Security Audit** - Comprehensive security configuration check
- 🔐 **Secret Scanner** - Detect exposed API keys and tokens
- 👥 **Access Control** - Manage devices, users, and permissions
- 🔑 **Token Manager** - Rotate and validate tokens
- 📊 **Security Report** - Generate detailed security reports
- 🛡️ **Hardening** - Apply security best practices

## Installation

```bash
# Clone the repository
git clone https://github.com/hkall/openclaw-security-toolkit.git

# No external dependencies required (uses Python stdlib)
```

## Requirements

- Python 3.6+
- OpenClaw installed

## Usage

### Security Audit

```bash
# Run security audit
python3 scripts/main.py audit

# Deep audit with auto-fix
python3 scripts/main.py audit --deep --fix
```

### Secret Scanner

```bash
# Scan for secrets
python3 scripts/main.py scan

# Scan for specific pattern
python3 scripts/main.py scan --pattern "sk-"
```

### Security Report

```bash
# Generate table report (default)
python3 scripts/main.py report

# Generate markdown report
python3 scripts/main.py report --format md -o security.md

# Generate JSON report
python3 scripts/main.py report --format json
```

### Token Management

```bash
# Check token status
python3 scripts/main.py token status

# Rotate tokens
python3 scripts/main.py token rotate
```

### Access Control

```bash
# List all access entries
python3 scripts/main.py access list

# List paired devices
python3 scripts/main.py access devices

# List users
python3 scripts/main.py access users
```

### Security Hardening

```bash
# Check hardening status
python3 scripts/main.py harden

# Apply hardening fixes
python3 scripts/main.py harden --fix
```

### Quick Status

```bash
python3 scripts/main.py status
```

## Options

| Option | Description |
|--------|-------------|
| `--format, -f` | Output format: json, md, table (default: table) |
| `--lang, -l` | Language: en, zh (default: auto-detect) |
| `--quiet, -q` | Quiet mode, only output results |
| `--verbose, -v` | Verbose output |
| `--output, -o` | Output file path |
| `--deep` | Deep scan mode |
| `--fix` | Auto-fix issues where possible |

## Security Checks

| Category | Checks |
|----------|--------|
| Config | Gateway bind, auth mode, token strength |
| Secrets | API keys, tokens, passwords, private keys |
| Access | Devices, users, channels, sessions |
| Network | Public exposure, open ports |

## Output Example

```
🔐 OpenClaw Security Guard v1.0.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 Security Score: 72/100 ⚠️

🔴 HIGH RISK
  • API Key exposed in config file
    Location: ~/.openclaw/openclaw.json:15

🟡 MEDIUM RISK
  • Token rotation recommended
    Last rotation: 30 days ago

🟢 PASSED
  ✓ Gateway properly secured
  ✓ No weak passwords detected
```

## Languages

- English (en)
- 中文 (zh)

Auto-detected based on system locale.

## License

MIT License

## Author

hkall

## Version

v1.0.0