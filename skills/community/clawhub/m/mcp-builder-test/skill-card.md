## Description:

Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uniquevme](https://clawhub.ai/user/uniquevme)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, implement, test, and evaluate MCP servers that connect agents to external APIs or services in TypeScript or Python.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional evaluation harness can send full MCP tool results to Anthropic and copy them into reports.

Mitigation: Run evaluations with test data or narrowly scoped read-only credentials, and review reports before sharing or storing them.

Risk: The optional evaluation harness can call any exposed MCP tool and does not enforce read-only limits itself.

Mitigation: Evaluate only sandboxed or read-only MCP servers, disable destructive tools during evaluation, and scope credentials to the minimum required access.

Risk: The bundled Python requirements are not pinned.

Mitigation: Pin and review dependencies before running the optional scripts.

## Reference(s):

- [MCP Server Best Practices](artifact/reference/mcp_best_practices.md)
- [Node/TypeScript MCP Server Implementation Guide](artifact/reference/node_mcp_server.md)
- [Python MCP Server Implementation Guide](artifact/reference/python_mcp_server.md)
- [MCP Server Evaluation Guide](artifact/reference/evaluation.md)
- [MCP Protocol Sitemap](https://modelcontextprotocol.io/sitemap.xml)
- [MCP Draft Specification](https://modelcontextprotocol.io/specification/draft.md)
- [MCP TypeScript SDK README](https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md)
- [MCP Python SDK README](https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code blocks, shell commands, configuration examples, and XML evaluation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create MCP server source files, tests, and evaluation reports.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
