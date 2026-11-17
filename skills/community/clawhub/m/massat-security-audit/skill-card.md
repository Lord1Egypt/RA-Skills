## Description:

Pays for a security audit of an AI agent or MCP server against OWASP Agentic Security ASI01–ASI10 using BlindOracle's public API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[craigmbrown](https://clawhub.ai/user/craigmbrown)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security teams use this skill to request audits of agents or MCP servers and review signed findings before trusting them. The results are self-assessed tooling, not a compliance certification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit calls and other service actions may require payment through x402 or a starter-credit note.

Mitigation: Check the live service prices and review the exact payment quote and target before authorizing a call.

Risk: MASSAT scores are self-assessed tooling and do not establish compliance.

Mitigation: Use the report as an audit aid; obtain an accredited assessor's determination for compliance decisions.

## Reference(s):

- [ClawHub release](https://clawhub.ai/craigmbrown/skills/massat-security-audit)
- [BlindOracle service prices and availability](https://api.craigmbrown.com/v1/services)
- [BlindOracle remote MCP server](https://api.craigmbrown.com/v1/mcp)
- [BlindOracle listings](https://craigmbrown.com/blindoracle/listings/)

## Skill Output:

**Output Type(s):** [Guidance, API calls, Text]

**Output Format:** [Markdown instructions with shell-command and JSON examples; audit findings are returned by the service as a signed report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes audit findings and verification details returned by the service.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata, artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
