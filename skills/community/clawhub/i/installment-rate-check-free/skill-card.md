## Description:

分期方案核对表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文行号。本免费版执行引擎声明的免费检查项。触发词包括 分期实际年化、IRR、月费率陷阱、分期成本。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators use this skill to check copied installment-rate worksheets for nominal fee, payment, annualized rate, total-row, duplicate-row, and blank-field issues. The skill is intended for deterministic worksheet checking and does not make financing decisions or provide financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a bundled Node script through Bash, so users could execute an unintended path or inspect the wrong local input file.

Mitigation: Review the command path before execution and provide only the worksheet input intended for checking.

Risk: Installment-rate findings could be mistaken for financial advice or a recommendation to accept a financing option.

Mitigation: Treat the output as deterministic worksheet checking only; review financing decisions separately with the appropriate business or financial process.

Risk: Incomplete or malformed worksheet material can prevent reliable conclusions.

Mitigation: Provide a worksheet with recognizable headers and source rows; when material is insufficient, the skill should report missing inputs instead of producing a conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/installment-rate-check-free)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Shell commands]

**Output Format:** [Markdown or JSON-formatted check results with source line references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally through bundled Node scripts; JSON output is available with --json.]

## Skill Version(s):

1.0.32 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
