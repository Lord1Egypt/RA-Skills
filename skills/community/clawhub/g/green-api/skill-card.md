## Description:

Send and receive WhatsApp messages, manage groups, contacts, and instances via GREEN-API MCP gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[support-greenapi](https://clawhub.ai/user/support-greenapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external teams use this skill to let an agent operate a GREEN-API WhatsApp instance for messaging, files, contacts, groups, chat history, and instance administration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose private WhatsApp messages and account data through chat history, contact, and notification tools.

Mitigation: Install only for trusted GREEN-API accounts and require explicit user confirmation before reading histories or retrieving message data.

Risk: Instance and partner tokens can grant access to WhatsApp account operations.

Mitigation: Treat tokens as secrets and use a safer secret store instead of pasting real credentials into general chat when available.

Risk: Messaging, group, settings, logout, reboot, and instance-deletion actions can change account state or affect recipients.

Mitigation: Require explicit confirmation before sending, deleting, forwarding, changing groups or settings, logging out, rebooting, or deleting instances.

## Reference(s):

- [GREEN-API Documentation](https://green-api.com/en/docs/)
- [GREEN-API Console](https://console.green-api.com)
- [GREEN-API](https://green-api.com)
- [ClawHub Skill Page](https://clawhub.ai/support-greenapi/skills/green-api)
- [Publisher Profile](https://clawhub.ai/user/support-greenapi)

## Skill Output:

**Output Type(s):** [API Calls, Text, Markdown, Configuration]

**Output Format:** [Agent guidance and tool calls for GREEN-API WhatsApp operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected GREEN-API instance and valid instance credentials before most WhatsApp operations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
