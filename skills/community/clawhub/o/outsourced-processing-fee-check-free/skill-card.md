## Description:

委外加工费与损耗核对（免费版）会对委外加工结算核对表执行逐行复算、合计勾稽、重复与空缺检测，并在结论中引用原文依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, and manufacturing reconciliation users can use this skill during month-end close, account reconciliation, or inventory review to check outsourced-processing settlement tables for arithmetic mismatches, total-line inconsistencies, duplicate rows, blanks, and negative values. It is a local arithmetic reconciliation aid, not financial, contract, or legal advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic reconciliation output as financial, contract, or legal advice.

Mitigation: Use the output as a local checking aid and have responsible finance, contract, or legal reviewers confirm any business decision.

Risk: The free tier omits checks such as loss-rate-over-limit, contract-price mismatch, and stock-count mismatch review.

Mitigation: Confirm whether the omitted checks are required for the workflow before relying on the free-tier result.

Risk: Incomplete or unrecognizable input can prevent the skill from reaching a conclusion.

Mitigation: Provide the outsourced-processing settlement table with headers and source rows; treat missing-input guidance as a request for more material, not as a clean result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/outsourced-processing-fee-check-free)
- [Publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text or JSON reconciliation report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source material when sufficient input is provided; insufficient input returns missing-material guidance rather than a conclusion.]

## Skill Version(s):

1.0.56 (source: server release evidence, SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
