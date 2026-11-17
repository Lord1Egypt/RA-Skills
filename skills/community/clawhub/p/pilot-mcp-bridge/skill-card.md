## Description:

MCP server wrapping the Pilot daemon for OpenClaw/Claude Code integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to expose Pilot Protocol daemon operations as MCP tools for Claude Code and OpenClaw workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The example daemon command uses a hard-coded external registry/beacon endpoint.

Mitigation: Use only Pilot infrastructure you trust and replace or avoid the endpoint unless its operator and purpose are known.

Risk: The command templates accept target, port, topic, and message values that could be unsafe if passed through shell interpolation.

Mitigation: Validate MCP inputs and invoke pilotctl through argument arrays or an equivalent non-shell execution path.

Risk: Daemon, listener, gateway, and mapping operations can expose network surfaces or local routes.

Mitigation: Run the daemon with least privilege and avoid exposing listeners or gateway mappings on untrusted networks.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command templates and MCP tool definitions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pilotctl on PATH, a running Pilot daemon, an MCP server framework, and an MCP-compatible client.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
