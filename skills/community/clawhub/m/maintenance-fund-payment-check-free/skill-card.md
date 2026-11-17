## Description:

维修资金与专项工程付款核对（免费版）逐行复算维修资金与专项工程付款表，检查合计勾稽、重复行、空缺占位符和负数，并为每条结论引用原文依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, cashier, property-management, or owners-committee users run this skill during monthly settlement, reconciliation, and inventory checks to verify tabular maintenance-fund payment arithmetic. It helps identify table inconsistencies but does not decide legal eligibility, regulatory compliance, accounting approval, or valuation fairness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic findings as legal, regulatory, accounting, or approval decisions.

Mitigation: Use the findings only as table-level arithmetic and consistency checks; route legal, regulatory, accounting, eligibility, and approval decisions through the responsible reviewers.

Risk: The free release does not run the full set of maintenance-fund payment checks.

Mitigation: Review the reported checks_not_run list before relying on the result, especially for overpayment, negative balance, contract-ratio, and duplicate-project questions.

Risk: Incomplete or incorrectly structured input can prevent a reliable conclusion.

Mitigation: Provide the complete payment table with recognized headers and review missing-field guidance when the skill reports insufficient input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/maintenance-fund-payment-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Human-readable terminal text or structured JSON containing executed checks, findings, source-line references, omitted checks, and scope notes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on user-provided text or JSON input; insufficient input returns missing-field guidance instead of a pass/fail conclusion.]

## Skill Version(s):

1.0.55 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
