## Description:

Gives an AI agent a self-custodial wallet on Base and registers witnessed work as Provenance Envelopes through Provian.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longevitymaniac](https://clawhub.ai/user/longevitymaniac)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Agent operators use this skill to create and register an agent-owned Base wallet, optionally link it to a person, record witnessed work, and inspect another agent's public Provian record.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan flags possible exposure of a token-bearing request through redirects and use of a changeable SDK package version.

Mitigation: Use the service only if you trust it to receive the one-time connection token, inspect the downloaded installer before running it, and pin the SDK version when a fixed release is needed.

## Reference(s):

- [Provian Agent Guide](https://provian.ai/agents)
- [Provian Developer Documentation](https://provian.ai/developers)
- [Provian Documentation for Agents](https://provian.ai/llms.txt)
- [Provian MCP Server Descriptor](https://api.provian.ai/.well-known/mcp.json)
- [Provian Hosted MCP Server](https://api.provian.ai/mcp)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration instructions]

**Output Format:** [Markdown with inline shell, PowerShell, and MCP instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers wallet setup, secret handling, witnessed-work records, and public-record verification.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
