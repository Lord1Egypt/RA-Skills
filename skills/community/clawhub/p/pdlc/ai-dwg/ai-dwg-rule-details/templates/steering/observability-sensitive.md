<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: observability-sensitive.md

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Security Architecture + Observability | date: {generation-date} -->

# Observability — Sensitive Data Rules

## NEVER Log
<!-- begin: AP-sourced -->
| Category | Items | Why |
|----------|-------|-----|
| Credentials | Passwords, hashes, API keys, tokens, private keys | Credential exposure |
| Secrets | Encryption keys, connection strings with creds | Secret leakage |
| PII | {project-specific: SSN, card numbers, etc.} | Compliance |
| Session | Full tokens, cookie values | Session hijack |
| Internal | Full paths, internal IPs | Reconnaissance |
<!-- end: AP-sourced -->

## Masking Patterns
<!-- begin: AP-sourced -->
| Data Type | Pattern | Example |
|-----------|---------|---------|
| Email | domain only | `***@example.com` |
| Phone | last 4 | `***-***-1234` |
| Token | first/last 4 | `eyJh...xyz9` |
| API Key | prefix only | `sk_live_***` |
| Card | last 4 | `****-4242` |

| Rule | Standard |
|------|----------|
| SENS-01 | Mask at log time — never store unmasked |
| SENS-02 | Error responses: never include sensitive data |
| SENS-03 | Stack traces: never in production responses |
<!-- end: AP-sourced -->

## Safe to Log
| Data | Reason |
|------|--------|
| User ID (UUID) | Opaque identifier |
| Tenant ID | Required for debugging |
| Entity IDs | Operation tracking |
| Timestamps | Operational |
| Status codes | No sensitive content |
| Duration | Performance metric |

## Enforcement
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| SENS-06 | Review every log statement with user data |
| SENS-07 | Automated scanning for sensitive patterns |
| SENS-08 | Tests verify sensitive fields absent from logs |
| SENS-09 | If found in logs: security incident → purge |
<!-- end: AP-sourced -->
```

## Filling: Refer to `mapping/infra-to-observability.md` (Target 2).
