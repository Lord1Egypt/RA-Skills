# OWASP Medical Device Security Checklist

## OWASP Top 10 Medical Device Risks (2023)

| Rank | Risk | Description |
|------|------|-------------|
| 1 | Unsafe or Outdated Components | Known CVEs, unpatched OS/libraries |
| 2 | Insufficient Authentication/Authorization | Weak auth, privilege escalation |
| 3 | Insecure Network Services | Exposed services, lack of encryption |
| 4 | Lack of Confidentiality/Integrity | Unencrypted PHI, unsigned code |
| 5 | Insufficient Logging | No audit trails, missed events |
| 6 | Unsafe or Insecure Update | Unauthenticated, unverified updates |
| 7 | Physical Security | USB ports, accessible hardware |
| 8 | Insufficient Data Protection | PHI at rest, weak encryption |
| 9 | Insufficient Hardening | Debug modes, unnecessary services |
| 10 | Insecure Configuration | Default credentials, open settings |

## Pre-Development Checklist

- [ ] Threat model completed
- [ ] Security requirements defined
- [ ] Secure coding standards adopted
- [ ] Security testing tools configured
- [ ] SBOM (Software Bill of Materials) plan in place

## Design Review Checklist

### Authentication & Authorization
- [ ] Multi-factor authentication for clinical functions
- [ ] Role-based access control (RBAC) implemented
- [ ] Default credentials removed/disabled
- [ ] Session timeout enforced
- [ ] Password policy enforced (length, complexity, expiration)

### Network Security
- [ ] All communications encrypted (TLS 1.2+)
- [ ] Certificate validation implemented
- [ ] No cleartext protocols (HTTP, Telnet, FTP)
- [ ] Firewalls restrict access to necessary ports only
- [ ] Network segmentation in place

### Data Protection
- [ ] PHI encrypted at rest (AES-256)
- [ ] PHI encrypted in transit
- [ ] Integrity checks on critical data
- [ ] Secure key storage (not hardcoded)
- [ ] Data minimization implemented

### Device Hardening
- [ ] Unnecessary services disabled
- [ ] Debug modes disabled in production
- [ ] Secure boot implemented
- [ ] Code signing required for updates
- [ ] JTAG/debug ports disabled

### Logging & Monitoring
- [ ] Audit logging for all security events
- [ ] Logs include timestamps and user identification
- [ ] Log integrity protection (tamper-evident)
- [ ] Centralized log collection
- [ ] Alerting for security events

## Code Review Checklist

### Input Validation
- [ ] All external input validated
- [ ] Bounds checking on arrays/buffers
- [ ] Input sanitization (no SQL/command injection)
- [ ] Type checking on all parameters

### Memory Safety (C/C++)
- [ ] No buffer overflows
- [ ] No use of unsafe string functions (strcpy, sprintf)
- [ ] Proper allocation/deallocation
- [ ] Integer overflow checks
- [ ] Null pointer checks

### Concurrency
- [ ] Thread-safe access to shared resources
- [ ] Proper mutex/lock usage
- [ ] No race conditions
- [ ] Deadlock prevention (lock ordering)
- [ ] Thread pool limits

### Error Handling
- [ ] All exceptions caught
- [ ] Errors logged appropriately
- [ ] Fail-safe defaults
- [ ] No information leakage in error messages
- [ ] Graceful degradation

### Cryptography
- [ ] Approved algorithms (AES, RSA-2048+, SHA-256+)
- [ ] Secure random number generation
- [ ] Keys not hardcoded
- [ ] Proper IV usage
- [ ] No custom cryptography

## Testing Checklist

### Static Analysis
- [ ] SAST tool run (Coverity, Checkmarx, SonarQube)
- [ ] Critical findings addressed
- [ ] C/C++ specific checks (CERT, MISRA)

### Dynamic Analysis
- [ ] DAST scan performed
- [ ] Fuzz testing on inputs
- [ ] API security testing

### Penetration Testing
- [ ] External network testing
- [ ] Physical access testing
- [ ] Social engineering testing (if applicable)

### Vulnerability Scanning
- [ ] CVE scanning on dependencies
- [ ] NVD/CVE database monitoring
- [ ] Regular vulnerability assessments

## Deployment Checklist

### Installation
- [ ] Default passwords changed
- [ ] Secure configuration applied
- [ ] Network ports verified
- [ ] Update verification enabled

### Documentation
- [ ] Security admin guide updated
- [ ] User documentation on security features
- [ ] Incident response contacts documented

### Ongoing
- [ ] Monitoring/alerting configured
- [ ] Update mechanism tested
- [ ] Backup/restore tested
- [ ] Decommissioning process defined

## Remediation Priority

| Priority | Criteria | Response Time |
|----------|----------|---------------|
| Critical | Active exploitation, patient safety | < 48 hours |
| High | PoC exploit, high impact | < 7 days |
| Medium | Exploitable with conditions | < 30 days |
| Low | Theoretical, low impact | Next release |

## References

- OWASP Medical Device Top 10: https://owasp.org/www-project-medical-device-top-10/
- OWASP SAMM: https://owasp.org/www-project-samm/
- NIST Cybersecurity Framework: https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final
