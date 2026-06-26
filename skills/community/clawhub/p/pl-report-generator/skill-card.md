## Description: <br>
Generates automated financial and business reports with PDF output, chart creation, and distribution workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance teams, accounting firms, and business operators use this skill to turn batch financial data from CSV exports, spreadsheets, or finance systems into reviewed P&L, KPI, variance, and executive reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Financial source data and generated reports may contain sensitive client, payroll, or business information. <br>
Mitigation: Use least-privilege access, keep raw data out of git, redact sensitive fields before sharing, and store source data only in controlled report directories. <br>
Risk: Automated email or messaging distribution can send reports to unintended recipients or channels. <br>
Mitigation: Review generated PDFs before sending and explicitly confirm recipients, channels, and approval before any email or Telegram distribution. <br>
Risk: Spreadsheet or finance-system integrations may expose or modify source data if granted broad permissions. <br>
Mitigation: Prefer read-only credentials for source tabs and write summaries to a separate output sheet when Google Sheets or similar systems are used. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samledger67-dotcom/pl-report-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Files] <br>
**Output Format:** [Markdown with inline bash and Python code blocks; report artifacts may include PDFs, CSV or JSON data, and chart images.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires human review before distribution and careful handling of sensitive financial data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
