# Threat Category: a2a-contagion

This document provides explainability for all rules in the `a2a-contagion` category.

## Rule: `A2A_SMUGGLE`
- **Severity**: CRITICAL
- **Description**: A2A Contagion: Instruction injection between request-response cycles
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `A2A_TOOL_POISON`
- **Severity**: CRITICAL
- **Description**: A2A Contagion: MCP tool description containing hidden instructions
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `A2A_SESSION_SMUGGLING`
- **Severity**: CRITICAL
- **Description**: A2A Session Smuggling: hidden instructions embedded in agent-to-agent response payloads (Unit42)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `A2A_SESSION_PERSIST_SMUGGLE`
- **Severity**: CRITICAL
- **Description**: A2A session persistence smuggling: hidden instructions carried across agent session boundaries (Unit42)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `A2A_MESH_HANDOFF`
- **Severity**: CRITICAL
- **Description**: Agentic Mesh: hidden instructions injected during agent task handoff (2026 primary A2A vector)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `A2A_TRUSTED_ORIGIN_SPOOF`
- **Severity**: CRITICAL
- **Description**: A2A Trusted Origin Spoofing: forged agent headers elevating trust level
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `A2A_AGENT_CARD_POISON`
- **Severity**: HIGH
- **Description**: A2A agent card/skill description prompt injection poisoning
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `A2A_TASK_REPLAY`
- **Severity**: MEDIUM
- **Description**: A2A task replay attack — replaying completed tasks without re-authorization
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

