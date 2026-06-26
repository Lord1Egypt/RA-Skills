# Threat Category: unverifiable-deps

This document provides explainability for all rules in the `unverifiable-deps` category.

## Rule: `DEP_REMOTE_IMPORT`
- **Severity**: HIGH
- **Description**: Remote dynamic import
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `DEP_REMOTE_SCRIPT`
- **Severity**: MEDIUM
- **Description**: Remote script loading
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `DEPS_PHANTOM_IMPORT`
- **Severity**: LOW
- **Description**: Dependency: unscoped package import (verify existence)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `DEPS_HTTP_IMPORT`
- **Severity**: CRITICAL
- **Description**: Dependency: HTTP URL import (unverifiable, MITM risk)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `DEPS_DYNAMIC_REQUIRE`
- **Severity**: HIGH
- **Description**: Dependency: dynamic require with non-literal module spec
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `DEPS_CDN_UNPINNED`
- **Severity**: HIGH
- **Description**: Dependency: CDN import without pinned version
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `DEPS_WASM_UNSIGNED`
- **Severity**: HIGH
- **Description**: Dependency: unsigned WASM module loading
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `DEPS_SUBRESOURCE_NOINT`
- **Severity**: MEDIUM
- **Description**: Dependency: external script without subresource integrity
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `DEPS_GO_REPLACE`
- **Severity**: MEDIUM
- **Description**: Dependency: Go module replace directive to non-standard path
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `DEPS_AUTO_UPDATE`
- **Severity**: HIGH
- **Description**: Dependency: auto-merge policy for dependency updates (supply chain risk)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

