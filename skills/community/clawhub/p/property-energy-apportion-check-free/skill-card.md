## Description:

公共能耗抄表与分摊明细表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文。本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

Property managers, property accountants, and regional finance staff use this skill before monthly billing or periodic review to check public energy apportionment tables for arithmetic mismatches, allocation total issues, ratio errors, duplicates, and missing fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The checker is limited to the listed free checks and does not cover the full set of apportionment review tasks.

Mitigation: Review the checks_not_run output and perform any required cross-building, cross-period, ranking, or root-cause analysis separately.

Risk: The tool checks table-internal arithmetic and consistency, not whether the underlying charges, allocation method, or legal treatment are correct.

Mitigation: Confirm source bills, property service contracts, management rules, and local requirements before relying on billing decisions.

Risk: Chinese-language input and output may be misunderstood by non-Chinese reviewers.

Mitigation: Have a reviewer who can read the input tables and Chinese findings validate any billing or disclosure action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/property-energy-apportion-check-free)
- [ClawHub publisher profile](https://clawhub.ai/user/chenqg618)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Human-readable terminal text or JSON with status, scope, findings, summary, and missing-input guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node.js standard library; JSON mode is available for machine-readable review output.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
