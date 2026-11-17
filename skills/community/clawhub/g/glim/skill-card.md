## Description:

Glim is a hosted MCP server that gives agents live external data from Twitter/X, Reddit, web search, page extraction, GitHub, Amazon, and YouTube transcripts through one endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenequm](https://clawhub.ai/user/tenequm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill to connect an MCP client to Glim for live search, retrieval, and page extraction workflows without provisioning separate API keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The headless crypto flow uses unpinned npm commands for wallet setup and payment-enabled MCP configuration.

Mitigation: Prefer OAuth with a prepaid balance where available; if using the x402 path, use a dedicated low-balance wallet, pin and verify x402-proxy, and review the MCP configuration changes before use.

## Reference(s):

- [glim.sh](https://glim.sh)
- [Glim OpenAPI specification](https://glim.sh/openapi.json)
- [ClawHub release page](https://clawhub.ai/tenequm/skills/glim)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command snippets; connected tools return text or structured data from external services.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires access to glim.sh and either OAuth with a prepaid balance or supported per-call payment.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
