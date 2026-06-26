# FDA Cybersecurity Guidance Summary

## Key FDA Documents

- **Cybersecurity in Medical Devices: Quality System Considerations and Content Premarket Submissions** (June 2023)
- **Postmarket Management of Cybersecurity in Medical Devices** (December 2016)
- **Software as a Medical Device (SaMD): Cybersecurity** (January 2016)

## Core Cybersecurity Principles

### 1. Secure Design

- **Defense in Depth**: Multiple layers of security
- **Least Privilege**: Minimal permissions required
- **Secure Defaults**: Out-of-box secure configuration
- **Fail Secure**: Safe failure modes

### 2. Threat Modeling

Required for all device classes:
- Identify assets (PHI, device functionality)
- Identify threats (attack vectors)
- Assess vulnerabilities
- Define mitigations

### 3. Security Controls

| Control Type | Examples |
|--------------|----------|
| Authentication | Multi-factor, password policies |
| Authorization | Role-based access control |
| Encryption | TLS 1.2+, AES-256 |
| Logging | Audit trails, tamper detection |
| Updates | Signed firmware, secure boot |

## Pre-Market Requirements

### Design Documentation

1. **Cybersecurity Management Plan**
   - Security team responsibilities
   - Vulnerability disclosure process
   - Update/patch management

2. **Threat Model**
   - Diagram showing attack surfaces
   - Threat agents and attack paths
   - Risk assessment matrix

3. **Cybersecurity Specifications**
   - Security requirements derived from threat model
   - Security architecture design

4. **Verification/Testing**
   - Security testing results
   - Vulnerability scanning
   - Penetration testing (for higher risk)

### Security Architecture

Must document:
- All network interfaces
- Data encryption (at rest, in transit)
- Authentication mechanisms
- Authorization/Access control
- Logging and monitoring capabilities
- Update mechanism security

## Post-Market Requirements

### Vulnerability Management

1. **Monitoring**
   - Monitor CVE databases
   - Monitor security researcher reports
   - Internal security testing

2. **Assessment**
   - Evaluate discovered vulnerabilities
   - Assess risk to device/users
   - Classify severity

3. **Mitigation**
   - Develop patches/updates
   - Workarounds for unpatchable issues

4. **Disclosure**
   - Public vulnerability disclosure
   - FDA notification (for critical)
   - Customer communication

### Reporting Timelines

| Vulnerability Type | FDA Notification |
|-------------------|------------------|
| Uncontrolled risk to patients | Within 30 days |
| Significant safety issue | Immediately |
| Routine vulnerabilities | In periodic reports |

## Common Cybersecurity Vulnerabilities

### Top Issues in Medical Devices

1. **Weak/Default Credentials**
   - Hardcoded passwords
   - Default credentials not changed

2. **Unencrypted Communications**
   - Telnet, unencrypted HTTP
   - Cleartext protocols

3. **Missing Authentication**
   - No authentication on interfaces
   - Bypassed auth in maintenance modes

4. **Injection Flaws**
   - SQL injection
   - Command injection
   - Buffer overflows

5. **Outdated Components**
   - Known CVEs in libraries
   - Unpatched OS components

6. **Insecure Update Mechanisms**
   - Unauthenticated updates
   - Unverified firmware

7. **Excessive Permissions**
   - Unnecessary services enabled
   - Overly permissive access

## Secure Coding Guidelines

Follow:
- **OWASP Top 10**
- **CWE (Common Weakness Enumeration)**
- **CERT C/C++ Secure Coding**
- **NIST SP 800-53**

## References

- FDA Cybersafety: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cybersecurity-medical-devices-quality-system-considerations-and-content-premarket
- MITRE CVE Database: https://cve.mitre.org/
- ICS-CERT: https://www.cisa.gov/news-events/cybersecurity-advisories
