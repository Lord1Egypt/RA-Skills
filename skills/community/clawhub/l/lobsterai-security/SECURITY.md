# 🔒 Security Policy

**LobsterAI Security Skill** is a comprehensive security framework for LobsterAI, providing audit logging, RBAC, input validation, output sanitization, code scanning, and dependency vulnerability detection.

**Maintainer**: LobsterAI Security Team
**Contact**: security@lobsterai.com (for security issues only)
**Repository**: https://github.com/stoneyhoo/lobsterai-security-skill

---

## 📋 Supported Versions

We actively maintain the following versions:

| Version | Supported | Security Updates |
|---------|-----------|------------------|
| 1.0.x   | ✅ Yes    | ✅ Yes           |
| < 1.0   | ❌ No     | ❌ No            |

**Please always use the latest version.**

---

## 🐛 Reporting a Vulnerability

We take security issues seriously. If you discover a vulnerability in this skill or any LobsterAI component, please report it responsibly.

### How to Report

**Email**: `security@lobsterai.com`

Please include:
- Description of the vulnerability
- Steps to reproduce (if applicable)
- Potential impact
- Suggested fix (optional)
- Your contact information for follow-up

### What to Expect

- **Acknowledgment**: Within 48 hours we will acknowledge receipt of your report.
- **Status Update**: Within 7 days we will provide an initial assessment and planned resolution timeline.
- **Resolution**: Critical vulnerabilities will be addressed within 30 days, depending on complexity.
- **Disclosure**: Public disclosure will be coordinated with the reporter after a fix is available. We request a **90-day embargo** on public discussion to allow time for a patch to be developed and deployed.

### Security Best Practices

This skill implements a defense-in-depth strategy:

1. **Input Validation**: All user inputs are validated against path traversal, command injection, and DoS patterns.
2. **Output Sanitization**: Sensitive data (passwords, API keys, tokens) is automatically redacted from logs and outputs.
3. **RBAC**: Role-based access control enforces least-privilege permissions.
4. **Audit Logging**: All security-relevant events are logged with tamper-evident signatures (when `LOBSTERAI_AUDIT_SECRET` is configured).
5. **Code Scanning**: Built-in static analysis detects dangerous patterns (eval, subprocess with shell=True, hardcoded secrets).
6. **Dependency Scanning**: Checks for known vulnerabilities in Python and JavaScript dependencies.

### Security Requirements for Deployment

- **Python**: 3.8+ (tested on 3.11.9)
- **No hardcoded secrets**: All credentials must be provided via environment variables or configuration files.
- **No sudo/root**: The skill should run with least privileges. Do **not** run LobsterAI or skills as root/Administrator.
- **File permissions**: Restrict access to `security/` directory and audit logs to authorized users only (optional but recommended).
- **Network isolation**: Skills that access external resources should operate in a sandboxed environment if possible.

### Known Limitations

- Audit log integrity depends on proper configuration of `LOBSTERAI_AUDIT_SECRET`. Without it, logs are not cryptographically signed.
- Input validation regex patterns may have edge cases; defense-in-depth is recommended.
- Code scanner only supports Python and JavaScript; other languages are not analyzed.
- Dependency scanner relies on external databases (GitHub Advisory, NVD) for vulnerability data; offline environments need manual database updates.

### Security Checklist for Users

Before deploying this skill in production:

- [ ] Set a strong, randomly generated `LOBSTERAI_AUDIT_SECRET` (minimum 32 characters)
- [ ] Configure RBAC roles according to the principle of least privilege
- [ ] Review and customize `input_validator.py` patterns for your environment
- [ ] Enable regular code scans (daily) and dependency scans (weekly)
- [ ] Ensure audit log directory is not world-writable
- [ ] Backup `rbac_config.json` and audit logs regularly
- [ ] Monitor audit logs for security incidents
- [ ] Keep LobsterAI and all skills updated to latest versions

---

## 🔐 Responsible Disclosure

We follow the industry standard **90-day disclosure policy**:

1. Security researcher reports vulnerability
2. We acknowledge and begin investigating (≤ 48 hours)
3. We develop a fix and test it
4. We coordinate with reporter for validation (≤ 30 days typical)
5. We release a security patch and advisory
6. Public disclosure is made after fix is available (reporter may choose to be credited or anonymous)

We do **not** pursue legal action against good-faith security researchers who follow this policy.

---

## 📚 Additional Resources

- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide with security hardening recommendations
- [TECHNICAL_DOCUMENTATION.md](TECHNICAL_DOCUMENTATION.md) - Detailed architecture and API reference
- [SKILL.md](SKILL.md) - Skill metadata and usage instructions

---

**Security is a shared responsibility.** If you have questions or concerns, please contact the LobsterAI Security Team.
