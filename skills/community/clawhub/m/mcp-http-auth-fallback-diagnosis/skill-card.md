## Description:

Diagnose MCP HTTP 401/405 fallback errors by isolating credentials, transport, and runtime interpolation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextaltair](https://clawhub.ai/user/nextaltair)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to troubleshoot HTTP MCP authentication failures, especially when credential drift, fallback/SSE errors, or runtime environment interpolation may be involved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credentials or bearer tokens could be exposed through logs, prompts, or persisted client configuration during troubleshooting.

Mitigation: Capture only HTTP status and protocol response, avoid printing credential values, keep secrets out of persisted config, and verify logs and config files do not contain full tokens.

Risk: Running authentication tests against servers without permission could create unauthorized access attempts.

Mitigation: Run the diagnostic workflow only against MCP servers and credentials the operator is authorized to use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nextaltair/skills/mcp-http-auth-fallback-diagnosis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill should report HTTP status, protocol response, and client verification results without exposing credential values.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
