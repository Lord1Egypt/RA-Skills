## Description: <br>
Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aabbcc456aa](https://clawhub.ai/user/aabbcc456aa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, implement, review, and evaluate MCP servers in TypeScript or Python. It provides practical guidance for tool design, protocol usage, testing, and evaluation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional evaluator may include tool inputs, tool outputs, summaries, and feedback in generated reports. <br>
Mitigation: Review generated reports before sharing them and avoid using sensitive, production, or credential-bearing data in evaluations. <br>
Risk: The evaluator connects to MCP servers and may invoke their tools while answering test questions. <br>
Mitigation: Run evaluations only against test or read-only MCP servers with synthetic data and non-destructive evaluation questions. <br>
Risk: The optional Python evaluator depends on external packages and model API access. <br>
Mitigation: Run it in a virtual environment with pinned dependencies and only provide the credentials required for the intended evaluation. <br>


## Reference(s): <br>
- [MCP Best Practices](artifact/reference/mcp_best_practices.md) <br>
- [Python MCP Server Guide](artifact/reference/python_mcp_server.md) <br>
- [Node MCP Server Guide](artifact/reference/node_mcp_server.md) <br>
- [MCP Server Evaluation Guide](artifact/reference/evaluation.md) <br>
- [MCP Protocol Sitemap](https://modelcontextprotocol.io/sitemap.xml) <br>
- [MCP Draft Specification](https://modelcontextprotocol.io/specification/draft.md) <br>
- [TypeScript MCP SDK README](https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md) <br>
- [Python MCP SDK README](https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code blocks, XML examples, and optional Markdown evaluation reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The optional evaluator can connect to stdio, SSE, or streamable HTTP MCP servers and produce a Markdown report.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
