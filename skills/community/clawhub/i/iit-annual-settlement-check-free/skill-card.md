## Description:

个税年度汇算表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。触发词包括 个税年度汇算（综合所得）核对、个税年度汇算表对不上。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

HR, payroll staff, and individual employees use this skill during China individual income tax annual settlement review to check copied annual settlement table text for arithmetic consistency, duplicate employee IDs, blanks, and missing columns. It provides deterministic findings with cited source values and does not replace official filing, tax advice, or document authenticity checks.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill handles sensitive payroll and tax table data.

Mitigation: Use it only on intended local input files and keep generated findings within the same access controls as the source payroll or tax material.

Risk: The findings may be mistaken for tax advice or official filing guidance.

Mitigation: Treat outputs as arithmetic consistency checks and confirm tax positions, eligibility, and filing decisions with current rules or qualified reviewers.

Risk: The free version intentionally omits some checks that a user may expect from a complete tax review.

Mitigation: Review the reported executed checks and checks-not-run list before relying on a clean result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/iit-annual-settlement-check-free)
- [Sample input template](artifact/templates/sample.json)

## Skill Output:

**Output Type(s):** [text, JSON, guidance, shell commands]

**Output Format:** [Human-readable console text or structured JSON containing findings, executed checks, omitted checks, summary counts, and scope metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library, accepts pasted table text or JSON input, and reports insufficient input without producing a false clean result.]

## Skill Version(s):

1.0.17 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
