## Description:

Looks up public MCP Registry, npm package, and observed server records to help assess MCP servers before use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[petshopbros](https://clawhub.ai/user/petshopbros)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use the skill to review recorded MCP Registry declarations, package status, and dated server observations when selecting, installing, connecting to, or troubleshooting an MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dated lookup records may be mistaken for proof that an MCP server is safe or continuously available.

Mitigation: Check observation dates and treat the records as one input; independently assess the server before installing or connecting.

## Reference(s):

- [Lowdown MCP lookup API](https://lowdown-proxy.vercel.app/api/reputation/{target}?ref=clawhub)
- [Lowdown API OpenAPI specification](https://lowdown-proxy.vercel.app/openapi.json)

## Skill Output:

**Output Type(s):** [Guidance, Analysis]

**Output Format:** [Text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes dated public lookup records; observations are not proof of safety or continuous availability.]

## Skill Version(s):

1.2.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
