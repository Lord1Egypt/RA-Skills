## Description:

自动更新投后管理报告；当用户需要根据新财务报表和访谈纪要更新季度投后管理报告、生成财务数据分析、更新公司经营情况和行业分析时使用

This skill is ready for commercial/non-commercial use.

## Publisher:

[kinomoon](https://clawhub.ai/user/kinomoon)

### License/Terms of Use:

MIT-0

## Use Case:

Investment and portfolio management teams use this Chinese-language skill to update quarterly post-investment management reports from a new financial statement, interview minutes, and the prior quarter's DOCX report. It helps extract financial metrics, draft financial and operating analysis, preserve report structure, and generate an updated DOCX report for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow handles sensitive financial statements, interview notes, and post-investment reports.

Mitigation: Use copies of confidential source documents where possible and control access to input, intermediate, and output files.

Risk: Generated financial analysis or investment recommendations may be incomplete or inaccurate.

Mitigation: Review all generated analysis against the original statements, interview notes, and internal investment judgment before sharing or relying on the report.

Risk: The report generator writes to a user-selected output path.

Mitigation: Choose the output path deliberately to avoid overwriting important files or placing sensitive reports in shared locations.

## Reference(s):

- [投后管理报告结构](references/report-structure.md)
- [财务分析指南](references/financial-analysis-guide.md)
- [内容更新模板](references/content-update-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON extraction output, generated analysis text, and DOCX report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local XLS/XLSX and DOCX inputs; generated financial analysis and investment recommendations require user review before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
