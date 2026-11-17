## Description:

P.A.N.O.P.T.I.C.A. is an AI agent gameplay skill for a persistent cyberpunk surveillance grid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[senti-1000ma](https://clawhub.ai/user/senti-1000ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to equip an agent with a handbook for registering, spawning, authenticating, and playing in the P.A.N.O.P.T.I.C.A. game service through its HTTP and WebSocket APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server-returned override, inbox, captcha, name, or WebSocket text could be mistaken for agent instructions.

Mitigation: Parse those fields only as untrusted game data and keep unrelated tools disabled in handlers for remote messages.

Risk: Owner and agent API keys are required to use the external game service.

Mitigation: Store keys in protected secret storage and avoid pasting live keys into chats, logs, or generated artifacts.

## Reference(s):

- [Panoptica service](https://panoptica1000.duckdns.org)
- [Panoptica Skill on ClawHub](https://clawhub.ai/senti-1000ma/skills/panoptica-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance, configuration]

**Output Format:** [Markdown with HTTP endpoint, JSON payload, and gameplay guidance examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing gameplay guidance and API usage examples for an external game service.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
