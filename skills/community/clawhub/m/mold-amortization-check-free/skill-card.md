## Description:

模具与工装摊销台账逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Cost accountants and finance managers use this skill before monthly costing and close to check mold and tooling amortization ledgers for arithmetic, totals, duplicate rows, missing required values, and negative amounts. The free edition reports only the included checks and cites source rows for findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive business and accounting ledger data.

Mitigation: Run it locally, avoid adding unnecessary confidential data to inputs, and control access to generated reports.

Risk: The output can influence financial review decisions but covers only the free edition's listed checks.

Mitigation: Review findings before relying on them and separately validate accounting-policy questions, capitalization, amortization method, useful life, residual value, ERP extraction, and other out-of-scope items.

Risk: Insufficient or malformed tables can prevent reliable conclusions.

Mitigation: Provide ledger text with recognized headers and required columns; treat missing-input responses as requests for more material, not as a clean audit result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/mold-amortization-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)
- [Sample input](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON ledger-check report from a local CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite input rows; insufficient input returns missing-field guidance instead of a clean result.]

## Skill Version(s):

1.0.53 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
