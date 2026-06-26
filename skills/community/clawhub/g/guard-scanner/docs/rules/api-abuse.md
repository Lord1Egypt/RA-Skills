# Threat Category: api-abuse

This document provides explainability for all rules in the `api-abuse` category.

## Rule: `API_KEY_HARDCODE`
- **Severity**: HIGH
- **Description**: API abuse: hardcoded API key in source code
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `API_RATE_BYPASS`
- **Severity**: HIGH
- **Description**: API abuse: rate limiting bypass technique
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `API_WEBHOOK_EXFIL`
- **Severity**: HIGH
- **Description**: API abuse: webhook to untrusted endpoint (data exfiltration)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `API_GRAPHQL_INTROSPECT`
- **Severity**: MEDIUM
- **Description**: API abuse: GraphQL introspection query (schema discovery)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `API_JWT_NONE_ALG`
- **Severity**: CRITICAL
- **Description**: API abuse: JWT "none" algorithm attack
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `API_SSRF_INTERNAL`
- **Severity**: CRITICAL
- **Description**: API abuse: SSRF to internal network endpoints
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `API_CORS_WILDCARD`
- **Severity**: MEDIUM
- **Description**: API abuse: CORS wildcard allowing any origin
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `API_OPEN_REDIRECT`
- **Severity**: HIGH
- **Description**: API abuse: open redirect from user-controlled input
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

