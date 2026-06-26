## Description: <br>
GLM MCP Server Use for OpenClaw configures and uses the 4 official Z.AI / GLM MCP servers (vision, web search, web reader, zread) with environment-variable API-key auth for endpoint wiring, schema inspection, smoke tests, and troubleshooting MCP calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[conanwhf](https://clawhub.ai/user/conanwhf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding-agent users use this skill to install, configure, inspect, smoke test, and troubleshoot Z.AI/GLM MCP servers for vision, web search, web reading, and repository-reading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup workflow stores a Z.AI API key in generated mcporter configuration for HTTP and local stdio MCP servers. <br>
Mitigation: Use a scoped or test API key where possible, keep generated config files private, and use --masked when checking key availability. <br>
Risk: Running the smoke tests and MCP calls sends search queries, URLs, repository names, screenshots, images, or videos to Z.AI services. <br>
Mitigation: Avoid sending sensitive material unless Z.AI processing is acceptable for the user and deployment context. <br>
Risk: The setup script replaces an existing config file at the selected --config path unless --keep is used. <br>
Mitigation: Point --config at a disposable or dedicated file, or pass --keep when preserving an existing config matters. <br>
Risk: Web Reader output may be incomplete for protected, paywalled, or anti-bot pages. <br>
Mitigation: Inspect returned content quality and validate critical extracted content against the original source. <br>


## Reference(s): <br>
- [GLM MCP Server Use on ClawHub](https://clawhub.ai/conanwhf/glm-mcp-server-use) <br>
- [GLM Official MCP Servers - Endpoint Matrix](references/official-endpoints.md) <br>
- [Test Report](references/test-report.md) <br>
- [Z.AI Vision MCP Server documentation](https://docs.z.ai/devpack/mcp/vision-mcp-server) <br>
- [Z.AI Web Search MCP Server documentation](https://docs.z.ai/devpack/mcp/search-mcp-server) <br>
- [Z.AI Web Reader MCP Server documentation](https://docs.z.ai/devpack/mcp/reader-mcp-server) <br>
- [Z.AI Zread MCP Server documentation](https://docs.z.ai/devpack/mcp/zread-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python helper scripts that can write JSON mcporter configuration and smoke-test reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Z.AI API key supplied through environment variables or an explicit setup argument; smoke tests call external Z.AI MCP services.] <br>

## Skill Version(s): <br>
1.0.2 (source: evidence.json release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
