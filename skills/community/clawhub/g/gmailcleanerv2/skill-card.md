## Description: <br>
Gmail assistant pack for reading, searching, analyzing, organizing, responding to, scheduling, and reporting on Gmail messages via gog CLI or Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Coorops25](https://clawhub.ai/user/Coorops25) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect Gmail mailboxes, summarize or classify messages, organize labels and spam, draft or send replies, schedule email workflows, and produce reports. It is appropriate only when the user intends to grant broad Gmail management access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can request Gmail scopes beyond read-only, including modify and compose access. <br>
Mitigation: Review and limit Google OAuth scopes before use, and install only when broad Gmail management access is intended. <br>
Risk: Email organization workflows can move, trash, delete, or bulk-modify messages. <br>
Mitigation: Confirm every destructive or bulk action, avoid irreversible delete unless explicitly required, and test on small message sets first. <br>
Risk: Responder and scheduler workflows can draft, send, or automate email actions. <br>
Mitigation: Require explicit user confirmation before sending messages and avoid --auto or cron cleanup until behavior has been reviewed. <br>
Risk: Email contents may be sent to Anthropic-powered analysis or response generation and may be written to local logs or report files. <br>
Mitigation: Use the AI analysis and response features only for appropriate mailbox data, and review local audit logs, reports, and prompt logs for sensitive content handling. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Coorops25/gmailcleanerv2) <br>
- [Publisher profile](https://clawhub.ai/user/Coorops25) <br>
- [Google Gmail readonly scope](https://www.googleapis.com/auth/gmail.readonly) <br>
- [Google Gmail modify scope](https://www.googleapis.com/auth/gmail.modify) <br>
- [Google Gmail compose scope](https://www.googleapis.com/auth/gmail.compose) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON outputs from Gmail-related tools] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce local audit logs, Markdown reports, Gmail drafts, labels, or scheduled actions depending on the selected workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
