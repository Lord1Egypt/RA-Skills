## Description:

Compara y cotiza seguros en España y explica coberturas con IAseguro.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iaseguro](https://clawhub.ai/user/iaseguro)

### License/Terms of Use:

MIT-0

## Use Case:

People in Spain use this skill to compare prices and coverage for supported personal insurance lines, and to understand returned offers. It does not arrange purchases or payments.

### Deployment Geography for Use:

Spain

## Known Risks and Mitigations:

Risk: Quotation requests may send personal details to IAseguro without the user first being told what will be shared; the security review is incomplete.

Mitigation: Check IAseguro’s privacy notice, explain the specific quote fields that will be sent and why, and get the user’s confirmation before sending them.

## Reference(s):

- [IAseguro agent documentation and privacy information](https://iaseguro.com/agentes)
- [IAseguro agent MCP service](https://mcp.iaseguro.com/mcp/agentes)
- [IAseguro OpenAPI documentation](https://mcp.iaseguro.com/openapi.json)
- [ClawHub release page](https://clawhub.ai/iaseguro/skills/iaseguro-seguros-espana)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Spanish conversational text or Markdown with returned prices, coverage details, and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offers are reported with their returned price type (firm, estimated, or unavailable); no purchase or payment is completed.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
