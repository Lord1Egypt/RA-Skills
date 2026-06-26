# Threat Category: leaky-skills

This document provides explainability for all rules in the `leaky-skills` category.

## Rule: `LEAK_SAVE_KEY_MEMORY`
- **Severity**: CRITICAL
- **Description**: Leaky: save secret in agent memory
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `LEAK_SHARE_KEY`
- **Severity**: CRITICAL
- **Description**: Leaky: output secret to user
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `LEAK_VERBATIM_CURL`
- **Severity**: HIGH
- **Description**: Leaky: verbatim secret in commands
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `LEAK_COLLECT_PII`
- **Severity**: CRITICAL
- **Description**: Leaky: PII/financial data collection
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `LEAK_LOG_SECRET`
- **Severity**: HIGH
- **Description**: Leaky: session log export
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `LEAK_ENV_IN_PROMPT`
- **Severity**: HIGH
- **Description**: Leaky: .env contents through LLM context
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

