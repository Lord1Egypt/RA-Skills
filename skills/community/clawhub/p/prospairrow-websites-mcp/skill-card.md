## Description:

Generate more revenue with high-quality leads by giving an AI agent access to Prospairrow for prospect extraction, enrichment, competitor discovery, and content marketing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[discry](https://clawhub.ai/user/discry)

### License/Terms of Use:


## Use Case:

Sales and go-to-market teams use this skill through an agent to run Prospairrow prospecting workflows, including extracting prospects, enriching company data, scoring fit, finding competitors, and generating positioning or content marketing outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local MCP server can use ambient Prospairrow API credentials without authenticating local callers.

Mitigation: Use a narrowly scoped API key and avoid exposing or relying on the loopback server in environments with untrusted local processes or browser content.

Risk: Write-capable mode can perform Prospairrow actions that modify account data or generate account-affecting outputs.

Mitigation: Start mcp:writes only when write actions are required; otherwise use the read-only runtime mode.

Risk: Optional OpenClaw config API-key fallback can increase credential exposure if enabled unnecessarily.

Mitigation: Keep OpenClaw config API-key fallback disabled unless it is specifically required.

Risk: Some tasks labeled read-only can trigger POST-based processing.

Mitigation: Treat read-only score tasks as potentially account-impacting until they are reclassified or confirmed side-effect-free.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/discry/skills/prospairrow-websites-mcp)
- [Prospairrow Application](https://app.prospairrow.com)
- [API Schema](API_SCHEMA.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [Operations Guide](docs/OPERATIONS.md)
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON-RPC request examples, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the selected Prospairrow task and the configured API key.]

## Skill Version(s):

1.2.5 (source: server release evidence, created 2026-02-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
