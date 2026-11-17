## Description:

物流仓储与操作费结算表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and supply-chain reconciliation staff use this skill before payment to check third-party warehouse storage and handling fee settlement tables for arithmetic mismatches, duplicate rows, missing placeholders, and negative amounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The output could be mistaken for legal, contract, tax, or payment approval advice.

Mitigation: Use the findings as arithmetic reconciliation support and keep final approval with the responsible finance, tax, contract, or payment reviewer.

Risk: The free version runs only the declared free checks and omits additional checks listed by the artifact.

Mitigation: Review the reported skipped checks before relying on the result, especially for contract-rate, policy, tax, invoice, or payment-term decisions.

Risk: Insufficient or malformed settlement-table input can prevent a reliable conclusion.

Mitigation: Provide only the settlement-table text or JSON needed for checking, including headers and required columns, and treat missing-input responses as no conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/logistics-storage-fee-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON reconciliation findings with source-line references, executed checks, skipped checks, and summary counts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided settlement-table text or JSON; materials that are insufficient produce a missing-input response instead of a conclusion.]

## Skill Version(s):

1.0.58 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
