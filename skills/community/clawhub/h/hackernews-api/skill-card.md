## Description:

Helps agents monitor and search public Hacker News stories, items, and users through the read-only ReplyNodes gateway using a preconfigured API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[replynodes-ai](https://clawhub.ai/user/replynodes-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other agents use this skill to monitor public Hacker News stories, search discussions, and retrieve public items and user profiles without write access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests pass through ReplyNodes and consume prepaid credits.

Mitigation: Use only when comfortable with the gateway and associated credit spending.

Risk: A disclosed API key could grant unauthorized gateway access.

Mitigation: Keep the key in the agent's secret store; never share it in chat, logs, source files, or URLs.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/replynodes-ai/skills/hackernews-api)
- [Supported operations](references/operations.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with public Hacker News results or example GET commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public data; retain gateway response details and request IDs when reporting results.]

## Skill Version(s):

2.0.2 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
