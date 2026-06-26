# MCP Security Audit Skill

An OpenClaw skill for performing enterprise-grade security audits on MCP (Model Context Protocol) servers and skills.

## Features

- 🔍 **Vulnerability Scanning**: Detects hardcoded credentials, insecure bindings, and common vulnerabilities
- 🛡️ **Malware Detection**: Identifies suspicious patterns like eval/exec, shell injection, and potential backdoors
- 📋 **Compliance Checking**: Flags logging and output issues that could lead to data exposure
- 📊 **Security Scoring**: Provides a 0-100 score with letter grade (A+ to F)
- 📝 **Detailed Reports**: Line-by-line findings with remediation guidance
- 🚨 **Severity Levels**: Critical, High, Medium, Low, Info classifications
- 🎯 **Actionable Recommendations**: Prioritized fixes based on risk level

## Installation

```bash
clawhub install mcp-security-audit
```

## Usage

### Basic Audit

```bash
# Audit an MCP server directory
mcp-security-audit ./mcp_server

# Audit a skill directory
mcp-security-audit ./my-skill
```

### With Custom Path

```bash
python audit.py /path/to/mcp/server
```

## Output Example

```
============================================================
MCP SECURITY AUDIT REPORT
============================================================
Path: ./mcp_server
Score: 85/100
Grade: B
------------------------------------------------------------
Summary:
  Critical: 0
  High: 2
  Medium: 5
  Low: 3
  Info: 0
------------------------------------------------------------
Recommendations:
  ⚠️ HIGH: Fix high severity vulnerabilities soon
  🔑 CREDENTIALS: Remove hardcoded credentials, use environment variables or vault
  🌐 NETWORK: Restrict binding to specific interfaces only
------------------------------------------------------------
Detailed Findings:
  [HIGH] Hardcoded API key detected
    Hardcoded API key detected
    Location: config.json:12
    Fix: Remove hardcoded credentials or use secure vault/environment variables
    
  [HIGH] Binding to all interfaces (0.0.0.0)
    Binding to all interfaces (0.0.0.0)
    Location: server.py:45
    Fix: Restrict binding to specific interfaces only
    
  [MEDIUM] Debug logging may leak sensitive info
    Debug logging may leak sensitive info
    Location: main.py:8
    Fix: Review logging and output to prevent sensitive data exposure
    ...
============================================================
```

## Configuration

The skill can be customized by modifying the patterns in `audit.py`:

- `malware_patterns`: Regex patterns for detecting malicious code
- `vulnerability_patterns`: Patterns for security vulnerabilities (credentials, bindings, etc.)
- `compliance_patterns`: Patterns for compliance and data exposure issues

## Requirements

- Python 3.7+
- No external dependencies (uses only standard library)

## Security Notes

- This skill is designed to be run in trusted environments
- Always review findings carefully before making changes
- Consider using in conjunction with other security tools (VirusTotal, Snyk, etc.)
- For enterprise use, integrate with your CI/CD pipeline for continuous security monitoring

## License

MIT

## Author

laosi (did:soul:laosi)