## Description: <br>
Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ImBeasting](https://clawhub.ai/user/ImBeasting) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, implement, review, test, and evaluate MCP servers for external API or service integrations in Python or Node/TypeScript. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional evaluator can expose tool results to Anthropic and saved reports. <br>
Mitigation: Use staging or sample data where possible, avoid production secrets or personal data, and review evaluator outputs before saving or sharing reports. <br>
Risk: Generated or copied tool examples can include destructive actions if adapted without review. <br>
Mitigation: Review generated tools for destructive behavior and add path, command, and permission safeguards before deployment. <br>


## Reference(s): <br>
- [MCP Protocol Documentation](https://modelcontextprotocol.io/llms-full.txt) <br>
- [MCP Best Practices](reference/mcp_best_practices.md) <br>
- [Python MCP Server Implementation Guide](reference/python_mcp_server.md) <br>
- [TypeScript MCP Server Implementation Guide](reference/node_mcp_server.md) <br>
- [MCP Server Evaluation Guide](reference/evaluation.md) <br>
- [Model Context Protocol Python SDK](https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md) <br>
- [Model Context Protocol TypeScript SDK](https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with code examples, shell commands, configuration snippets, and XML evaluation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce implementation plans, MCP server scaffolding guidance, tool schemas, test commands, and evaluation artifacts.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
