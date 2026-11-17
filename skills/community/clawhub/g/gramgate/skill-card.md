## Description:

Telegram gateway for AI agents and automation. Use GramGate to access a real Telegram account over REST or MCP: read channels and history, search across chats, click inline buttons, join groups, and send messages as a user account rather than a bot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zakirovdmr](https://clawhub.ai/user/zakirovdmr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use GramGate to give agents structured Telegram read/write access through REST or MCP for channel monitoring, content workflows, Telegram E2E testing, support, CRM, and notification flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill enables sensitive Telegram account read/write automation, including sending, editing, deleting, joining, leaving, pinning, reacting, and button-click actions as the user account.

Mitigation: Install only when real Telegram account access is intended, review write-side tasks before execution, and write only when the task requires it.

Risk: Exposing GramGate beyond localhost could broaden access to a real Telegram account.

Mitigation: Keep the service bound to localhost when possible, and require authentication and rate limits if it is exposed.

## Reference(s):

- [GramGate ClawHub skill page](https://clawhub.ai/zakirovdmr/skills/gramgate)
- [GramGate GitHub repository](https://github.com/zakirovdmr/gramgate)
- [zakirovdmr ClawHub publisher profile](https://clawhub.ai/user/zakirovdmr)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline bash code blocks and endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 according to ClawHub metadata.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
