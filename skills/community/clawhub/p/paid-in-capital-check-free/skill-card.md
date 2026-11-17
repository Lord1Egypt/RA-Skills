## Description:

股东出资明细表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。触发词包括 实收资本与股东出资核对、股东出资明细表对不上。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Company finance, corporate secretarial, and securities affairs teams use this skill before audits, annual filings, capital increases, share restructurings, or equity transfers to check whether shareholder contribution tables are internally consistent. It performs local checks for paid-in capital, subscribed capital, unpaid contribution, ownership percentage, duplicate shareholder rows, blank placeholders, and total-row reconciliation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake table self-consistency checks for legal, audit, tax, bank-record, or corporate-registry verification.

Mitigation: Use the skill as a local preliminary table check only; verify legal, audit, tax, banking, and registry matters against authoritative records and qualified reviewers.

Risk: The free release omits documented checks and can miss issues outside the implemented free scope.

Mitigation: Review the listed withheld checks before relying on results, and perform separate review for bank-entry mismatches, negative unpaid amounts, ownership-total errors, controlling-shareholder prompts, and zero-paid shareholder prompts.

Risk: Missing or unrecognized table columns lead to insufficient input rather than a substantive conclusion.

Mitigation: Provide a shareholder contribution table with the required headers for subscribed amount, cumulative paid amount, current paid amount, unpaid amount, ownership ratio, bank entry amount, paid-in capital, and capital reserve.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/paid-in-capital-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Human-readable console text or JSON findings with cited source-table evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; the free release reports only the implemented free checks and lists withheld checks instead of inferring them.]

## Skill Version(s):

1.0.17 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
