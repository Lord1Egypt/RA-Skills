# Threat Category: agent-protocol

This document provides explainability for all rules in the `agent-protocol` category.

## Rule: `PROTO_A2A_IMPERSONATE`
- **Severity**: CRITICAL
- **Description**: A2A protocol: agent card identity spoofing
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PROTO_A2A_TASK_FLOOD`
- **Severity**: HIGH
- **Description**: A2A protocol: task flooding DoS attack
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PROTO_MCP_TOOL_REDEFINE`
- **Severity**: CRITICAL
- **Description**: MCP protocol: tool definition mutation after initial registration
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PROTO_MCP_RESOURCE_POISON`
- **Severity**: CRITICAL
- **Description**: MCP protocol: resource poisoning via tampered content
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PROTO_MCP_PROMPT_INJECT`
- **Severity**: CRITICAL
- **Description**: MCP protocol: prompt template injection
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PROTO_OAUTH_REDIRECT`
- **Severity**: CRITICAL
- **Description**: OAuth redirect hijack: unsafe URI scheme in redirect
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PROTO_SSE_HIJACK`
- **Severity**: HIGH
- **Description**: SSE transport hijack: MCP server-sent event interception
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PROTO_STDIO_INJECT`
- **Severity**: HIGH
- **Description**: STDIO transport injection: raw protocol message injection via stdin
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PROTO_CAPABILITY_ESCALATE`
- **Severity**: CRITICAL
- **Description**: Agent protocol: capability escalation beyond granted scope
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PROTO_CONTEXT_OVERFLOW`
- **Severity**: HIGH
- **Description**: Context window overflow: deliberate token budget exhaustion attack
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PROTO_NESTED_AGENT_CALL`
- **Severity**: HIGH
- **Description**: Nested agent call: recursive agent invocation chain (confused deputy)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PROTO_TOOL_PARAM_OVERFLOW`
- **Severity**: HIGH
- **Description**: Tool parameter overflow: oversized input to crash or bypass validation
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `AGENT_PROTOCOL_ABUSE`
- **Severity**: HIGH
- **Description**: Agent Protocol: Suspicious context triggering agent protocol abuse
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

