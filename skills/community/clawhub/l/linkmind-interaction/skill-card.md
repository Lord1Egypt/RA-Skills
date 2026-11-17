## Description:

Operate LinkMind Interaction channel features against the hosted LinkMind server with API-key identity, including recommended, joined, and owned channels; subscribe and unsubscribe; monitor, list, and send messages; and create, enable, disable, delete, and translate channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhujunxian3](https://clawhub.ai/user/zhujunxian3)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage LinkMind Interaction and social channels from an agent without installing the LinkMind client. It supports channel discovery, subscription management, message monitoring and sending, channel publishing controls, and translation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can discover generic local credential files and send a LinkMind API key to a configurable remote server.

Mitigation: Use an explicit private --config file containing only the LinkMind key, avoid running from directories with .env or generic config files, and only set --base-url or LINKMIND_BASE_URL for a trusted server.

Risk: The skill can change LinkMind channel state, including subscribing, unsubscribing, creating, enabling, disabling, deleting, translating, and sending messages.

Mitigation: Review the requested operation before execution, use channel IDs for precision when available, and require explicit user confirmation before destructive delete operations.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhujunxian3/skills/linkmind-interaction)
- [LinkMind hosted service](https://ai.linkmind.top)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; bundled command output is JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill should summarize successful JSON responses and relay failed response messages without exposing API keys.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
