# Threat Category: prompt-injection

This document provides explainability for all rules in the `prompt-injection` category.

## Rule: `PI_IGNORE`
- **Severity**: CRITICAL
- **Description**: Prompt injection: ignore instructions
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PI_ROLE`
- **Severity**: CRITICAL
- **Description**: Prompt injection: role override
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PI_SYSTEM`
- **Severity**: CRITICAL
- **Description**: Prompt injection: system message impersonation
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PI_ZWSP`
- **Severity**: CRITICAL
- **Description**: Zero-width Unicode (hidden text)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PI_BIDI`
- **Severity**: CRITICAL
- **Description**: Unicode BiDi control character (text direction attack)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PI_INVISIBLE`
- **Severity**: HIGH
- **Description**: Invisible/formatting Unicode character
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PI_HOMOGLYPH`
- **Severity**: HIGH
- **Description**: Cyrillic/Latin homoglyph mixing
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PI_HOMOGLYPH_GREEK`
- **Severity**: HIGH
- **Description**: Greek/Latin homoglyph mixing
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PI_HOMOGLYPH_MATH`
- **Severity**: HIGH
- **Description**: Mathematical symbol homoglyphs (𝐀-𝟿)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PI_TAG_INJECTION`
- **Severity**: CRITICAL
- **Description**: XML/tag-based prompt injection
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PI_BASE64_MD`
- **Severity**: CRITICAL
- **Description**: Base64 execution instruction in docs
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MOLTBOOK_REVERSE_PI`
- **Severity**: CRITICAL
- **Description**: Moltbook Reverse Prompt Injection
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `AUTO_REFINE_A2A_IDPI`
- **Severity**: CRITICAL
- **Description**: A2A Contagion Indirect Prompt Injection (IDPI)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `A2A_SEMANTIC_CONTAGION`
- **Severity**: CRITICAL
- **Description**: A2A Semantic Contagion passing downstream payload overrides
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PI_TOKEN_SPLIT`
- **Severity**: HIGH
- **Description**: Token-splitting PI: fragmented "ignore" across delimiters
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `PI_FULLWIDTH_EVASION`
- **Severity**: HIGH
- **Description**: Fullwidth Latin evasion (NFKC bypass)
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `MOLTBOOK_INDIRECT_PI`
- **Severity**: CRITICAL
- **Description**: Moltbook Bot-to-Bot payload: hidden system instruction
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

## Rule: `SNYK_AGENT_GUARD_EVASION`
- **Severity**: CRITICAL
- **Description**: Snyk Agent Guard evasion using Cyrillic/Homoglyphs
- **Rationale**: Explains why this pattern is considered dangerous.
- **Exploit Precondition**: What an attacker needs to trigger this.
- **Likely False Positives**: Scenarios where this might trigger safely.
- **Remediation Hint**: How to fix or mitigate the finding.

