## Description:

商场联营抽成与保底核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Finance and cashiering users use this skill during month-end settlement, reconciliation, or inventory-close workflows to check mall concession rent tables for arithmetic consistency, totals, duplicate rows, blanks, and negative values. The skill is intended for local table reconciliation, not legal, tax, contract, POS, ERP, or full audit review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the reconciliation output as legal, tax, contract, POS, ERP, or full audit assurance.

Mitigation: Use the output as a local arithmetic and table-consistency check only, and review the original contract, tax, POS, ERP, and audit materials before making financial decisions.

Risk: The free edition does not run every check associated with the broader mall concession workflow.

Mitigation: Review the runtime lists of checks performed and checks not run before relying on the result for month-end close or settlement.

Risk: Missing, malformed, or insufficient table input can prevent the skill from reaching a conclusion.

Mitigation: Provide the copied table text with recognizable headers and treat any insufficient-input response as no reconciliation conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/mall-concession-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Console text or JSON report with findings, scope, summary, omitted checks, and insufficient-input guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source rows when produced; missing or unusable table input returns insufficient-input guidance instead of a reconciliation conclusion.]

## Skill Version(s):

1.0.58 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
