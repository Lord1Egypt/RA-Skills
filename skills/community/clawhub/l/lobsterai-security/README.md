# 🛡️ LobsterAI Security Framework

Enterprise-grade security module for LobsterAI providing comprehensive protection through audit logging, role-based access control, input validation, output sanitization, code scanning, and dependency vulnerability detection.

[![License: Proprietary](https://img.shields.io/badge/license-Proprietary-red.svg)](https://github.com/stoneyhoo/lobsterai-security-skill/blob/main/LICENSE)
[![Version: 1.0.0](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/stoneyhoo/lobsterai-security-skill/releases/tag/v1.0.0)
[![Official: true](https://img.shields.io/badge/official-true-green.svg)](https://github.com/stoneyhoo/lobsterai-security-skill)

## 📋 Features

- **Audit Logging** - Comprehensive JSON-structured logs tracking all skill executions
- **RBAC** - Role-based access control with flexible permission management
- **Input Validation** - Path traversal prevention, dangerous command blocking
- **Output Sanitization** - Automatic redaction of passwords, API keys, tokens
- **Code Scanning** - Static analysis for vulnerability detection
- **Dependency Scanning** - Automated NPM and Python package vulnerability checks

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/stoneyhoo/lobsterai-security-skill.git
cd lobsterai-security-skill

# Install dependencies
pip install -r requirements.txt

# Configure RBAC
cp rbac_config.example.json rbac_config.json
# Edit rbac_config.json with your roles and permissions
```

### Basic Usage

```python
from security.audit_logger import audit_log_skill_start, audit_log_skill_end
from security.input_validator import InputValidator
from security.output_sanitizer import sanitize_text

# Log skill execution
audit_log_skill_start('my-skill', {'input': 'data'})

# Validate user input
validator = InputValidator(allowed_workdir='/safe/path')
validator.validate_all('my-skill', user_input)

# Sanitize error messages
safe_error = sanitize_text(str(error))

audit_log_skill_end('my-skill', {'result': 'success'}, duration_ms=150)
```

## 📁 Project Structure

```
security/
├── SKILL.md              # Skill metadata and documentation
├── README.md             # This file
├── __init__.py           # Package initialization
├── audit_logger.py       # Audit logging module
├── authorizer.py         # RBAC authorization module
├── code_scanner.py       # Static code analysis
├── dependency_scanner.py # Dependency vulnerability scanning
├── input_validator.py    # Input validation and sanitization
├── output_sanitizer.py   # Output data redaction
├── rbac_config.example.json  # RBAC configuration template
├── tests.py              # Test suite
├── scripts/              # Helper scripts
│   ├── daily_code_scan.ps1
│   ├── weekly_rbac_audit.ps1
│   └── integrate_audit.py
├── setup.py              # Python package setup
├── MANIFEST.in           # Package manifest
└── requirements.txt      # Python dependencies
```

## 🔒 Security Architecture

The security framework implements a defense-in-depth strategy:

```
┌─────────────────────────────────────────────┐
│  Pre-Execution Validation                   │
│  • Session authentication                   │
│  • Skill authorization (enabled status)    │
│  • Input validation                        │
│  • Rate limiting                           │
└─────────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────────┐
│  Runtime Monitoring                        │
│  • Behavior tracking (file/network access) │
│  • Resource limits (CPU, memory, time)     │
│  • Anomaly detection                       │
│  • Real-time auditing                      │
└─────────────────────────────────────────────┘
                ↓
┌─────────────────────────────────────────────┐
│  Post-Execution Sanitization               │
│  • Sensitive data filtering                │
│  • Error message desensitization           │
│  • Secure logging                          │
└─────────────────────────────────────────────┘
```

## 📚 Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deployment guide and security hardening
- **[TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md)** - Detailed API reference and architecture
- **[SECURITY.md](SECURITY.md)** - Security policy and vulnerability reporting
- **[UPLOAD_GUIDE.md](UPLOAD_GUIDE.md)** - Upload and installation instructions
- **[SKILL_MARKET_SUBMISSION.md](SKILL_MARKET_SUBMISSION.md)** - Community distribution guide

## 🧪 Testing

Run the test suite:

```bash
python tests.py
```

## 📦 Packaging

Create distribution packages:

```bash
python setup.py sdist bdist_wheel
```

Packages will be generated in the `dist/` directory.

## 🔐 Security Best Practices

This module implements security best practices:

- ✅ No hardcoded credentials
- ✅ All user inputs validated
- ✅ Sensitive data automatically redacted from logs
- ✅ Comprehensive audit trails
- ✅ RBAC for fine-grained access control
- ✅ Path traversal protection
- ✅ Dependency vulnerability scanning

See [SECURITY.md](https://github.com/stoneyhoo/lobsterai-security-skill/blob/main/SECURITY.md) for the complete security architecture.

## 📝 License

This software is proprietary and confidential. All rights reserved.

## 🤝 Contributing

This is an official LobsterAI security module. For security issues, please contact the LobsterAI Security Team directly through your internal channels.

## 📞 Support

- GitHub Issues: https://github.com/stoneyhoo/lobsterai-security-skill/issues
- Documentation: https://github.com/stoneyhoo/lobsterai-security-skill/wiki
- Security Team: Contact via internal LobsterAI channels

## 📜 Changelog

### v1.0.0 (2026-03-18)
- Initial release
- Complete security framework with audit logging, RBAC, validation, sanitization
- Code and dependency scanning capabilities
- Comprehensive test coverage
- Full documentation

---

**Maintained by:** LobsterAI Security Team
**Official Repository:** https://github.com/stoneyhoo/lobsterai-security-skill
