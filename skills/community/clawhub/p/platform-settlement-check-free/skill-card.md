## Description:

平台结算单逐项核对（逐行算术、合计勾稽、重复与空缺检测），每条结论引用原文行号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, and operations users use this skill during monthly settlement, reconciliation, or inventory-close workflows to check copied Chinese e-commerce platform settlement sheets for arithmetic consistency, total-row mismatches, duplicate order IDs, blanks, and placeholders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The free release omits advanced checks such as commission-rate range checks, negative settlement detection, refund-greater-than-sales detection, and zero-sales-with-fees detection.

Mitigation: Treat results as limited to the listed free checks and use manual review or a fuller workflow for omitted financial checks.

Risk: The checker expects copied settlement text with recognizable headers and does not read .xlsx files directly.

Mitigation: Export or copy the sheet with headers into text or JSON input, and follow the missing-material guidance when the skill reports insufficient input.

Risk: Settlement findings can affect financial decisions if accepted without review.

Mitigation: Review cited source lines and recalculate material findings before using them for payment, audit, tax, or platform-dispute decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/platform-settlement-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Console text or JSON objects containing check status, findings, summaries, executed checks, withheld checks, and out-of-scope checks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers when checks run; insufficient input produces missing-material guidance instead of a positive or negative conclusion.]

## Skill Version(s):

1.0.29 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
