## Description: <br>
Scores website leads from audit signals, assigns priority tiers, and writes the results to Google Sheets for lead-list workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick-software](https://clawhub.ai/user/maverick-software) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Sales, growth, and operations teams use this skill to prioritize website leads after auditing and contact enrichment. It scores each lead, explains the matching issues, assigns a Hot/Warm/Lukewarm/Cold tier, and prepares Google Sheets output for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create a Google Sheet containing lead contact data and make it publicly writable. <br>
Mitigation: Remove automatic public writer sharing, use a private pre-created spreadsheet or explicit named-account sharing, and confirm that storing lead emails and phone numbers in Google Sheets is acceptable for the workflow. <br>
Risk: Google Sheets and Drive access uses a service account that can read or modify spreadsheet resources available to it. <br>
Mitigation: Use a dedicated low-privilege Google service account and restrict the credentials to only the spreadsheets needed for this workflow. <br>


## Reference(s): <br>
- [Lead Scorer on ClawHub](https://clawhub.ai/maverick-software/lead-scorer-pro) <br>
- [Publisher profile](https://clawhub.ai/user/maverick-software) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Markdown with Python code examples and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces lead scores, priority tiers, issue labels, score breakdowns, and Google Sheets rows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
