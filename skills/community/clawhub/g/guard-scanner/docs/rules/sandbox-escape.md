# Threat Category: sandbox-escape

This document provides explainability for all rules in the `sandbox-escape` category.

## Rule: `SANDBOX_PROC_MOUNT`
- **Severity**: CRITICAL
- **Description**: Sandbox escape: /proc/self access for container breakout
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SANDBOX_CHROOT_BREAK`
- **Severity**: CRITICAL
- **Description**: Sandbox escape: chroot/namespace manipulation
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SANDBOX_DOCKER_SOCK`
- **Severity**: CRITICAL
- **Description**: Sandbox escape: Docker socket access or privileged exec
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SANDBOX_SYMLINK_RACE`
- **Severity**: HIGH
- **Description**: Sandbox escape: symlink race condition to access restricted paths
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SANDBOX_PTRACE`
- **Severity**: CRITICAL
- **Description**: Sandbox escape: ptrace-based process injection
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SANDBOX_RLIMIT_BYPASS`
- **Severity**: HIGH
- **Description**: Sandbox escape: resource limit bypass
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SANDBOX_MOUNT_NS`
- **Severity**: CRITICAL
- **Description**: Sandbox escape: filesystem mount in restricted namespace
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SANDBOX_DBUS_ESCAPE`
- **Severity**: HIGH
- **Description**: Sandbox escape: D-Bus IPC exploitation (Flatpak/Snap)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SANDBOX_SECCOMP_BYPASS`
- **Severity**: CRITICAL
- **Description**: Sandbox escape: seccomp filter manipulation
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SANDBOX_CGROUP_ESCAPE`
- **Severity**: CRITICAL
- **Description**: Sandbox escape: cgroup breakout via release_agent (CVE-2022-0492 variant)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SANDBOX_K8S_SA_TOKEN`
- **Severity**: CRITICAL
- **Description**: Sandbox escape: Kubernetes service account token theft
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SANDBOX_WASM_ESCAPE`
- **Severity**: HIGH
- **Description**: WASM sandbox escape: WASI filesystem escape via mapped directories
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

