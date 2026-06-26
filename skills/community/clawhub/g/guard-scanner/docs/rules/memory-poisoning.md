# Threat Category: memory-poisoning

This document provides explainability for all rules in the `memory-poisoning` category.

## Rule: `MEMPOIS_WRITE_SOUL`
- **Severity**: CRITICAL
- **Description**: Memory poisoning: SOUL/IDENTITY file modification
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MEMPOIS_WRITE_MEMORY`
- **Severity**: HIGH
- **Description**: Memory poisoning: agent memory modification
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MEMPOIS_CHANGE_RULES`
- **Severity**: CRITICAL
- **Description**: Memory poisoning: behavioral rule override
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MEMPOIS_PERSIST`
- **Severity**: HIGH
- **Description**: Memory poisoning: persistence instruction
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MEMPOIS_CODE_WRITE`
- **Severity**: HIGH
- **Description**: Memory poisoning: file write to user home
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `ASI06_MEMORY_POISONING`
- **Severity**: CRITICAL
- **Description**: ASI06: RAG/Vector DB persistent fake knowledge injection
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `CONTEXTCRUSH_DOC_POISON`
- **Severity**: CRITICAL
- **Description**: ContextCrush: planted documentation with hidden instructions for RAG/retrieval poisoning (5-in-1M ASR)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MEM_MINJA_QUERY_POISON`
- **Severity**: CRITICAL
- **Description**: MINJA: query-only memory poisoning via retrieval injection (95%+ ISR, arXiv:2503.03704)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MEM_RAG_DECEPTIVE_REASON`
- **Severity**: CRITICAL
- **Description**: RAG deceptive reasoning: poisoned retrieval documents with semantic chains that override agent reasoning
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MEM_MICROSOFT_BIAS`
- **Severity**: HIGH
- **Description**: Memory bias injection: planted entries to bias AI assistant recommendations (Microsoft 2026)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

