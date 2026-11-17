## Description:

OpenClaw plugin for Otto Travel -- search, compare, and book flights and hotels via Otto's MCP endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cd-otto](https://clawhub.ai/user/cd-otto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to connect an agent to Otto Travel's MCP endpoint for flight and hotel search, booking, booking lookup, preferences, and loyalty program management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A configurable remote MCP server receives OAuth material and travel details.

Mitigation: Use only the default Otto HTTPS endpoint unless the custom server is fully trusted.

Risk: The skill can book travel and change preferences or loyalty-program data through authenticated tools.

Mitigation: Require explicit user confirmation before any booking, preference, or loyalty-program change.

Risk: OAuth tokens are stored locally and can grant account access if exposed.

Mitigation: Treat the local token file as sensitive and keep access restricted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cd-otto/skills/otto-travel-local)
- [Otto MCP endpoint](https://api.ottotheagent.com/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and text responses with configuration snippets and tool-call results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Discovers available MCP tools dynamically from the configured Otto server.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
