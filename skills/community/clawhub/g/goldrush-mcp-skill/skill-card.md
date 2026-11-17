## Description:

Use GoldRush MCP through UXC for multichain wallet balances, transfers, portfolio history, NFT ownership, token approvals, prices, and chain metadata via stdio MCP with injected API-key auth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure and run GoldRush MCP operations through UXC for blockchain wallet, portfolio, NFT, transfer, token approval, price, and chain metadata queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented command runs @covalenthq/goldrush-mcp-server@latest, so future package changes could alter behavior without a skill update.

Mitigation: Use a pinned, reviewed package version or trusted local install before creating the persistent UXC link.

Risk: The GoldRush API key is injected into a child process used by the MCP server.

Mitigation: Use a scoped key where possible, limit exposure, rotate it regularly, and avoid sharing logs or shell history containing secrets.

Risk: The created goldrush-mcp-cli link persists the documented command until it is changed.

Mitigation: Review the linked command during installation and update or remove the link when changing package versions or credential handling.

## Reference(s):

- [GoldRush MCP Server Documentation](https://goldrush.dev/docs/goldrush-mcp-server)
- [Usage Patterns](references/usage-patterns.md)
- [GoldRush MCP Skill on ClawHub](https://clawhub.ai/jolestar/skills/goldrush-mcp-skill)
- [jolestar Publisher Profile](https://clawhub.ai/user/jolestar)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands and JSON-output handling notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agents to inspect operation help first, use stable JSON envelope fields, inject GOLDRUSH_API_KEY into the stdio MCP subprocess, and keep blockchain query scopes narrow.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
