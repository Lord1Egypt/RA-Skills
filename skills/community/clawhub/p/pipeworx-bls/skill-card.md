## Description:

Access and search Bureau of Labor Statistics economic data series, fetch historical or latest employment, inflation, wages, productivity, and housing data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to search BLS series and retrieve historical or latest public economic data for employment, inflation, wages, productivity, and housing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: BLS-related queries are sent to an external Pipeworx MCP gateway.

Mitigation: Install only when that data flow is acceptable for the intended workflow.

Risk: Economic analysis based on returned BLS data may be consequential if used for business or policy decisions.

Mitigation: Verify important results against official BLS sources before relying on them.

## Reference(s):

- [Pipeworx bls on ClawHub](https://clawhub.ai/brucegutman/skills/pipeworx-bls)
- [Pipeworx BLS MCP gateway](https://gateway.pipeworx.io/bls/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, API Calls]

**Output Format:** [Text or Markdown responses with BLS series results, plus MCP server configuration as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only access through the disclosed Pipeworx MCP gateway]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
