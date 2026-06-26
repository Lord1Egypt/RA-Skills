## Description: <br>
Gmail: Reply to a message (handles threading automatically). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[googleworkspace-bot](https://clawhub.ai/user/googleworkspace-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Users who manage Gmail through the gws CLI use this skill to draft or send threaded replies, including optional recipients, HTML bodies, and attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help send real Gmail replies, including additional recipients, HTML content, and attachments. <br>
Mitigation: Confirm the Gmail account, message ID, recipients, body, quoted thread, and attachments before sending; use --dry-run or --draft for sensitive replies. <br>
Risk: The workflow depends on the external gws CLI and its Gmail authentication setup. <br>
Mitigation: Install and use it only in environments where the gws CLI and configured Gmail account are trusted. <br>


## Reference(s): <br>
- [Gws Gmail Reply on ClawHub](https://clawhub.ai/googleworkspace-bot/gws-gmail-reply) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the external gws CLI and Gmail authentication; replies can be sent, drafted, or dry-run.] <br>

## Skill Version(s): <br>
1.0.14 (source: server release metadata; artifact metadata version 0.22.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
