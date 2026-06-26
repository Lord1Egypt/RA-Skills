## Description: <br>
Search Outlook mail, read threads, manage drafts, send or reply to email, and manage calendar events via Microsoft Graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users use this skill to manage Outlook email, calendar events, contacts, attachments, rules, and categories through Microsoft Graph with ClawLink-managed OAuth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive Outlook mail, calendar, contact, and task data through a connected Microsoft account. <br>
Mitigation: Review Microsoft consent scopes before connecting Outlook through ClawLink and revoke the connection when access is no longer needed. <br>
Risk: Write actions can send email, delete messages, cancel events, or modify Outlook resources. <br>
Mitigation: Use explicit confirmation and preview flows before send, delete, create, update, move, or cancel operations. <br>
Risk: Batch operations can affect multiple mailbox items in one call. <br>
Mitigation: Review the target item list before execution and keep batch moves or updates within the documented 20-item limit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hith3sh/outlook-inbox) <br>
- [Microsoft Graph Mail API overview](https://learn.microsoft.com/graph/api/resources/mail-api-overview) <br>
- [Microsoft Graph Calendar API](https://learn.microsoft.com/graph/api/resources/calendar) <br>
- [Microsoft Graph Message resource](https://learn.microsoft.com/graph/api/resources/message) <br>
- [Microsoft Graph Event resource](https://learn.microsoft.com/graph/api/resources/event) <br>
- [ClawLink OpenClaw docs](https://docs.claw-link.dev/openclaw) <br>
- [ClawLink verification](https://claw-link.dev/verify) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connected Microsoft account through ClawLink; write actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
