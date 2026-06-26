## Description: <br>
This skill helps an agent use Gmail through gogcli for mailbox reading, organization, drafts, forwarding, autoreplies, attachments, and bulk message operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to work with a selected Gmail account in depth, including threads, labels, drafts, attachments, forwarding, autoreplies, and bulk archive, trash, or mark-read operations. It is appropriate only when the user intends to grant broad Gmail mailbox and account-setting authority. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad access to Gmail messages and account settings. <br>
Mitigation: Review before installing for sensitive personal or business mail, and authorize only the Gmail account the user intends to expose. <br>
Risk: The skill can support permanent deletion, forwarding, delegates, forwarding settings, filters, send-as settings, vacation responders, watch notifications, tracking, sending mail, and downloading message content. <br>
Mitigation: Require explicit confirmation before any destructive action, message sending, forwarding, settings change, tracking action, or message-content download. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/gogcli-mcp-gmail) <br>
- [gogcli project](https://github.com/openclaw/gogcli) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with JSON MCP server configuration and Gmail tool-use instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can lead an agent to invoke Gmail MCP tools that read, send, modify, delete, forward, download, or change Gmail account settings after authorization.] <br>

## Skill Version(s): <br>
2.8.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
