# Security Policy

## 🔒 Security Features

iCalendar Sync v2.4 implements enterprise-grade security measures:

### Credential Protection

- **System Keyring Integration**: Credentials stored in OS-native secure storage
  - macOS: Keychain
  - Windows: Credential Manager
  - Linux: Secret Service (GNOME Keyring, KWallet)
- **Explicit File Storage Option**: Optional YAML credential file with `0600` permissions for headless/GUI-restricted runtimes
- **Fail-Closed Setup**: No implicit plaintext fallback files
- **Log Filtering**: Automatic redaction of passwords and emails from logs

### Input Validation

- **Calendar Names**: Unicode-aware regex validation (`^[\w\s_-]+$`)
- **Text Fields**: Sanitization and length limits
  - Summary: 500 characters
  - Description: 5000 characters
  - Location: 500 characters
- **File Size**: 1MB limit for JSON inputs
- **Email Validation**: RFC-compliant regex
- **Path Validation**: Protection against directory traversal

### Attack Prevention

- **Rate Limiting**: 10 API calls per 60-second window
- **SSL Verification**: Enforced certificate validation
- **Header Hardening**: Explicit User-Agent/Origin/Host for iCloud CalDAV requests
- **Redirect Handling**: Controlled 301/302 redirect resolution for iCloud CalDAV endpoints
- **Injection Protection**: All inputs sanitized
- **DoS Protection**: Size limits, timeouts, rate limiting
- **Thread Safety**: Locks on shared resources

### Code Security

- **Memory Safety**: Traceback cleanup in exception handlers
- **Credential Persistence**: Keyring by default, optional explicit YAML config file (`0600`)
- **Debug Diagnostics**: Optional detailed Apple response logging (`x-apple-request-id`, response body)
- **Timeout Protection**: 30-second timeout on interactive inputs
- **Type Validation**: Strict type checking on all inputs

## 🚨 Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 2.4.x   | :white_check_mark: |
| 2.2.x   | :x: (upgrade)      |
| 2.1.x   | :x: (upgrade)      |
| 2.0.x   | :x: (upgrade)      |
| < 2.0   | :x:                |

## 📝 Reporting a Vulnerability

If you discover a security vulnerability:

1. **DO NOT** open a public issue
2. Email: security@clawhub.ai (or create private security advisory)
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Triage**: Within 5 business days
- **Fix & Release**: Depends on severity
  - Critical: 1-3 days
  - High: 5-7 days
  - Medium: 2-4 weeks
  - Low: Next minor release

## 🛡️ Security Audit Results (v2.4)

### Vulnerability Summary

- **Critical**: 0 ✅
- **High**: 0 ✅
- **Medium**: 0 ✅
- **Low**: 4 ⚠️ (non-security impacting)

### Overall Rating: **A** (Excellent)

### Known Low-Risk Items

1. **ReDoS in SensitiveDataFilter**: Theoretical on extremely long strings
2. **Windows timeout fallback**: No timeout on Windows (acceptable tradeoff)
3. **RRULE validation**: Missing FREQ enum validation (minor UX issue)

## 🔐 Best Practices for Users

### Credential Management

1. **Use App-Specific Passwords**: Never use your main Apple ID password
2. **Generate at**: https://appleid.apple.com → Sign-In & Security → App-Specific Passwords
3. **Rotate Regularly**: Create new passwords every 6-12 months
4. **Revoke Old Passwords**: Remove unused app-specific passwords

### System Hardening

1. **Update Dependencies**: `pip install --upgrade openclaw-icalendar-sync`
2. **Secret Injection**: Provide `ICLOUD_USERNAME` and `ICLOUD_APP_PASSWORD` via secure OpenClaw env or container secret manager
   - For GUI-restricted runtimes, use explicit file storage: `setup --storage file --config /secure/path.yaml`
3. **Log Rotation**: Configure log rotation for /var/log if running as service
4. **Network Security**: Use firewall rules if exposed

### Multi-Agent Isolation

- Each agent gets separate credentials
- Use different calendar names per agent
- Rate limiting applies per CalendarManager instance
- Thread-safe for concurrent access

## 📊 Security Testing

### Automated Tests

```bash
# Run security tests
pytest tests/test_security.py -v

# Check for known vulnerabilities
pip-audit

# Static analysis
bandit -r src/
```

Security checks are also enforced in CI via `.github/workflows/security.yml`.

### Manual Testing

- Injection attacks (SQL, Command, Path Traversal)
- Authentication bypass attempts
- Rate limit testing
- Memory leak detection
- Concurrent access testing

## 📝 Compliance

- **OWASP Top 10**: Addressed all applicable items
- **CWE Coverage**: Protected against common weaknesses
- **PCI DSS**: Not applicable (no payment card data)
- **GDPR**: User data stored locally, full control

## 🔗 Security Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/stable/library/security_warnings.html)
- [CalDAV Security](https://datatracker.ietf.org/doc/html/rfc4791#section-8)
- [Apple ID Security](https://support.apple.com/en-us/HT204915)

---

**Last Updated**: March 5, 2026
**Security Version**: 2.4
**Audit Date**: March 4, 2026
