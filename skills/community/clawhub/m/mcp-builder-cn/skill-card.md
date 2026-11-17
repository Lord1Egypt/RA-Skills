## Description:

Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to plan, implement, test, and evaluate MCP servers for external APIs or services in TypeScript or Python.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide an agent to create MCP server projects or run an optional evaluation harness.

Mitigation: Use an isolated development environment and review generated project files and commands before execution.

Risk: Evaluation runs can connect to MCP servers and pass tool outputs through a model client.

Mitigation: Use least-privilege API keys, avoid intentionally destructive tools during evaluation, and redact sensitive tool outputs.

Risk: Dependency installation commands may rely on unpinned package versions.

Mitigation: Pin dependencies or generate a lockfile before relying on the setup commands.

## Reference(s):

- [MCP Server Best Practices](reference/mcp_best_practices.md)
- [Node/TypeScript MCP Server Implementation Guide](reference/node_mcp_server.md)
- [Python MCP Server Implementation Guide](reference/python_mcp_server.md)
- [MCP Server Evaluation Guide](reference/evaluation.md)
- [Model Context Protocol sitemap](https://modelcontextprotocol.io/sitemap.xml)
- [Model Context Protocol draft specification](https://modelcontextprotocol.io/specification/draft.md)
- [Model Context Protocol TypeScript SDK README](https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md)
- [Model Context Protocol Python SDK README](https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, configuration examples, and XML evaluation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also produce evaluation report content when the optional evaluation harness is run.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
