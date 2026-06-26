## Description: <br>
Google Analytics CLI helps agents query Google Analytics 4 reports, realtime activity, account structure, and user behavior through google-analytics-cli. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bin-huang](https://clawhub.ai/user/bin-huang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to inspect GA4 properties, run standard and custom reports, monitor realtime users, and summarize analytics behavior from CLI JSON output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: GA4 reports, access reports, and audience export commands can expose sensitive analytics, identity, or audience data. <br>
Mitigation: Use a dedicated least-privilege service account scoped to the intended properties, avoid pasting credential JSON into chat, and require explicit approval before running access-report or audience-export commands. <br>
Risk: Default gcloud credentials may grant broader analytics access than the immediate task requires. <br>
Mitigation: Prefer per-command credentials or GOOGLE_APPLICATION_CREDENTIALS for a narrowly scoped service account, and verify access with an accounts command before running reports. <br>


## Reference(s): <br>
- [google-analytics-cli documentation](https://github.com/Bin-Huang/google-analytics-cli) <br>
- [GA4 Data API overview](https://developers.google.com/analytics/devguides/reporting/data/v1) <br>
- [Dimensions and metrics reference](https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema) <br>
- [Realtime API schema](https://developers.google.com/analytics/devguides/reporting/data/v1/realtime-api-schema) <br>
- [FilterExpression reference](https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/FilterExpression) <br>
- [OrderBy reference](https://developers.google.com/analytics/devguides/reporting/data/v1/rest/v1beta/OrderBy) <br>
- [Quotas and limits](https://developers.google.com/analytics/devguides/reporting/data/v1/quotas) <br>
- [GA4 Admin API](https://developers.google.com/analytics/devguides/config/admin/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance, Analysis] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GA4 property IDs and Google service account credentials; CLI output is pretty-printed JSON by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
