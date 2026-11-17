## Description:

LeafEngines provides agricultural intelligence tools for soil analysis, crop recommendations, and TurboQuant capability checks through a remote MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qwarranto](https://clawhub.ai/user/qwarranto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agricultural operators, researchers, and AI agents use this skill to request soil analysis, crop recommendations, and location-based agricultural capability checks. The skill is intended for MCP-compatible clients that can send county FIPS codes and optional paid API credentials to the LeafEngines service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agricultural, location, and farm operational data is routed to a remote LeafEngines service.

Mitigation: Install only when this data sharing is acceptable for the intended workflow and avoid sending sensitive operational details unless required.

Risk: Paid API keys may be stored in local agent or MCP configuration.

Mitigation: Store API keys only in user-private configuration or secret management and avoid world-readable config files.

Risk: Documentation includes broader external setup paths and an unpinned global npm install.

Mitigation: Prefer the declared ClawHub MCP endpoint and review any external installation path before execution.

Risk: A shared test key appears in artifact documentation.

Mitigation: Treat shared test credentials as non-secret evaluation access only and do not rely on them for protected or production workflows.

## Reference(s):

- [LeafEngines API Reference](references/API_REFERENCE.md)
- [LeafEngines ClawHub Listing](https://clawhub.ai/qwarranto/skills/leafengines)
- [LeafEngines MCP Service](https://wzgnxkoeqzvueypwzvyn.supabase.co/functions/v1/mcp-server)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with configuration snippets, shell commands, and remote MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote service calls may require a free-tier header or paid API key; tool inputs center on county FIPS codes.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
