## Description:

GLM MCP Server Use for OpenClaw. Configure and use the 4 official Z.AI / GLM MCP servers (vision, web search, web reader, zread) with environment-variable API-key auth. Use for endpoint wiring, schema inspection, smoke tests, and troubleshooting MCP calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[conanwhf](https://clawhub.ai/user/conanwhf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to configure, validate, and troubleshoot Z.AI / GLM MCP servers for vision, web search, webpage reading, and repository reading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Z.AI API keys may be exposed or persisted through command-line arguments or generated mcporter configuration.

Mitigation: Use a low-scope key from environment variables, avoid command-line key arguments, protect generated configs, and keep them out of version control.

Risk: The vision server is installed through a mutable npm package invocation.

Mitigation: Prefer a pinned, audited @z_ai/mcp-server version or run the vision server in a sandboxed environment before production use.

Risk: Setup can replace an existing mcporter config when run without keeping the prior file.

Mitigation: Back up existing configuration first, use a dedicated config path, or run setup with the keep option where appropriate.

Risk: Web Reader output can be incomplete when target pages block automated access.

Mitigation: Inspect returned content quality, trust live schema output for tool names and arguments, and use alternate sources when a page returns verification or anti-bot content.

## Reference(s):

- [Official endpoint matrix](references/official-endpoints.md)
- [Test report](references/test-report.md)
- [Z.AI Vision MCP Server documentation](https://docs.z.ai/devpack/mcp/vision-mcp-server)
- [Z.AI Web Search MCP Server documentation](https://docs.z.ai/devpack/mcp/search-mcp-server)
- [Z.AI Web Reader MCP Server documentation](https://docs.z.ai/devpack/mcp/reader-mcp-server)
- [Z.AI Zread MCP Server documentation](https://docs.z.ai/devpack/mcp/zread-mcp-server)
- [ClawHub skill release page](https://clawhub.ai/conanwhf/skills/glm-mcp-server-use)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce mcporter JSON configuration and smoke-test JSON reports when the bundled scripts are run.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
