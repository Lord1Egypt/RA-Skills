## Description:

Use when publishing or submitting an MCP server to third-party MCP directories and marketplaces including Glama, mcp.so, Smithery, and MCP Market, especially when Codex must use Computer Use, Browser, or Chrome to open websites, fill submission forms, verify listing pages, and stop before final external submission.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zian502](https://clawhub.ai/user/zian502)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to publish MCP servers to third-party directories and marketplaces, fill listing forms, verify resulting listing pages, and stop for human confirmation before final external submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill may run payload-provided CLI commands.

Mitigation: Review every command against the intended MCP server and destination before allowing execution.

Risk: The security review says the skill can use hardcoded account details and steer users toward a paid listing option.

Mitigation: Confirm the account, email, listing tier, and any payment or publication action with the user before proceeding.

Risk: The skill submits data to external third-party platforms.

Mitigation: Use the skill's stop-before-submit behavior to verify destination, account page, and submitted fields before final submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zian502/skills/mcp-third-party-publisher)
- [Glama MCP directory](https://glama.ai/mcp)
- [mcp.so submit page](https://mcp.so/submit)
- [Smithery server publish page](https://smithery.ai/servers/new)
- [MCP Market submit page](https://mcpmarket.com/submit)
- [PatSnap MCP repository](https://github.com/patsnap/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline commands, JSON snippets, and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports platform, status, public URL, page messages, review state, or failure reason; requires human confirmation before final external submission.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
