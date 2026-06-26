## Description: <br>
Business KPI monitoring with threshold-based alerts that connects to QuickBooks Online, Google Sheets, and CSV exports to track AR aging, cash runway, revenue growth, gross margin, and burn rate, then sends alerts through Telegram, Slack, or email when thresholds breach. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samledger67-dotcom](https://clawhub.ai/user/samledger67-dotcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Finance operators, bookkeepers, and developers use this skill to define KPI thresholds, run periodic financial health checks, and route alerts for breached business metrics. It is suited to AR aging, cash runway, burn rate, revenue growth, margin, and liquidity monitoring from QBO, Sheets, or CSV data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: KPI alerts may expose sensitive financial data through Telegram, Slack, email, or generated summaries. <br>
Mitigation: Use only approved private destinations and avoid including exact sensitive values unless the recipient and channel are authorized. <br>
Risk: Source integrations and exported CSV files can broaden access to financial records. <br>
Mitigation: Use read-only QuickBooks and Sheets access where possible and keep CSV exports in controlled workspace locations. <br>
Risk: Scheduled KPI checks can continue sending outdated or misrouted alerts if cron settings are not maintained. <br>
Mitigation: Periodically review cron schedules, alert recipients, and configured thresholds before ongoing deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samledger67-dotcom/kpi-alert-system) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, Code, Markdown] <br>
**Output Format:** [Markdown with YAML, JSON, Python pseudocode, and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces KPI configuration patterns, scheduling payloads, and alert message formats; no executable package is included.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
