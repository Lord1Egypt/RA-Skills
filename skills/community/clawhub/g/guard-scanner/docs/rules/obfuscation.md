# Threat Category: obfuscation

This document provides explainability for all rules in the `obfuscation` category.

## Rule: `OBF_HEX`
- **Severity**: HIGH
- **Description**: Hex-encoded string (5+ bytes)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `OBF_BASE64_EXEC`
- **Severity**: CRITICAL
- **Description**: Base64 decode → execute chain
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `OBF_BASE64`
- **Severity**: MEDIUM
- **Description**: Base64 decoding
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `OBF_CHARCODE`
- **Severity**: HIGH
- **Description**: Character code construction (4+ chars)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `OBF_CONCAT`
- **Severity**: MEDIUM
- **Description**: Array join obfuscation
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `OBF_BASE64_BASH`
- **Severity**: CRITICAL
- **Description**: Base64 decode piped to shell
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `LLM_SCANNER_EVASION`
- **Severity**: HIGH
- **Description**: LLM scanner evasion: adversarial comment claiming code is safe
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

