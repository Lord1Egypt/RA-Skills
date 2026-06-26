---
name: openclaw-security-auditor
description: OpenClaw Security Auditor (OSA) - Comprehensive security auditing tool for OpenClaw deployments. Provides 60-second security diagnosis, risk scoring (0-100), bilingual reports (Chinese/English), and automated fix suggestions. Use when users request security audits, vulnerability scanning, configuration validation, or security hardening for their OpenClaw installations.
license: MIT
---

# OpenClaw Security Auditor Skill

## Overview

This skill provides comprehensive security auditing capabilities for OpenClaw deployments. It can scan OpenClaw configurations, identify security vulnerabilities, provide risk scores, and suggest remediation steps.

## When to Use This Skill

- User requests security audit or vulnerability assessment
- User wants to check OpenClaw security configuration  
- User needs security hardening recommendations
- User asks about OpenClaw security best practices
- User wants to validate their OpenClaw configuration
- User mentions "security", "audit", "vulnerability", "hardening" in context of OpenClaw

## Core Capabilities

### Security Scanning
- **47-point security check**: Covers 7 major security domains
- **Gateway Configuration**: Binding modes, authentication, tokens
- **Session Security**: dmScope, pairing strategies, timeouts  
- **Tool Permissions**: exec profiles, allowed tools, filesystem access
- **Channel Security**: dmPolicy, mention requirements, allowlists
- **Network Security**: Firewall status, port exposure
- **Logging Security**: Log levels, sensitive data handling
- **Skill Security**: Auto-install policies, source restrictions

### Risk Assessment
- **0-100 Security Score**: Comprehensive risk scoring system
- **Three Security Modes**: Conservative, Balanced (recommended), Aggressive
- **Severity Classification**: Critical, High, Medium, Low, Info levels
- **Bilingual Reporting**: Chinese/English dual-language output

### Automated Remediation
- **Fix Suggestions**: Specific commands for each identified issue
- **Mode Recommendations**: Guidance on appropriate security modes
- **Configuration Templates**: Best practice configuration examples

## Usage Workflow

### Step 1: Security Scan
Run comprehensive security scan on OpenClaw configuration:

```python
# Import required modules
from scripts.security_scanner import SecurityScanner
from scripts.report_generator import ReportGenerator

# Scan current OpenClaw configuration
scanner = SecurityScanner(config_path="~/.openclaw/openclaw.json", mode="balanced")
results = scanner.scan()
```

### Step 2: Generate Report  
Generate bilingual security report:

```python
# Generate bilingual Markdown report
reporter = ReportGenerator(results, mode="balanced")
bilingual_report = reporter.generate("bilingual")

# Save report to user's directory
with open("~/.openclaw/security-audit-report.md", "w") as f:
    f.write(bilingual_report)
```

### Step 3: Provide Recommendations
Based on scan results, provide specific remediation steps:

- **Critical Issues**: Immediate fixes required
- **High Issues**: Fix as soon as possible  
- **Medium/Low Issues**: Optimization suggestions
- **Security Mode Selection**: Recommend appropriate mode based on use case

## Available Scripts

### Core Scripts
- `scripts/security_scanner.py` - Main security scanning engine
- `scripts/report_generator.py` - Multi-format report generation
- `scripts/config_fixer.py` - Automated configuration fixing
- `scripts/i18n.py` - Bilingual translation support

### Utility Scripts  
- `scripts/scan_current.py` - Quick scan of current configuration
- `scripts/fix_security.py` - Apply security fixes interactively
- `scripts/debug_session.py` - Debug session configuration issues

## Reference Documentation

### Security Best Practices
- `references/security-modes.md` - Detailed security mode configurations
- `references/config-guide.md` - OpenClaw security configuration guide
- `references/vulnerability-db.md` - Common OpenClaw security vulnerabilities

### API Documentation
- `references/api-reference.md` - Complete API reference for security auditor
- `references/integration-guide.md` - CI/CD and automation integration guide

## Output Formats

### Report Types
- **Markdown**: Human-readable bilingual reports
- **JSON**: Machine-readable format for automation
- **HTML**: Visual web-based reports

### Report Structure
Each report includes:
- Security score and risk level
- Summary of passed/failed checks
- Detailed issue descriptions with severity levels
- Specific fix commands and recommendations
- Security mode guidance

## Security Mode Guidance

### Conservative Mode (Production)
- **Use Case**: Production environments, sensitive data
- **Score Target**: 95+
- **Key Settings**: loopback binding, token auth, minimal permissions

### Balanced Mode (Development) ⭐
- **Use Case**: Personal development, small teams  
- **Score Target**: 75-90
- **Key Settings**: loopback binding, reasonable permissions, standard logging

### Aggressive Mode (Testing)
- **Use Case**: Isolated test environments only
- **Score Target**: 40-60  
- **Key Settings**: Full permissions, minimal restrictions

## Example Usage

### Basic Security Audit
```
User: "Can you audit my OpenClaw security configuration?"

Assistant: 
1. Load security_scanner.py script
2. Run scan on ~/.openclaw/openclaw.json
3. Generate bilingual report
4. Present security score and key findings
5. Provide specific fix recommendations
```

### Mode Recommendation
```
User: "What security mode should I use for my development setup?"

Assistant:
1. Explain three security modes
2. Recommend Balanced mode for development
3. Provide configuration examples
4. Show expected security score range
```

### Vulnerability Remediation
```
User: "How do I fix the security issues in my OpenClaw setup?"

Assistant:
1. Run security scan to identify specific issues
2. Categorize issues by severity
3. Provide step-by-step fix commands
4. Verify fixes with re-scan if requested
```

## Limitations and Considerations

### Scope Limitations
- Only scans OpenClaw configuration files
- Does not perform network penetration testing
- System-level security (firewall, OS hardening) requires manual intervention
- Cannot modify configurations without user approval

### Safety Considerations
- Always backup configuration before applying fixes
- Test fixes in non-production environments first
- Some fixes require system administrator privileges
- Conservative mode may break existing functionality

## Integration Capabilities

### CI/CD Integration
- JSON output format for automated security gates
- Exit codes based on security score thresholds
- Integration with GitHub Actions, GitLab CI, etc.

### Monitoring Integration  
- Scheduled security scans
- Trend analysis and reporting
- Alert notifications for critical issues

## Getting Started

To use this skill, simply ask for a security audit of your OpenClaw configuration. The skill will automatically:

1. Locate your OpenClaw configuration file
2. Perform comprehensive security scanning
3. Generate detailed bilingual report
4. Provide actionable security recommendations

The skill is designed to be safe and non-destructive - it only reads configuration files and provides recommendations, never makes automatic changes without explicit user approval.