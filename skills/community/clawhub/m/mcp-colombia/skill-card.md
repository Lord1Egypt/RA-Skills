## Description:

MCP Colombia aggregates Colombian commerce, travel, finance, job-search, and identity-verification services through an MCP server for MCP-compatible agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manuelfelipearias](https://clawhub.ai/user/manuelfelipearias)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to connect an MCP-compatible client to Colombian product search, hotel and flight lookup, job listings, financial comparisons, loan simulation, and Soulprint-based identity checks.

### Deployment Geography for Use:

Global, with functional coverage focused on Colombia

## Known Risks and Mitigations:

Risk: The skill installs and runs a mutable remote npm package through npx.

Mitigation: Pin the npm package to a reviewed version, inspect the package before installation, and run it with least privilege.

Risk: Soulprint and job-application workflows may involve identity-linked reputation data and sharing with external validation or job-search services.

Mitigation: Only provide Soulprint tokens, CV links, or job-application data after confirming the privacy and data-sharing implications are acceptable.

Risk: Travel, job, and financial outputs may depend on external live search or scraped public pages.

Mitigation: Verify important prices, rates, listings, and application links with the authoritative provider before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/manuelfelipearias/skills/mcp-colombia)
- [npm package](https://www.npmjs.com/package/mcp-colombia-hub)
- [Soulprint validator endpoint](https://soulprint-node-production.up.railway.app)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown with JSON configuration and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include external service links, Colombian peso values, identity status, reputation details, and MCP tool-call guidance.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
