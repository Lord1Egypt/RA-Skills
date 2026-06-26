# Threat Category: model-poisoning

This document provides explainability for all rules in the `model-poisoning` category.

## Rule: `MODEL_WEIGHT_BACKDOOR`
- **Severity**: CRITICAL
- **Description**: Model poisoning: backdoor embedded in model weights
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MODEL_GRADIENT_LEAK`
- **Severity**: CRITICAL
- **Description**: Model poisoning: gradient-based data exfiltration during training
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MODEL_DATASET_POISON`
- **Severity**: CRITICAL
- **Description**: Model poisoning: training dataset contamination
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MODEL_RLHF_EXPLOIT`
- **Severity**: CRITICAL
- **Description**: RLHF exploitation: reward model gaming to bypass safety alignment
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MODEL_QUANTIZE_DEGRADE`
- **Severity**: HIGH
- **Description**: Quantization degradation: safety guardrails weakened through aggressive quantization
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

