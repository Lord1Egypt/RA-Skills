## Description: <br>
MidOS is an MCP knowledge operating system for AI agents, with tools for knowledge management, multi-agent orchestration, search, planning, and persistent memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[msruruguay](https://clawhub.ai/user/msruruguay) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to connect agents to a hosted or self-hosted MCP knowledge service for hybrid search, persistent memory, task planning, knowledge quality checks, and operational health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes broad shell, file, git, HTTP, Discord, and webhook actions. <br>
Mitigation: Run it in a sandboxed environment, grant least-privilege access, and require explicit approval before actions that execute commands, modify files, contact external services, or send notifications. <br>
Risk: Persistent memory can retain sensitive, secret, or regulated information. <br>
Mitigation: Avoid storing secrets or regulated data in memory, review memory contents before reuse, and apply retention and access controls appropriate to the deployment. <br>
Risk: The security review flagged unclear safety boundaries around the hosted or self-hosted MCP service. <br>
Mitigation: Audit the service and self-hosted repository before deployment, pin reviewed versions, and rescan the artifact when configuration or code changes. <br>


## Reference(s): <br>
- [MidOS homepage](https://midos.dev) <br>
- [MidOS MCP endpoint](https://midos.dev/mcp) <br>
- [MidOS documentation](https://midos.dev/docs) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance, JSON-RPC examples, and MCP tool call results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on selected MCP tools and may include search results, saved memory, planning updates, health information, file or shell operation results, and notification requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
