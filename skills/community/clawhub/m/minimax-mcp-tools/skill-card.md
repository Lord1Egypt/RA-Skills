## Description:

Provides MiniMax-backed web search and image understanding tools through MCP for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hongjiahao371-pixel](https://clawhub.ai/user/hongjiahao371-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure MiniMax MCP tools so an agent can search the web and analyze images from URLs or local paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation path executes mutable third-party MCP package code.

Mitigation: Pin and verify the MCP package version before installation.

Risk: The configuration stores a MiniMax API key in plain local MCP configuration.

Mitigation: Restrict the OpenClaw configuration file permissions and use a limited, rotatable MiniMax API key.

Risk: MiniMax may receive search queries and image inputs, including local image files selected for analysis.

Mitigation: Use the skill only for data that is appropriate to send to MiniMax.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hongjiahao371-pixel/skills/minimax-mcp-tools)
- [MiniMax Token Plan](https://platform.minimaxi.com/subscribe/token-plan)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing guidance for installing, configuring, and calling MiniMax MCP search and image-understanding tools.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact changelog, released 2026-03-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
