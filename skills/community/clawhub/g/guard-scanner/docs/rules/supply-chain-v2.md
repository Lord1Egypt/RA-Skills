# Threat Category: supply-chain-v2

This document provides explainability for all rules in the `supply-chain-v2` category.

## Rule: `SUPPLY_TYPOSQUAT_NPM`
- **Severity**: HIGH
- **Description**: Supply chain: NPM typosquatting of popular packages
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SUPPLY_STAR_VERSION`
- **Severity**: HIGH
- **Description**: Supply chain: wildcard/latest version in package.json (unpinned deps)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SUPPLY_POSTINSTALL_RCE`
- **Severity**: CRITICAL
- **Description**: Supply chain: lifecycle script with shell execution
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SUPPLY_GIT_DEPENDENCY`
- **Severity**: MEDIUM
- **Description**: Supply chain: git-based dependency (bypasses registry vetting)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SUPPLY_LOCKFILE_MISMATCH`
- **Severity**: LOW
- **Description**: Supply chain: lockfile integrity hash (verify not tampered)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SUPPLY_NODE_PRELOAD`
- **Severity**: HIGH
- **Description**: Supply chain: Node.js preload injection via --require flag
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SUPPLY_PIP_INDEX`
- **Severity**: HIGH
- **Description**: Supply chain: pip installing from non-standard index
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SUPPLY_CARGO_PATCH`
- **Severity**: MEDIUM
- **Description**: Supply chain: Cargo [patch] section pointing to non-official repo
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SUPPLY_EXTENSION_SIDELOAD`
- **Severity**: HIGH
- **Description**: Supply chain: IDE extension sideloading (VSIX/unpacked)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SUPPLY_HUGGINGFACE_PICKLE`
- **Severity**: CRITICAL
- **Description**: Supply chain: HuggingFace model loading with trust_remote_code or pickle deserialization
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `CLAWHAVOC_CRYPTO_THEFT`
- **Severity**: CRITICAL
- **Description**: ClawHavoc malware crypto key exfiltration
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

