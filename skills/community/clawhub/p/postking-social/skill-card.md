## Description:

Generate, approve, and schedule social posts on PostKing across LinkedIn, X, Instagram, Threads, and Facebook, plus content weeks and repurposing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitsandtea](https://clawhub.ai/user/bitsandtea)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing teams use this skill to manage the PostKing social-post lifecycle, including drafting, approving, scheduling, repurposing, account connection, assets, templates, and per-platform rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide account disconnection, asset deletion, template deletion, social-rule changes, and recurring schedule changes.

Mitigation: Require the agent to restate the exact target and obtain explicit user confirmation before taking those actions.

Risk: The skill manages publishing and scheduling workflows that can affect public brand channels.

Mitigation: Review generated or repurposed post content and confirm scheduled times before approval.

## Reference(s):

- [PostKing Social on ClawHub](https://clawhub.ai/bitsandtea/skills/postking-social)
- [PostKing MCP endpoint](https://mcp.postking.app/mcp)
- [PostKing Social icon](https://raw.githubusercontent.com/bitsandtea/postking-skills/main/assets/icons/postking-social.svg)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tool-call parameters and optional CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an active PostKing brand and an MCP-compatible client connected to postking-mcp; the pking CLI is an optional fast path when a shell is available.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
