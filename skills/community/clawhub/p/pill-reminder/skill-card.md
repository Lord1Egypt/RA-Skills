## Description: <br>
Pill Reminder helps an OpenClaw agent set up scheduled medication or supplement reminders, track took or did-not-take responses, issue refill alerts, and produce printable adherence logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bgoodwinstudio](https://clawhub.ai/user/bgoodwinstudio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and caregivers use this skill to configure medication reminders, maintain local pill schedules and adherence logs, and prepare printable summaries for medical appointments. It supports reminder and tracking workflows only and is not medical advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medication schedules, reminder messages, and adherence logs may contain sensitive health information. <br>
Mitigation: Use private direct-message channels, avoid shared groups for family medical information, and remove schedules and logs when they are no longer needed. <br>
Risk: Reminder setup errors could lead to missed, duplicated, or mistimed reminder messages. <br>
Mitigation: Review generated cron reminders and the local pills.md schedule after setup or medication changes. <br>
Risk: Users could mistake reminder and adherence text for medical guidance. <br>
Mitigation: Keep the not-medical-advice disclaimer visible and consult a doctor or pharmacist for medication decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/bgoodwinstudio/pill-reminder) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text reminders, local markdown configuration and log files, and scheduled command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates and updates local pills.md and pill-log.md files; reminder delivery depends on the user's configured chat channel and cron setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version and artifact SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
