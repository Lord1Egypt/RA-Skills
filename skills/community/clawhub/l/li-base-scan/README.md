# Li Base Scan

A comprehensive security scanning tool integrated with OpenClaw, supporting multiple scanning modes and security assessment capabilities.

## Author

**Beijing Lao Li (北京老李)**

## Features

- 🔍 **Network Scanning**: Nmap integration for port and service discovery
- 🛡️ **Vulnerability Scanning**: Nikto for web vulnerability detection
- 🗄️ **SQL Injection Detection**: SQLMap integration
- 📦 **Container Security**: Trivy for image scanning
- 🔒 **System Compliance**: Lynis for system audit
- 🤖 **AI-Powered Analysis**: LLM-based security report analysis
- 📊 **Report Generation**: Markdown, JSON, and HTML report formats
- 📜 **Scan History**: SQLite-based history management

## Installation

### Prerequisites

Ensure the following tools are installed on your system:

- `nmap` - Network scanner
- `nikto` - Web vulnerability scanner
- `sqlmap` - SQL injection tool
- `trivy` - Container image scanner
- `lynis` - System auditing tool

### Install via ClawHub

```bash
clawhub skills install li-base-scan
```

## Usage

### Basic Scan

```bash
# Quick scan (30 seconds)
li-base-scan 192.168.1.1 --mode quick

# Standard scan (2-5 minutes)
li-base-scan 192.168.1.1 --mode standard

# Full scan (5-10 minutes)
li-base-scan 192.168.1.1 --mode full
```

### Web Application Scan

```bash
# Web vulnerability scan
li-base-scan http://example.com --mode web

# Web + SQL injection scan
li-base-scan http://example.com --mode web_sql
```

### Compliance & Stealth

```bash
# Compliance audit
li-base-scan 192.168.1.1 --mode compliance

# Stealth scan
li-base-scan 192.168.1.1 --mode stealth
```

### LLM Analysis

```bash
# Enable AI-powered analysis (requires LLM_API_KEY)
li-base-scan 192.168.1.1 --mode full --llm
```

## Security Features

- ✅ Target address hashing (SHA-256) - no sensitive data stored
- ✅ File permission restrictions (0o600 for sensitive files)
- ✅ Audit logging with privacy protection
- ✅ Command injection prevention using `shlex.quote()`
- ✅ Single-host limitation (no CIDR/range scanning)
- ✅ Timeout protection (5-30 minutes per command)

## Scan Modes

| Mode | Duration | Description |
|------|----------|-------------|
| `quick` | ~30s | Fast port scan |
| `standard` | 2-5min | Standard security scan |
| `full` | 5-10min | Comprehensive scan |
| `web` | 2-3min | Web vulnerability scan |
| `web_sql` | 3-5min | Web + SQL injection scan |
| `compliance` | Varies | System compliance audit |
| `stealth` | Varies | Stealth mode scan |

## Report Output

Reports are saved in the `reports/` directory:
- `security-report-{timestamp}.md` - Markdown report
- `security-report-{timestamp}.json` - JSON report
- `security-report-{timestamp}.html` - HTML report

## History & Logs

- **Scan History**: Stored in `history.db` (SQLite)
- **Logs**: `~/.openclaw/logs/li-base-scan.log`

## Environment Variables

- `LLM_API_KEY` - API key for LLM-powered analysis
- `LLM_API_URL` - Custom LLM API endpoint

## License

MIT License

## Safety Notice

⚠️ **Important**: This tool is for authorized security testing only. Always ensure you have permission to scan the target systems. Unauthorized scanning may violate laws and regulations.
