## Description: <br>
Automated reporting and alerts from Google Sheets data. Daily summaries with auto-detected metrics, configurable threshold alerts, and weekly multi-sheet digest emails. 3 production-ready n8n workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mhmalvi](https://clawhub.ai/user/mhmalvi) <br>

### License/Terms of Use: <br>
CC BY-NC-SA 4.0 <br>


## Use Case: <br>
Operations, sales, support, marketing, and finance teams use this skill to import n8n workflows that read Google Sheets, summarize metrics, check thresholds, and email scheduled reports or alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Spreadsheet contents are sent by email to the configured report recipient. <br>
Mitigation: Install only for sheets whose contents are appropriate to email, and verify REPORT_EMAIL, SMTP credentials, and approved recipients before activation. <br>
Risk: The imported workflows can run continuously on daily, hourly, or weekly schedules. <br>
Mitigation: Disable schedules that should not run continuously and review alert thresholds before enabling the workflows. <br>
Risk: Google Sheets access may expose more spreadsheet data than intended. <br>
Mitigation: Use least-privilege Google Sheets credentials and avoid regulated or highly sensitive spreadsheets unless recipients are approved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mhmalvi/google-sheets-reporting) <br>
- [Daily summary workflow](artifact/workflows/01-daily-summary.json) <br>
- [Threshold alerts workflow](artifact/workflows/02-threshold-alerts.json) <br>
- [Weekly digest workflow](artifact/workflows/03-weekly-digest.json) <br>


## Skill Output: <br>
**Output Type(s):** [configuration, code, guidance] <br>
**Output Format:** [JSON workflow files with Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires n8n, Google Sheets OAuth2, SMTP credentials, REPORT_EMAIL, and optional ALERT_THRESHOLDS.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
