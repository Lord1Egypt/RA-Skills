## Description: <br>
Send and receive WhatsApp messages, manage groups, contacts, and instances via GREEN-API MCP gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[support-greenapi](https://clawhub.ai/user/support-greenapi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect a GREEN-API WhatsApp instance to OpenClaw so an agent can send messages, read chat history, manage contacts and groups, and administer instances through the GREEN-API MCP gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose WhatsApp messages, contacts, group membership, files, and account state to an agent. <br>
Mitigation: Install only when the GREEN-API MCP endpoint and connected WhatsApp account are trusted; use least-privilege or non-production credentials where possible and avoid sharing API tokens in ordinary chat. <br>
Risk: The skill can perform high-impact actions such as sending, forwarding, editing, deleting, changing settings, logging out, rebooting, modifying groups, and deleting instances. <br>
Mitigation: Require explicit user confirmation before mutating chats, groups, settings, authorization state, or partner instances. <br>
Risk: Broad chat history and notification reads can reveal more personal or business data than needed. <br>
Mitigation: Limit history and notification reads to specific chats and small counts, and review requests before retrieving recent inbound or outbound messages. <br>


## Reference(s): <br>
- [GREEN-API ClawHub Skill Page](https://clawhub.ai/support-greenapi/green-api) <br>
- [GREEN-API](https://green-api.com) <br>
- [GREEN-API Documentation](https://green-api.com/en/docs/) <br>
- [GREEN-API Console](https://console.green-api.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke GREEN-API MCP tools to send messages, read history, manage groups, contacts, files, notifications, settings, and instances.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
