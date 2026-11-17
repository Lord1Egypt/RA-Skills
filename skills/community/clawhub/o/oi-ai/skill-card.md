## Description:

Route Oi requests through MCP for Contexts, Workflows, Skills, Guardrails, Brain, Connections, prompts, resources, sessions, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[carhaix](https://clawhub.ai/user/carhaix)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route Oi-assisted work through the Oi MCP surface for discovery, retrieval, execution, authoring, lifecycle changes, durable memory, connected-provider work, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote Oi-returned instructions can influence tool routing, provider access, publication, memory, or write actions.

Mitigation: Install only when Oi and the organization resources it returns are trusted, and review unexpected tool use, provider data access, publication, memory, and write actions before allowing them.

Risk: The skill can route stateful operations such as drafts, releases, publishing, archival, durable memory, reporting, and connected-provider writes.

Mitigation: Require explicit user confirmation for consequential state changes and external writes, and follow returned Oi confirmation requests exactly.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/carhaix/skills/oi-ai)
- [Oi MCP Authentication for OpenClaw](references/authentication.md)
- [Oi MCP Tools](references/mcp-tools.md)
- [Oi Product Surfaces](references/product-surfaces.md)
- [Oi MCP authentication guide](https://www.oioioi.ai/resources/authentication)
- [OpenClaw MCP CLI](https://docs.openclaw.ai/cli/mcp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, API calls]

**Output Format:** [Markdown with inline command examples and MCP tool-routing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Oi-returned prompts, records, confirmation requests, usage IDs, trace IDs, billing links, and provider action results when supplied by the MCP server.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
