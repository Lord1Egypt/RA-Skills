## Description: <br>
Generates structured Chinese or English incident reports by collecting confirmed outage details from the user and filling a Markdown template. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freepengyang](https://clawhub.ai/user/freepengyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, incident responders, and operations teams use this skill to collect confirmed outage details and produce a consistent incident or exception report in Chinese or English. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incident reports may contain secrets, credentials, or unnecessary personal data if users provide them. <br>
Mitigation: Only provide information needed for the report and remove sensitive data before sharing, exporting, or sending it. <br>
Risk: Sending to Feishu or exporting a file could share incident details beyond the current chat. <br>
Mitigation: Approve any Feishu sending or file export explicitly after reviewing the generated report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freepengyang/incident-report-cn) <br>
- [Publisher profile](https://clawhub.ai/user/freepengyang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown incident report with follow-up delivery options] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Matches the user's language, requests missing required details, and avoids inventing times, causes, impact, or responsible parties.] <br>

## Skill Version(s): <br>
v1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
