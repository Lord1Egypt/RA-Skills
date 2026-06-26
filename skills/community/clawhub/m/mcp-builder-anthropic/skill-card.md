## Description: <br>
Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pupuking723](https://clawhub.ai/user/pupuking723) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, implement, review, test, and evaluate MCP servers for external APIs or services in TypeScript or Python. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Guidance and examples may be copied into production MCP servers without enough hardening around credentials, reports, or network exposure. <br>
Mitigation: Review, test, and scan generated or copied server code before deployment; pin dependencies and harden examples for the target environment. <br>
Risk: The optional evaluation harness can connect to MCP servers and send prompts, tool outputs, and reports through an Anthropic model workflow. <br>
Mitigation: Run evaluations only against trusted, read-only test MCP servers with narrowly scoped test tokens, and inspect generated reports for private data before sharing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pupuking723/mcp-builder-anthropic) <br>
- [MCP Best Practices](reference/mcp_best_practices.md) <br>
- [TypeScript Implementation Guide](reference/node_mcp_server.md) <br>
- [Python Implementation Guide](reference/python_mcp_server.md) <br>
- [MCP Server Evaluation Guide](reference/evaluation.md) <br>
- [MCP Protocol Sitemap](https://modelcontextprotocol.io/sitemap.xml) <br>
- [MCP Draft Specification](https://modelcontextprotocol.io/specification/draft.md) <br>
- [TypeScript MCP SDK README](https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md) <br>
- [Python MCP SDK README](https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with code and shell command examples; optional XML evaluation files and Markdown evaluation reports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP server design recommendations, implementation checklists, tool schema guidance, and evaluation outputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
