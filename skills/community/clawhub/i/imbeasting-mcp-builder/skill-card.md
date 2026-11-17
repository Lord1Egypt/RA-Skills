## Description:

Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imbeasting](https://clawhub.ai/user/imbeasting)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and engineers use this skill to plan, implement, test, and evaluate MCP servers that expose external APIs or services to LLM agents in Python or TypeScript.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional evaluation harness can send MCP tool results and errors to Anthropic.

Mitigation: Run evaluations in an isolated environment, use only test or low-sensitivity MCP servers and credentials, and review reports before sharing or committing them.

Risk: Remote MCP connections and tool access are not strongly constrained by the skill.

Mitigation: Prefer HTTPS remote URLs, avoid production authorization headers, and restrict credentials to the minimum needed for the evaluation.

## Reference(s):

- [ClawHub mcp-builder skill page](https://clawhub.ai/imbeasting/skills/imbeasting-mcp-builder)
- [MCP Protocol Reference](https://modelcontextprotocol.io/llms-full.txt)
- [MCP Python SDK README](https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md)
- [MCP TypeScript SDK README](https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md)
- [MCP Server Development Best Practices and Guidelines](reference/mcp_best_practices.md)
- [Python MCP Server Implementation Guide](reference/python_mcp_server.md)
- [Node/TypeScript MCP Server Implementation Guide](reference/node_mcp_server.md)
- [MCP Server Evaluation Guide](reference/evaluation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, and example XML.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce implementation plans, MCP server files, evaluation questions, test commands, and Markdown evaluation reports.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
