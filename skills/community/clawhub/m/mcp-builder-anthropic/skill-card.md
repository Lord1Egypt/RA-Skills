## Description:

Guides developers through planning, implementing, testing, and evaluating Model Context Protocol servers in TypeScript or Python.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pupuking723](https://clawhub.ai/user/pupuking723)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to design MCP servers that expose external APIs and services through clear tools, then review, test, and evaluate those servers with realistic read-only tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The evaluator and copied examples can expose private tool data when run against sensitive MCP servers.

Mitigation: Run evaluations against test or low-sensitivity MCP servers unless read-only tool allowlists and redaction for tool results and errors are in place.

Risk: Copied MCP server examples can lead to insecure deployments without added safeguards.

Mitigation: Review examples before copying them and add authenticated or loopback HTTP configuration, safe path handling, and pinned dependencies before production use.

Risk: Production credentials or private data can be exposed during testing.

Mitigation: Avoid production credentials and private data during evaluation unless the deployment has appropriate access controls and data handling protections.

## Reference(s):

- [MCP Best Practices](artifact/reference/mcp_best_practices.md)
- [TypeScript MCP Server Guide](artifact/reference/node_mcp_server.md)
- [Python MCP Server Guide](artifact/reference/python_mcp_server.md)
- [MCP Server Evaluation Guide](artifact/reference/evaluation.md)
- [Model Context Protocol Sitemap](https://modelcontextprotocol.io/sitemap.xml)
- [Model Context Protocol Draft Specification](https://modelcontextprotocol.io/specification/draft.md)
- [TypeScript SDK README](https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md)
- [Python SDK README](https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, and XML evaluation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP implementation plans, server code examples, tool design guidance, and evaluation artifacts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
