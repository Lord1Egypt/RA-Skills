## Description: <br>
MCP Server Pack provides managed MCP server connection details and OpenClaw configuration for filesystem, memory, GitHub, PostgreSQL, web search, and RSS servers, with cloud-hosted and self-hosted options. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neroagent](https://clawhub.ai/user/neroagent) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to list supported MCP servers and generate OpenClaw MCP configuration for cloud-hosted, self-hosted, or hybrid setups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated MCP configurations can expose filesystem, credential, database, cloud, or persistent storage access if too many servers are enabled or permissions are broad. <br>
Mitigation: Enable only the servers needed for the task, avoid default-all configurations, restrict filesystem mounts to narrow paths, and use least-privilege credentials. <br>
Risk: Self-hosted operation may run Docker images, binaries, or npm packages whose supply chain and permissions need review. <br>
Mitigation: Pin and verify Docker images or npm packages before use, review generated commands, and scan artifacts before deployment. <br>
Risk: Cloud-hosted servers may send sensitive data through a hosted provider. <br>
Mitigation: Use self-hosted deployment for sensitive workloads unless the provider is trusted, and avoid sending secrets or regulated data through the cloud option. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/neroagent/mcp-server-pack) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include selected-server configuration and placeholder environment variables such as GITHUB_TOKEN.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
