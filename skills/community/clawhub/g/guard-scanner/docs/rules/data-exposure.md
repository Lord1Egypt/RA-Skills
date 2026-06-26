# Threat Category: data-exposure

This document provides explainability for all rules in the `data-exposure` category.

## Rule: `AUTO_REFINE_MOLTBOOK_LEAK`
- **Severity**: CRITICAL
- **Description**: Moltbook-style API Key Leak Detection
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MOLTBOOK_API_KEY_LEAK`
- **Severity**: CRITICAL
- **Description**: Moltbook API Extractor payload targeting Supabase keys
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `DATA_VERBOSE_ERROR`
- **Severity**: MEDIUM
- **Description**: Data exposure: verbose error/stack trace in HTTP response
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `DATA_DEBUG_ENDPOINT`
- **Severity**: HIGH
- **Description**: Data exposure: debug/admin endpoint exposed in production
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `DATA_DIRECTORY_LISTING`
- **Severity**: MEDIUM
- **Description**: Data exposure: directory listing enabled in static file server
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `DATA_CORS_CREDENTIALS`
- **Severity**: CRITICAL
- **Description**: Data exposure: CORS with credentials + wildcard origin
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `DATA_LOG_SENSITIVE`
- **Severity**: HIGH
- **Description**: Data exposure: logging sensitive data (passwords, tokens, keys)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `DATA_HEADER_LEAK`
- **Severity**: LOW
- **Description**: Data exposure: server technology disclosure via HTTP headers
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `DATA_GIT_EXPOSED`
- **Severity**: CRITICAL
- **Description**: Data exposure: .git directory or .env file accessible
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `DATA_BACKUP_FILE`
- **Severity**: MEDIUM
- **Description**: Data exposure: backup/temporary files left in accessible location
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

