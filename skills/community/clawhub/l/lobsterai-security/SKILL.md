---
name: security
description: Enterprise-grade security framework for LobsterAI with audit logging, RBAC, input validation, output sanitization, code scanning, and dependency vulnerability detection.
version: 1.0.3
author: LobsterAI Security Team
license: Proprietary
priority: 100
tags:
  - security
  - audit
  - rbac
  - compliance
  - validation
  - scanning
environment:
  - name: LOBSTERAI_HOME
    description: Base directory for LobsterAI data and logs
    required: false
    default: ${APPDATA}/LobsterAI (Windows) or ${HOME}/.config/LobsterAI (Linux/macOS)
  - name: LOBSTERAI_AUDIT_SECRET
    description: HMAC secret for audit log signature
    required: false
  - name: LOBSTERAI_USER_ID
    description: Current user identifier for audit trails
    required: false
    default: anonymous
  - name: SKILLS_ROOT
    description: Path to the SKILLs root directory
    required: false
---

# Security

Comprehensive security framework for LobsterAI providing audit logging, role-based access control (RBAC), input validation, output sanitization, code scanning, and dependency vulnerability detection.

## Core Features

### Audit Logger
- Records all skill executions with timestamps, user context, and input/output
- JSON-structured logs for easy analysis
- Automatic log rotation (90 days retention)
- Encrypted storage support

### Authorizer (RBAC)
- Role-based access control configuration
- Fine-grained permission management
- JSON-based role definitions
- Session validation

### Input Validator
- Path traversal prevention
- Dangerous command detection (rm, del, eval, etc.)
- Cron expression validation
- Working directory restrictions

### Output Sanitizer
- Automatic redaction of sensitive data (passwords, API keys, tokens)
- Error message sanitization
- Safe error formatting for user display

### Code Scanner
- Static code analysis for common vulnerabilities
- Pattern-based malicious code detection
- Configurable scan rules

### Dependency Scanner
- NPM vulnerability scanning (npm audit)
- Python package vulnerability detection (pip-audit)
- Automated dependency checking

## Usage

All security features are available for import by other skills:

```python
from security.audit_logger import audit_log_skill_start, audit_log_skill_end
from security.authorizer import Authorizer
from security.input_validator import InputValidator, ValidationError
from security.output_sanitizer import sanitize_text, create_safe_error
from security.code_scanner import CodeScanner
from security.dependency_scanner import DependencyScanner
```

## Configuration

Copy `rbac_config.example.json` to `rbac_config.json` and customize roles and permissions.

### Scan Scope

The code scanner and dependency scanner are designed to scan **all skills** in the SKILLs directory when invoked explicitly (e.g., `python -m security.code_scanner --skill all`). This allows comprehensive security assessment across your entire LobsterAI installation.

**Privacy Note**: Scanning all skills grants this module read access to all skill code and dependencies. This is intentional for a security audit tool, but users should be aware of the broad read scope. Ensure you trust the skill source before enabling full-system scanning.

To limit scanning to specific skills, invoke with explicit skill IDs:
```bash
python -m security.code_scanner --skill web-search --skill scheduled-task
```

## Environment Variables

This skill requires the following environment variables to function correctly:

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `LOBSTERAI_HOME` | Base directory for LobsterAI data and logs | Yes (if not using default) | `${APPDATA}/LobsterAI` (Windows) or `${HOME}/.config/LobsterAI` (Linux/macOS) |
| `LOBSTERAI_AUDIT_SECRET` | HMAC secret for audit log signature (optional) | No | - |
| `LOBSTERAI_USER_ID` | Current user identifier for audit trails | No | `anonymous` |
| `SKILLS_ROOT` | Path to the SKILLs root directory | No (auto-detected) | Parent directory of the current skill |

**Note**: Ensure `LOBSTERAI_HOME/logs/security/` exists and is writable.

## Deployment

See `DEPLOYMENT.md` for detailed deployment instructions, security hardening checklist, and incident response procedures.

## Testing

Run `python tests.py` to execute the test suite.

## Integration

This module integrates seamlessly with LobsterAI's skill execution pipeline, providing:
- Pre-execution validation
- Runtime monitoring
- Post-execution sanitization
- Comprehensive audit trails

## Security Maturity

⭐⭐⭐☆☆ (3/10) - Active development

We are continuously improving our security posture. See `SECURITY.md` for the complete security architecture and best practices.
