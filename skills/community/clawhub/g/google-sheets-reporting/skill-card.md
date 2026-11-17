## Description:

Automated reporting and alerts from Google Sheets data through daily summaries, configurable threshold alerts, and weekly multi-sheet digest emails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mhmalvi](https://clawhub.ai/user/mhmalvi)

### License/Terms of Use:

CC BY-NC-SA 4.0

## Use Case:

Operations, sales, support, marketing, and finance teams use this skill to turn Google Sheets data into scheduled n8n reports and threshold alerts sent by email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated emails may include Google Sheets data that is sensitive or not approved for reporting.

Mitigation: Use only approved sheets, set REPORT_EMAIL deliberately, and scope Google Sheets and SMTP credentials to the minimum required.

Risk: Generated report and alert emails include sheet-derived HTML content.

Mitigation: HTML-escape sheet-derived fields or convert reports to plain text before production use.

## Reference(s):

- [Google Sheets Reporting on ClawHub](https://clawhub.ai/mhmalvi/skills/google-sheets-reporting)
- [mhmalvi publisher profile](https://clawhub.ai/user/mhmalvi)

## Skill Output:

**Output Type(s):** [configuration, guidance, json]

**Output Format:** [n8n workflow JSON files with Markdown setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REPORT_EMAIL, optional ALERT_THRESHOLDS, Google Sheets OAuth2 credentials, and SMTP credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
