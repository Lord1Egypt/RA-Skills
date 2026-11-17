## Description:

个税累计预扣计算表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文行号。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

Proprietary

## Use Case:

HR and finance users use this skill to check Chinese payroll individual income tax cumulative withholding worksheets before payroll runs. It recalculates worksheet rows, checks totals, flags duplicate or blank entries, and reports insufficient input instead of inventing conclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the free subset as a complete tax review.

Mitigation: Review the listed withheld and out-of-scope checks, and obtain qualified tax review for special cases or tax advice.

Risk: Incomplete or unrecognized worksheet input can lead to no executed checks.

Mitigation: Provide a worksheet with recognizable headers and treat insufficient-input output as no conclusion.

Risk: Payroll data can be sensitive even when processed locally.

Mitigation: Install only when this Chinese payroll withholding checker is needed and handle input files under the user's normal payroll data controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/iit-withholding-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [Text, JSON, Analysis, Guidance]

**Output Format:** [Console text or JSON containing findings, summaries, executed checks, withheld checks, and missing-input guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings cite source line numbers; security evidence says the skill runs locally without network, persistence, or credential use.]

## Skill Version(s):

1.0.35 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
