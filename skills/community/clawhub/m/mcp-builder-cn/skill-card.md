## Description: <br>
Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, implement, test, and evaluate MCP servers that expose external APIs or services through well-designed tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Evaluation runs can expose prompts, tool outputs, headers, environment variables, or API credentials to connected MCP servers and the model provider. <br>
Mitigation: Run evaluations only against trusted test servers, use read-only questions, pass least-privilege tokens, and avoid logging raw user queries or sensitive responses. <br>
Risk: Guidance-generated MCP tools may perform unintended write or destructive operations if tool annotations and evaluation questions are not reviewed. <br>
Mitigation: Review tool schemas, annotations, and tests before deployment; keep evaluations non-destructive and idempotent. <br>
Risk: Collecting long-lived API keys conversationally can leak credentials into transcripts or logs. <br>
Mitigation: Use OAuth, managed secrets, or environment variables for credentials instead of asking users to paste long-lived keys into chat. <br>


## Reference(s): <br>
- [MCP Server Best Practices](reference/mcp_best_practices.md) <br>
- [Node/TypeScript MCP Server Implementation Guide](reference/node_mcp_server.md) <br>
- [Python MCP Server Implementation Guide](reference/python_mcp_server.md) <br>
- [MCP Server Evaluation Guide](reference/evaluation.md) <br>
- [MCP Protocol Sitemap](https://modelcontextprotocol.io/sitemap.xml) <br>
- [MCP Draft Specification](https://modelcontextprotocol.io/specification/draft.md) <br>
- [MCP TypeScript SDK README](https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md) <br>
- [MCP Python SDK README](https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code blocks, shell commands, and XML evaluation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes optional Python evaluation scripts for testing MCP servers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
