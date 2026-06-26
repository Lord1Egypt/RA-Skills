# Threat Category: inference-manipulation

This document provides explainability for all rules in the `inference-manipulation` category.

## Rule: `INFER_LOGIT_BIAS`
- **Severity**: HIGH
- **Description**: Inference manipulation: extreme logit_bias forcing specific token output
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `INFER_TEMP_ZERO_EXPLOIT`
- **Severity**: MEDIUM
- **Description**: Inference manipulation: temperature=0 exploitation for deterministic extraction
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `INFER_STOP_SEQ_BYPASS`
- **Severity**: HIGH
- **Description**: Inference manipulation: stop sequence bypass attempt
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `INFER_SYSTEM_EXTRACT`
- **Severity**: CRITICAL
- **Description**: Inference: system prompt extraction via verbatim reproduction request
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `INFER_JAILBREAK_DAN`
- **Severity**: CRITICAL
- **Description**: Inference: DAN/jailbreak role-play to bypass content filters
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `INFER_MULTI_TURN_ESCAPE`
- **Severity**: HIGH
- **Description**: Inference: multi-turn jailbreak escalation (crescendo attack)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `INFER_FUNCTION_ABUSE`
- **Severity**: CRITICAL
- **Description**: Inference: function call response injection to hijack tool outputs
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

