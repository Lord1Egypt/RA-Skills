## Description: <br>
Controls a user's local Chrome browser through MCP Chrome DevTools or browser tools to query Outlook mail, jump to dates, filter or search messages, and read message bodies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyun2000](https://clawhub.ai/user/yuyun2000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
People with a configured OpenClaw environment use this skill to inspect a logged-in Outlook mailbox in Chrome, answer mail queries, navigate to messages by date, search for specific email, and read message content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent access to a logged-in Outlook mailbox through the user's active Chrome session. <br>
Mitigation: Use it only for narrow, explicit mail queries and avoid broad inbox reads. <br>
Risk: Chrome remote debugging and MCP browser control can expose more browser-session access than a single mail task requires. <br>
Mitigation: Enable the connection only when needed, then disable Chrome remote debugging or remove the MCP configuration when finished. <br>
Risk: The security evidence notes limited per-task consent or scope limits for mailbox access. <br>
Mitigation: Confirm the requested date range, sender, subject, or search term before reading mail, and report only the requested messages. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yuyun2000/outlook-mail-reader) <br>
- [Outlook Mail](https://outlook.cloud.microsoft/mail/) <br>
- [Outlook Inbox](https://outlook.cloud.microsoft/mail/inbox) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include mailbox summaries and setup or troubleshooting steps based on the user's active Outlook session.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
