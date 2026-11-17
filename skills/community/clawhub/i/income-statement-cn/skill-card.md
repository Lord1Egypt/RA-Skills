## Description:

根据明细表数据自动生成规范格式的利润表 Excel，按收入、实收和支出分类动态汇总，并计算经营利润。

This skill is ready for commercial/non-commercial use.

## Publisher:

[courage-zen](https://clawhub.ai/user/courage-zen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate standardized Chinese income statement workbooks from financial detail spreadsheets, grouping income and expenses by category and computing operating profit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Input spreadsheet values can be carried into the generated workbook in a way that may preserve formula-like content.

Mitigation: Review spreadsheets received from other people or messaging workflows before use, and update the skill to escape category text beginning with formula-triggering characters such as =, +, -, @, tab, or carriage return.

Risk: The skill assumes a hard-coded local output path and Chinese-language workbook conventions.

Mitigation: Verify the configured paths, sheet name, column layout, and Chinese-language assumptions fit the deployment environment before running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/courage-zen/skills/income-statement-cn)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and shell command examples; generated artifact is an Excel workbook.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Assumes a Chinese-language input workbook with a sheet named 明细 and writes the generated workbook to a local output path.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
