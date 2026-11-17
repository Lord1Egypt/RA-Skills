# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in the AI-* Family packages, please report it responsibly.

**Do NOT open a public GitHub issue for security vulnerabilities.**

### How to Report

Send an email to: **[mohammad.maheri.work@gmail.com](mailto:mohammad.maheri.work@gmail.com)**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if you have one)

### What to Expect

- **Acknowledgment:** Within 72 hours of your report
- **Assessment:** We will evaluate severity and impact within 7 days
- **Resolution:** Critical issues will be prioritized for the next patch release
- **Credit:** Reporters will be credited in the release notes (unless you prefer anonymity)

### Scope

This policy covers:
- Security issues in the workflow logic (e.g., instructions that could lead to insecure code generation)
- Credential or secret exposure in package files
- Vulnerabilities in generated workspace configurations (hooks, steering files)
- Supply chain concerns (tampered package content)

This policy does NOT cover:
- Issues in AI model behavior (report those to the AI platform provider)
- Issues in user-generated content produced by running the packages
- Issues in third-party dependencies (AI-DLC v1, IDE extensions)

### Severity Levels

| Level | Definition | Response Time |
|-------|-----------|:-------------:|
| Critical | Credential exposure, code injection via generated files | 24 hours |
| High | Insecure defaults in generated configurations | 72 hours |
| Medium | Information disclosure, overly permissive file patterns | 7 days |
| Low | Documentation errors that could mislead security decisions | 14 days |

---

## Supported Versions

| Version | Supported |
|---------|:---------:|
| 0.1.x (Beta 1) | ✅ |
| Pre-release / Alpha | ❌ |

---

## Security Design Principles

The AI-* Family packages follow these security principles:

1. **No secrets in packages.** Packages contain only process logic — never credentials, tokens, or environment-specific values.
2. **Prescriptive security guidance.** AI-GCE generates security-specific steering files and hooks derived from the architecture's security decisions.
3. **Least privilege in hooks.** Generated hooks use the narrowest file patterns possible — never `*.*`.
4. **Non-destructive operations.** No package auto-applies changes. All modifications require user approval at gates.
5. **Audit trail.** AI-GCE's compliance log provides a JSONL record of every governance action.

---

**Copyright:** © 2026 Mohammad Maheri
