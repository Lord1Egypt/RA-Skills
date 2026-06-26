## Description: <br>
自动更新投后管理报告；当用户需要根据新财务报表和访谈纪要更新季度投后管理报告、生成财务数据分析、更新公司经营情况和行业分析时使用. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kinomoon](https://clawhub.ai/user/kinomoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investment teams and portfolio operators use this skill to update quarterly post-investment management reports from new financial statements, interview notes, and the prior quarter's report. It helps extract financial data, draft financial and business updates, add industry analysis, and generate an updated Word report for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial statements, interview notes, and prior reports may contain confidential business information. <br>
Mitigation: Provide only the intended input files, review where industry analysis is performed, and check the generated report for sensitive details before sharing. <br>
Risk: Generated financial analysis or report updates may be inaccurate or incomplete. <br>
Mitigation: Review the generated report against the source documents and verify key figures, conclusions, and output filename before distribution. <br>
Risk: Dependency installation from untrusted sources can introduce supply-chain risk. <br>
Mitigation: Install openpyxl and python-docx from trusted package sources and pin the documented dependency versions. <br>


## Reference(s): <br>
- [Report Structure](references/report-structure.md) <br>
- [Financial Analysis Guide](references/financial-analysis-guide.md) <br>
- [Content Update Template](references/content-update-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON intermediate data, analysis text, and DOCX report file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses user-provided XLS/XLSX financial statements and DOCX documents; generated reports should be reviewed before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
