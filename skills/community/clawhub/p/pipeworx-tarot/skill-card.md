## Description:

Draw and search all 78 Rider-Waite tarot cards with upright and reversed meanings, including single or multiple card spreads and detailed lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent draw tarot cards, search the Rider-Waite deck, and retrieve upright and reversed meanings through the documented MCP endpoint.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tarot requests are sent to a documented third-party MCP endpoint.

Mitigation: Avoid sending private or sensitive information in tarot queries unless the user trusts that service.

## Reference(s):

- [Pipeworx tarot ClawHub page](https://clawhub.ai/brucegutman/skills/pipeworx-tarot)
- [brucegutman publisher profile](https://clawhub.ai/user/brucegutman)
- [Tarot MCP endpoint](https://gateway.pipeworx.io/tarot/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and JSON examples; MCP tool results return card text and structured card details.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requests are sent to a third-party MCP endpoint documented by the artifact.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
