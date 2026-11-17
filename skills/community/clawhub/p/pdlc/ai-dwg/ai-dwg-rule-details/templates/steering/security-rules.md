<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: security-rules.md

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Security & Identity Architecture | date: {generation-date} -->

# Security Rules

## Security Model Summary
**Authentication:** {method}  |  **Authorization:** {model}  |  **Encryption:** {algorithm}
**Secrets:** {management approach}  |  **Audit:** {strategy}

## Authentication Rules
<!-- begin: AP-sourced -->
| Rule | Description |
|------|-------------|
| AUTH-01 | {token type and usage} |
| AUTH-02 | {token expiry} |
| ... | ... |
<!-- end: AP-sourced -->

## Authorization Rules
<!-- begin: AP-sourced -->
| Rule | Description |
|------|-------------|
| AUTHZ-01 | {authorization model} |
| AUTHZ-02 | {roles} |
| ... | ... |
<!-- end: AP-sourced -->

## Data Protection Rules
<!-- begin: AP-sourced -->
| Rule | Description |
|------|-------------|
| DATA-01 | {encryption at rest} |
| DATA-02 | {encryption in transit} |
| ... | ... |
<!-- end: AP-sourced -->

## Input Validation & API Security
<!-- begin: AP-sourced -->
| Rule | Description |
|------|-------------|
| SEC-01 | ALL input validated |
| SEC-02 | Parameterized queries only |
| ... | ... |
<!-- end: AP-sourced -->

## Audit & Logging
<!-- begin: AP-sourced -->
| Rule | Description |
|------|-------------|
| AUDIT-01 | Log ALL auth events |
| ... | ... |
<!-- end: AP-sourced -->

## Security Review Checklist
- [ ] No secrets in code
- [ ] Input validated
- [ ] Auth checked
- [ ] No sensitive data in logs
- [ ] Tenant scoping (if multi-tenant)
```

## Filling: Refer to `mapping/security-to-steering.md`.
