---
name: neckr0ik-security-suite
version: 1.0.0
description: Complete security suite for OpenClaw skills. Includes scanner (detects vulnerabilities), fixer (auto-remediates issues), and compliance reports (SOC2, HIPAA, PCI-DSS). Bundle discount - all three tools for the price of two.
---

# Security Suite for OpenClaw Skills

Complete security toolkit: scan, fix, and certify your skills.

## What's Included

### 1. Security Scanner
Detects 20+ vulnerability types:
- Hardcoded secrets (API keys, passwords, tokens)
- Shell injection risks
- Code execution vulnerabilities
- Prompt injection vectors
- Path traversal risks
- Network access issues
- Dependency vulnerabilities

### 2. Security Fixer
Auto-fixes common issues:
- Converts hardcoded secrets to environment variables
- Rewrites shell commands safely
- Adds prompt sanitization
- Implements path validation
- Generates .env.example templates

### 3. Compliance Reports
Generate certification reports for:
- SOC 2 Type II
- HIPAA
- PCI-DSS
- GDPR
- Custom frameworks

## Quick Start

```bash
# Scan a skill
neckr0ik-security-suite scan /path/to/skill

# Fix issues automatically
neckr0ik-security-suite fix /path/to/skill --auto

# Generate compliance report
neckr0ik-security-suite report /path/to/skill --framework soc2

# Full audit + fix + certify
neckr0ik-security-suite certify /path/to/skill --framework hipaa
```

## Commands

### scan

```bash
neckr0ik-security-suite scan <skill-path> [options]

Options:
  --format json|markdown|summary    Output format
  --severity critical|high|medium   Minimum severity to report
  --exclude <patterns>              File patterns to exclude
```

### fix

```bash
neckr0ik-security-suite fix <skill-path> [options]

Options:
  --auto          Apply all fixes without prompting
  --dry-run       Show changes without applying
  --no-backup     Do not create backup files
```

### report

```bash
neckr0ik-security-suite report <skill-path> [options]

Options:
  --framework soc2|hipaa|pci|gdpr   Compliance framework
  --format json|markdown|pdf        Output format
  --output <file>                   Output file path
```

### certify

```bash
neckr0ik-security-suite certify <skill-path> [options]

Options:
  --framework soc2|hipaa|pci|gdpr   Compliance framework
  --auto-fix                        Apply fixes before certification
  --output <file>                   Certificate output path
```

## Compliance Frameworks

### SOC 2 Type II

Checks for:
- Access controls (CC6.1)
- Encryption (CC6.7)
- Change management (CC8.1)
- Risk mitigation (CC9.2)

### HIPAA

Checks for:
- PHI protection (§164.312)
- Access controls (§164.312(a))
- Audit controls (§164.312(b))
- Integrity (§164.312(c))

### PCI-DSS

Checks for:
- Cardholder data protection (Req 3)
- Encryption (Req 4)
- Access control (Req 7-8)
- Audit logs (Req 10)

### GDPR

Checks for:
- Data minimization (Art 5)
- Security measures (Art 32)
- Access controls (Art 32)
- Audit trails (Art 30)

## Sample Output

### Compliance Report (SOC 2)

```
╔══════════════════════════════════════════════════════════════╗
║         SECURITY COMPLIANCE CERTIFICATE - SOC 2 TYPE II      ║
╠══════════════════════════════════════════════════════════════╣
║ Skill: my-ai-agent                                           ║
║ Version: 1.2.0                                               ║
║ Scan Date: 2026-03-06                                        ║
║ Framework: SOC 2 Type II                                     ║
╠══════════════════════════════════════════════════════════════╣
║ STATUS: ✅ COMPLIANT                                         ║
╠══════════════════════════════════════════════════════════════╣
║ Controls Checked:                                            ║
║   ✅ CC6.1 - Access Controls                                 ║
║   ✅ CC6.7 - Encryption                                       ║
║   ✅ CC8.1 - Change Management                               ║
║   ✅ CC9.2 - Risk Mitigation                                 ║
╠══════════════════════════════════════════════════════════════╣
║ Vulnerabilities Found: 0                                     ║
║ Warnings: 2 (documentation recommended)                      ║
║ Certificate ID: SOC2-2026-03-06-A7B3C9D2                     ║
╚══════════════════════════════════════════════════════════════╝
```

## Integration

### CI/CD Pipeline

```yaml
# .github/workflows/security.yml
name: Security Audit

on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Install Security Suite
        run: clawhub install neckr0ik-security-suite
      
      - name: Run Security Scan
        run: neckr0ik-security-suite scan ./skill/
      
      - name: Check Compliance
        run: neckr0ik-security-suite certify ./skill/ --framework soc2
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

neckr0ik-security-suite scan ./skills/ --severity high
if [ $? -ne 0 ]; then
    echo "❌ Security issues found. Fix before committing."
    exit 1
fi
```

## Pricing

| Tool | Standalone | In Suite |
|------|-----------|----------|
| Scanner | $10 | ✅ Included |
| Fixer | $15 | ✅ Included |
| Compliance | $20 | ✅ Included |
| **Total** | **$45** | **$30** |

**Save 33% with the suite bundle!**

## See Also

- `neckr0ik-security-scanner` - Standalone scanner
- `neckr0ik-security-fixer` - Standalone fixer
- `references/compliance-frameworks.md` - Detailed framework requirements
- `scripts/suite.py` - Main suite script