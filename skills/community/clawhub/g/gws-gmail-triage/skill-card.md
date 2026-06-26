## Description: <br>
Gmail: Show unread inbox summary (sender, subject, date). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers can use this skill to ask an agent for a concise summary of unread Gmail inbox messages, including sender, subject, and date metadata. It is intended for read-only email triage through the trusted gws CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unread Gmail sender, subject, date, and label metadata may be exposed to the agent or surrounding session. <br>
Mitigation: Use the skill only where that metadata is appropriate to share, and avoid copying outputs into contexts that should not contain email metadata. <br>
Risk: The skill depends on the local gws CLI and its Gmail authentication configuration. <br>
Mitigation: Install only a trusted gws CLI, confirm it is connected to the intended Google account, and review the shared auth and security guidance before use. <br>
Risk: Broad queries or high message limits can return more unread email metadata than intended. <br>
Mitigation: Prefer narrow Gmail queries and conservative --max values when triaging sensitive inboxes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/googleworkspace-bot/gws-gmail-triage) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash examples; command output is table text by default and can be JSON when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Gmail metadata summary; default maximum is 20 unread messages unless changed with flags.] <br>

## Skill Version(s): <br>
1.0.12 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
