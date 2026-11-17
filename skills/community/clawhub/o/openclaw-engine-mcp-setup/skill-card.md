## Description:

Enables OpenClaw MCP support and guides agents in adding the engine_mcp_server configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rxjhfmf](https://clawhub.ai/user/rxjhfmf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to enable MCP support, add the engine_mcp_server endpoint, and validate JSON-RPC calls for finance strategy analysis or backtesting workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to trust a third-party MCP endpoint that may receive financial strategy inputs.

Mitigation: Use it only when the endpoint operator is trusted, review what data will be sent, and keep a documented path to disable the server entry.

Risk: The artifact includes a live-looking shared credential in the sample MCP configuration.

Mitigation: Replace the embedded credential with individually provisioned credentials, store them securely, and revoke any shared or exposed credential before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rxjhfmf/skills/openclaw-engine-mcp-setup)
- [engine_mcp_server MCP endpoint](https://mcp.hzyotoy.com/engine/mcp)

## Skill Output:

**Output Type(s):** [configuration, code, shell commands, guidance]

**Output Format:** [Markdown with YAML and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP configuration examples, setup checks, and sample JSON-RPC tool-call payloads.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
