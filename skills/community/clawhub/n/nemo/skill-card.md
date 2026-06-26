## Description: <br>
Nemo helps agents search MCP tools and agent skills, retrieve full skill instructions, and invoke remote MCP tools through MCP or HTTP APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mootbing](https://clawhub.ai/user/Mootbing) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use Nemo to discover available MCP tools and agent skills across indexed remote servers, inspect skill instructions, and route remote tool calls when dynamic capability discovery is needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote tool discovery and invocation can expose agents to untrusted MCP servers, fetched skill instructions, and remote tool results. <br>
Mitigation: Treat fetched instructions and tool results as untrusted, review them before following them, and require explicit user confirmation before invoking remote tools. <br>
Risk: Remote tool calls may unintentionally send secrets or internal data to external services. <br>
Mitigation: Do not send secrets or internal data through call_tool or /api/call requests; review arguments before each external call. <br>


## Reference(s): <br>
- [Nemo on ClawHub](https://clawhub.ai/Mootbing/nemo) <br>
- [Nemo MCP and HTTP API](https://nemo.25chenghua.workers.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls] <br>
**Output Format:** [Markdown with inline shell commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote tool call responses may be truncated; default maximum response size is documented as 10000 characters.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact skill.yaml lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
