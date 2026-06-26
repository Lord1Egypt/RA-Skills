## Description: <br>
Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uniquevme](https://clawhub.ai/user/uniquevme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, implement, test, and evaluate MCP servers that integrate external APIs or services through Python or Node/TypeScript tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional evaluator can let an AI call any connected MCP server tool and record sensitive tool data. <br>
Mitigation: Run evaluations only against trusted test servers or read-only credentials, avoid production accounts, and review outputs before sharing. <br>
Risk: Credentials, tool inputs, tool outputs, or evaluation reports may contain sensitive data. <br>
Mitigation: Avoid putting real tokens directly on the command line and add allowlisting or redaction before using the skill with sensitive services. <br>


## Reference(s): <br>
- [MCP Best Practices](artifact/reference/mcp_best_practices.md) <br>
- [Node/TypeScript MCP Server Implementation Guide](artifact/reference/node_mcp_server.md) <br>
- [Python MCP Server Implementation Guide](artifact/reference/python_mcp_server.md) <br>
- [MCP Server Evaluation Guide](artifact/reference/evaluation.md) <br>
- [MCP Protocol Sitemap](https://modelcontextprotocol.io/sitemap.xml) <br>
- [MCP Draft Specification](https://modelcontextprotocol.io/specification/draft.md) <br>
- [MCP TypeScript SDK README](https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md) <br>
- [MCP Python SDK README](https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code blocks, shell commands, and XML examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include evaluator configuration and reports that should be reviewed for sensitive data before sharing.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and user changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
