## Description:

租金账单/租赁结算表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文行号。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Businesses that lease venues, shops, or similar spaces use this skill to check rent bills and lease settlement worksheets for arithmetic consistency, rolled-over arrears, duplicate tenants, blanks, and column totals. It is intended for local review of worksheet text and does not provide legal, tax, or contract advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial worksheet findings may be incomplete if users treat the free version as a full audit.

Mitigation: Review results manually and note that the free version omits several checks, including non-positive rent, negative ending arrears, out-of-range month counts, and negative receipts.

Risk: Users may overread arithmetic checks as legal, tax, contract, or deposit-settlement advice.

Mitigation: Use the skill only for the disclosed rent worksheet arithmetic checks and route legal, tax, contract, and deposit questions to qualified reviewers.

Risk: Insufficient or malformed worksheet input could lead to unsupported conclusions if defaults were assumed.

Mitigation: The skill reports missing input and avoids conclusions when required worksheet fields cannot be recognized; users should supply the table header and relevant rows before relying on output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/lease-rent-check-free)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Human-readable text or JSON containing findings, summaries, executed checks, withheld checks, and missing-input guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers; insufficient input produces missing-field guidance instead of a conclusion.]

## Skill Version(s):

1.0.32 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
