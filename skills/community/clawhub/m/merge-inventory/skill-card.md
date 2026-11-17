## Description:

将用户上传的入库单 Excel 中多个表单的单据数据提取合并，转换为统一格式的标准汇总表并导出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingchazhushui](https://clawhub.ai/user/qingchazhushui)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations teams use this skill to standardize inbound-inventory Excel workbooks into a single formatted summary workbook. It is intended for source files that match the documented inbound inventory layout, including multi-sheet and multi-document inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Inputs that do not match the documented inbound-inventory layout can produce an incorrect workbook.

Mitigation: Confirm the source workbook structure, target sheet selection, and intended output path before running the skill.

Risk: The skill writes a formatted output workbook to a user-specified path.

Mitigation: Choose a deliberate output path and avoid reusing an existing important workbook path unless overwriting is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qingchazhushui/skills/merge-inventory)
- [Artifact skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Files, Guidance, Shell commands]

**Output Format:** [Excel workbook (.xlsx), with concise text or shell-command guidance when used by an agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads user-provided inbound-inventory spreadsheets and writes a standardized summary workbook.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
