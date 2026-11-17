## Description:

Helps configure and use the Groundmail MCP server to send and manage email, domains, templates, webhooks, and deliverability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[groundmail](https://clawhub.ai/user/groundmail)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to connect an agent to Groundmail and manage email operations, sending domains, templates, webhooks, and deliverability. It also guides setup through hosted OAuth or a local API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious because it references an unpinned npm package that could change between launches; some scan evidence is incomplete.

Mitigation: Assess trust in the package publisher and use a reviewed, pinned version; account for the scan's incomplete evidence when reviewing the release.

## Reference(s):

- [Groundmail MCP documentation](https://docs.groundmail.dev/ai/mcp)
- [Groundmail agent skills](https://docs.groundmail.dev/ai/agent-skills)
- [Hosted Groundmail MCP server](https://mcp.groundmail.dev/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Text]

**Output Format:** [Markdown instructions, shell commands, JSON configuration, and MCP tool requests and results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool results depend on the requested email or account operation.]

## Skill Version(s):

1.0.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
