## Description:

备用金与报销核销表逐项核对，执行逐行复算、合计勾稽、重复与空缺检测，并为每条结论引用原文依据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and cashier teams use this skill during month-end close, reconciliation, stocktake, handoff, and internal-control review to check petty-cash and reimbursement write-off tables. It helps identify arithmetic mismatches, total-row issues, duplicate rows, blanks, placeholders, and negative amounts in provided table text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker does not replace accounting policy, compliance review, or verification of supporting vouchers.

Mitigation: Use it as a deterministic table check and have finance or compliance reviewers confirm policy, approval, voucher, and tax questions.

Risk: The free version intentionally omits some checks, including negative closing balance, over-write-off, aging, multiple uncleared balances, and zero-claim write-off checks.

Mitigation: Review the listed checks not run before relying on a clean result, and perform omitted checks separately when they matter.

Risk: Insufficient or malformed table text can prevent the skill from producing a conclusion.

Mitigation: Provide exported table text with the required headers and treat missing-input responses as a request for more material, not as a clean finding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/petty-cash-check-free)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Plain text or JSON report with cited findings, missing-input status, executed checks, and checks not run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with the bundled Node.js checker; no network use is described in the security evidence.]

## Skill Version(s):

1.0.57 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
