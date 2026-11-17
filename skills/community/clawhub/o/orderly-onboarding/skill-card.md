## Description:

Agent onboarding for Orderly Network - omnichain perpetual futures infrastructure, MCP server, skills, and developer quickstart

This skill is ready for commercial/non-commercial use.

## Publisher:

[tarnadas](https://clawhub.ai/user/tarnadas)

### License/Terms of Use:


## Use Case:

Developers, builders, aggregators, trading desks, and bot authors use this skill to understand Orderly Network, configure agent tooling, and find the right Orderly SDK, API, MCP, and skill resources for onboarding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends unpinned package execution through npx defaults or @latest.

Mitigation: Pin package versions before running install or MCP setup commands.

Risk: The skill includes broad persistent agent configuration and all-agent global install examples.

Mitigation: Prefer project-local installation, install only the needed Orderly pieces, and review MCP configuration diffs before applying them.

## Reference(s):

- [Orderly Documentation](https://orderly.network/docs)
- [Orderly Tokenomics](https://orderly.network/docs/introduction/tokenomics)
- [Orderly API](https://api.orderly.org)
- [Orderly Testnet API](https://testnet-api.orderly.org)
- [Orderly Chain Info Endpoint](https://api.orderly.org/v1/public/chain_info)
- [Orderly JavaScript SDK](https://github.com/orderlynetwork/js-sdk)
- [Orderly Example DEX](https://github.com/orderlynetwork/example-dex)
- [Orderly MCP Server Package](https://www.npmjs.com/package/@orderly.network/mcp-server)
- [Orderly Skills Package](https://www.npmjs.com/package/@orderly.network/skills)
- [ClawHub Skill Page](https://clawhub.ai/tarnadas/skills/orderly-onboarding)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON/TOML configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes onboarding checklists, package installation commands, MCP setup examples, API endpoints, and links to related Orderly skills and documentation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
