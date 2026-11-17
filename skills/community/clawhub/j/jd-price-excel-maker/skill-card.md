## Description:

根据用户提供的电脑/服务器配置清单（图片、截图或文本），在京东平台搜索各配件的价格与商品链接，并生成包含京东链接的 Excel 价格表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhaorui](https://clawhub.ai/user/wuhaorui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and procurement or system-building teams use this skill to turn computer or server configuration lists into Excel workbooks with JD.com reference prices, product links, subtotals, and notes about pricing limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated workbook can present static product prices as if they were live JD.com quotes.

Mitigation: Confirm prices manually on the linked product pages before purchase or procurement decisions, and state that workbook prices are time-limited references.

Risk: The bundled helper script writes to a hardcoded path outside the stated workspace.

Mitigation: Review and edit the output path before running the script, and require an explicit non-overwrite location inside the workspace.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/wuhaorui/skills/jd-price-excel-maker)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files, guidance]

**Output Format:** [Markdown response plus generated .xlsx workbook and optional Python/openpyxl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated workbooks may contain static JD.com reference prices and clickable product hyperlinks.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
