## Description:

Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aabbcc456aa](https://clawhub.ai/user/aabbcc456aa)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to plan, build, review, and evaluate MCP servers for external APIs or services in TypeScript or Python.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The evaluation harness can expose credentials or sensitive MCP tool data in prompts, command-line arguments, environment values, HTTP headers, or generated reports.

Mitigation: Run evaluations in an isolated virtual environment or container, use narrowly scoped test credentials, avoid real secrets in command-line arguments, and review report paths before running against sensitive servers.

Risk: Dependency installation and MCP server evaluation commands execute in the user's development environment.

Mitigation: Pin dependencies before use and run the evaluator only against reviewed, non-production, non-destructive MCP servers unless the environment and report output are isolated.

## Reference(s):

- [MCP Server Best Practices](reference/mcp_best_practices.md)
- [Node/TypeScript MCP Server Implementation Guide](reference/node_mcp_server.md)
- [Python MCP Server Implementation Guide](reference/python_mcp_server.md)
- [MCP Server Evaluation Guide](reference/evaluation.md)
- [MCP specification sitemap](https://modelcontextprotocol.io/sitemap.xml)
- [MCP draft specification](https://modelcontextprotocol.io/specification/draft.md)
- [MCP TypeScript SDK README](https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md)
- [MCP Python SDK README](https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with code blocks and optional XML evaluation files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP server implementation guidance, evaluation questions, connection commands, and review feedback.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
