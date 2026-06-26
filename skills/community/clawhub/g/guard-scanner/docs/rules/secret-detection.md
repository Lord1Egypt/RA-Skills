# Threat Category: secret-detection

This document provides explainability for all rules in the `secret-detection` category.

## Rule: `SECRET_HARDCODED_KEY`
- **Severity**: HIGH
- **Description**: Hardcoded API key/secret
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SECRET_PRIVATE_KEY`
- **Severity**: CRITICAL
- **Description**: Embedded private key
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SECRET_GITHUB_TOKEN`
- **Severity**: CRITICAL
- **Description**: GitHub token
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MOLTBOOK_SUPABASE_LEAK`
- **Severity**: CRITICAL
- **Description**: Supabase API Key (Moltbook 1.5M Leak pattern)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SECRET_ANTHROPIC_KEY_V2`
- **Severity**: CRITICAL
- **Description**: Anthropic API key v2 (sk-ant-api/msg/adm prefix)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

