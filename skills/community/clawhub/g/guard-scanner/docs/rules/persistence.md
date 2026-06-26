# Threat Category: persistence

This document provides explainability for all rules in the `persistence` category.

## Rule: `PERSIST_CRON`
- **Severity**: HIGH
- **Description**: Persistence: scheduled task creation
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PERSIST_STARTUP`
- **Severity**: HIGH
- **Description**: Persistence: startup execution
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PERSIST_LAUNCHD`
- **Severity**: HIGH
- **Description**: OS-level persistence mechanism
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PERSIST_CRONTAB_INJECT`
- **Severity**: HIGH
- **Description**: Persistence: crontab manipulation for scheduled execution
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PERSIST_LAUNCHD_PLIST`
- **Severity**: HIGH
- **Description**: Persistence: macOS LaunchAgent/Daemon installation
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PERSIST_REGISTRY_RUN`
- **Severity**: HIGH
- **Description**: Persistence: Windows registry Run key modification
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PERSIST_BASHRC_INJECT`
- **Severity**: HIGH
- **Description**: Persistence: shell profile injection (~/.bashrc, ~/.zshrc)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PERSIST_SSH_AUTHORIZED`
- **Severity**: CRITICAL
- **Description**: Persistence: SSH authorized_keys modification for backdoor access
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PERSIST_SYSTEMD_SERVICE`
- **Severity**: HIGH
- **Description**: Persistence: systemd service installation
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `EVASION_FILELESS`
- **Severity**: CRITICAL
- **Description**: Evasion: fileless execution via memory-backed file descriptors
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `EVASION_LOG_TAMPER`
- **Severity**: HIGH
- **Description**: Evasion: shell history clearing to hide activity
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `EVASION_TIMESTAMP_STOMP`
- **Severity**: HIGH
- **Description**: Evasion: file timestamp manipulation (timestomping)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `EVASION_PACKED_PAYLOAD`
- **Severity**: HIGH
- **Description**: Evasion: packed/protected binary to evade analysis
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

