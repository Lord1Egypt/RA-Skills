## Description: <br>
Generate structured, blame-free incident postmortem reports from logs, timeline data, and incident metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, SREs, incident commanders, and operations teams use this skill to draft post-incident reviews, reconstruct timelines from logs or JSON inputs, summarize impact and root cause, and check reports for blameful language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incident logs and generated postmortems may include secrets, customer data, or internal operational details. <br>
Mitigation: Process only intended local files and store generated reports in trusted locations with appropriate access controls. <br>
Risk: Generated root cause, timeline, impact, or action item content may be incomplete or misleading if source logs or incident metadata are incomplete. <br>
Mitigation: Have the incident team review and correct the generated report before sharing or using it as an official record. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/charlie-morrison/incident-postmortem-generator) <br>
- [Publisher profile](https://clawhub.ai/user/charlie-morrison) <br>
- [Postmortem templates and guidelines](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, HTML, JSON, or plain text reports with optional shell command examples and structured incident fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write reports to user-selected output paths and can return CI-style exit codes based on severity or detected log errors.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
