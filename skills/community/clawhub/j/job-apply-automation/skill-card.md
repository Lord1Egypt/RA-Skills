## Description: <br>
Automated job application assistant that searches job boards and direct URLs, drafts personalized application emails with a CV attached, sends them through Gmail SMTP, and maintains a JSON application tracker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Z-Hussein](https://clawhub.ai/user/Z-Hussein) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Job seekers use this skill to find matching roles, prepare tailored application emails, send applications from a dedicated Gmail account, and track application status across the job search workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically email employers with a CV and may reply to recruiters on the user's behalf. <br>
Mitigation: Use a dedicated job-search mailbox and keep manual approval enabled for every outgoing email, especially before trusting auto mode. <br>
Risk: The tracker can contain sensitive job-search history, recruiter details, interview information, and application outcomes. <br>
Mitigation: Regularly inspect, secure, or delete Applications.json and avoid sharing it outside the intended workspace. <br>
Risk: Email credentials and personal profile data are required for normal operation. <br>
Mitigation: Use a Gmail app password for a dedicated account, avoid storing main-account credentials, and keep filled CONFIG.md and profile files private. <br>
Risk: Notifications may expose application activity or personal information through WhatsApp. <br>
Mitigation: Review notification behavior and remove or limit notification details if the channel is shared or not private. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Z-Hussein/job-apply-automation) <br>
- [README](README.md) <br>
- [Platform Notes](references/Platform-notes.md) <br>
- [Tracker Commands](references/Tracker-commands.md) <br>
- [Configuration Template](references/config.md) <br>
- [Email Templates](references/email-templates.md) <br>
- [Job Profile Template](references/job-profile.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, drafted email text, JSON tracker updates, and setup commands or configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send application emails with CV attachments and update Applications.json when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
