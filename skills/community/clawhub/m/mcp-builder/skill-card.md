## Description: <br>
Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan, implement, test, and evaluate MCP servers for external APIs or services in TypeScript or Python. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Evaluation runs can send MCP tool outputs to an external model and save those results in reports. <br>
Mitigation: Use read-only evaluation tasks, connect only to trusted MCP servers, and avoid secrets or highly sensitive business data during evaluation. <br>


## Reference(s): <br>
- [MCP Best Practices](reference/mcp_best_practices.md) <br>
- [Node/TypeScript MCP Server Implementation Guide](reference/node_mcp_server.md) <br>
- [Python MCP Server Implementation Guide](reference/python_mcp_server.md) <br>
- [MCP Server Evaluation Guide](reference/evaluation.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown guidance with code examples, shell commands, and XML evaluation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include generated MCP server structure, tool implementation guidance, and evaluation instructions.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
