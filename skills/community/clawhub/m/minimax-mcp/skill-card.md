## Description:

MiniMax MCP helps agents run web searches, analyze images, and extract URL content through the MiniMax API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangusers](https://clawhub.ai/user/tangusers)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to add MiniMax-backed web search, URL content extraction, and image understanding to MCP-capable coding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and runtime guidance can execute mutable third-party MCP package code or installer scripts.

Mitigation: Prefer a pinned, reviewed minimax-coding-plan-mcp package version and avoid curl-piped shell installers.

Risk: MiniMax API keys may be exposed through shell history or shared MCP configuration.

Mitigation: Use a dedicated minimally scoped MiniMax API key and keep credentials out of shell history and shared config files.

Risk: Search, image analysis, and URL extraction can send sensitive content to MiniMax services.

Mitigation: Do not submit confidential images, screenshots, internal URLs, or regulated data unless MiniMax processing is approved for that data.

## Reference(s):

- [MiniMax MCP Usage Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/tangusers/skills/minimax-mcp)
- [MiniMax Platform (China)](https://platform.minimaxi.com)
- [MiniMax Platform (Global)](https://www.minimax.io)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples; MCP tool calls return structured search results or image-analysis text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uvx plus MINIMAX_API_KEY and MINIMAX_API_HOST; MiniMax API usage may incur fees.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
