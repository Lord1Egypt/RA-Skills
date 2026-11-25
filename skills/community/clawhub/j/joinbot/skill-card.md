## Description:

Join a Microsoft Teams, Zoom, or Google Meet meeting and answer aloud when addressed by name, when the user provides a meeting link or asks you to attend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engmsaleh](https://clawhub.ai/user/engmsaleh)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use JoinBot to join a meeting at the user's request, listen for questions, and respond aloud or in meeting chat. Meeting participants can address the agent by its registered name.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can contribute to a meeting without a direct address when engagement is set to helpful or active.

Mitigation: Set engagement to addressed when you want replies only after a direct address.

Risk: The skill retrieves the full meeting transcript and instructs the agent to save useful transcript-derived content in memory.

Mitigation: Review transcript-derived content before saving it, and retain only what is needed.

## Reference(s):

- [JoinBot](https://usejoinbot.com)
- [JoinBot MCP server](https://usejoinbot.com/api/mcp)
- [ClawHub skill page](https://clawhub.ai/engmsaleh/skills/joinbot)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Text]

**Output Format:** [Markdown instructions, spoken meeting replies, and optional meeting chat messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Spoken replies are one to three short sentences (under about 110 words); longer details can go in meeting chat.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
