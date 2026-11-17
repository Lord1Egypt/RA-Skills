## Description:

Integrate AI agents with business data via Model Context Protocol to query ads, analytics, and CRM data through normalized interfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engsathiago](https://clawhub.ai/user/engsathiago)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to plan MCP servers that connect AI agents to business systems such as databases, REST APIs, ad platforms, analytics tools, and CRM data sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes broad business-data integrations and write-capable tools that could affect customer records, files, or ad budgets.

Mitigation: Use least-privilege credentials, explicit authorization checks, and confirmation gates before writes or budget changes.

Risk: Illustrative file and API examples may be unsafe if copied directly into a production MCP server.

Mitigation: Add path containment, destination allowlists, input validation, and bounded query limits before implementation.

Risk: Business data, credentials, and tool results can be exposed through logs or caches.

Mitigation: Redact sensitive logs and define clear cache expiration, retention, and deletion controls.

## Reference(s):

- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [Official MCP Servers](https://github.com/modelcontextprotocol/servers)
- [Community MCP Servers](https://github.com/punkpeye/awesome-mcp-servers)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline Python, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces implementation guidance and illustrative snippets; examples require review before use with real business systems.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
