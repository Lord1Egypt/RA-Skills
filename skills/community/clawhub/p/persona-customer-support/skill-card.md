## Description: <br>
Manage customer support: track tickets, respond, and escalate issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Support teams use this persona to triage support inboxes, turn customer emails into tickets, log ticket status, escalate urgent issues, and schedule follow-ups across Google Workspace tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access customer email and update shared business tools without clear approval or data-handling limits. <br>
Mitigation: Install it only for an authorized support account, configure least-privilege access, and define approved data handling boundaries before use. <br>
Risk: Incorrect support labels, sheets, Chat spaces, or calendars could send customer information to the wrong destination. <br>
Mitigation: Confirm the support label, target tracking sheet, escalation space, and follow-up calendar before running the workflow. <br>
Risk: Customer-facing replies, escalation posts, or follow-up events may be inappropriate if generated without review. <br>
Mitigation: Require human review before sending messages to customers, posting escalations, or creating follow-up events. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/persona-customer-support) <br>
- [Publisher profile](https://clawhub.ai/user/googleworkspace-bot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with Google Workspace CLI commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires gws and the gws-gmail, gws-sheets, gws-chat, and gws-calendar skills.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
