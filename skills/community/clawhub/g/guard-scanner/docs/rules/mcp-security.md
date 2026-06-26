# Threat Category: mcp-security

This document provides explainability for all rules in the `mcp-security` category.

## Rule: `MCP_TOOL_POISON`
- **Severity**: CRITICAL
- **Description**: MCP Tool Poisoning: hidden instruction
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MCP_SCHEMA_POISON`
- **Severity**: CRITICAL
- **Description**: MCP Schema Poisoning: malicious default
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MCP_TOKEN_LEAK`
- **Severity**: HIGH
- **Description**: MCP01: Token through tool parameters
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MCP_SHADOW_SERVER`
- **Severity**: HIGH
- **Description**: MCP09: Shadow server registration
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MCP_NO_AUTH`
- **Severity**: HIGH
- **Description**: MCP07: Disabled authentication
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MCP_SSRF_META`
- **Severity**: CRITICAL
- **Description**: Cloud metadata endpoint (SSRF)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `AUTO_REFINE_MCP_REBIND`
- **Severity**: CRITICAL
- **Description**: Shadow MCP Localhost Rebinding Attack
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MCP_BIND_ALL`
- **Severity**: HIGH
- **Description**: MCP server bound to all interfaces (0.0.0.0) — remote exploitation risk (36.7% of 7K+ servers)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MCP_SHADOW_NAME_COLLISION`
- **Severity**: HIGH
- **Description**: MCP Shadowing: naming collision with well-known MCP server (solo.io 2026-03)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MCP_OAUTH_CMD_INJECT`
- **Severity**: CRITICAL
- **Description**: MCP OAuth Command Injection: Unsanitized OAuth callback code passed to shell
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MCP_MPMA_PREFERENCE`
- **Severity**: HIGH
- **Description**: MCP MPMA: tool preference manipulation to bias agent tool selection
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MCP_TOOL_SQUATTING`
- **Severity**: CRITICAL
- **Description**: MCP Tool Squatting: registering tool with name of well-known built-in
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MCP_CONSENT_FATIGUE`
- **Severity**: HIGH
- **Description**: MCP Consent Fatigue: auto-approval bypasses human-in-the-loop safety
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MCP_CMD_INJECTION_CHAIN`
- **Severity**: CRITICAL
- **Description**: MCP command injection: tool invocation → shell execution chain (43% servers vulnerable)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MCP_RUG_PULL`
- **Severity**: CRITICAL
- **Description**: MCP Rug-Pull: deferred tool metadata mutation after initial inspection
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MCP_CREATEMESSAGE_HIJACK`
- **Severity**: CRITICAL
- **Description**: MCP Sampling Hijack: createMessage interface abuse to bypass human-in-the-loop controls
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MCP_8K_OPEN_SERVERS`
- **Severity**: HIGH
- **Description**: MCP exposed admin/debug endpoints: 8,000+ servers discovered with unauthenticated access
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `OPENCLAW_CVE_2026_25253`
- **Severity**: CRITICAL
- **Description**: OpenClaw CVE-2026-25253 One-Click Gateway Token Steal
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

