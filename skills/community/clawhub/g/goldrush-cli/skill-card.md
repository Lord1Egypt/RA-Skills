## Description:

GoldRush CLI helps agents and developers query blockchain wallets, markets, gas prices, and streaming DEX or wallet activity from the terminal and through MCP integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gane5h](https://clawhub.ai/user/gane5h)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run GoldRush CLI commands for ad hoc blockchain lookups, wallet monitoring, market discovery, trading intelligence, and MCP setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an unpinned remote npm package.

Mitigation: Review the GoldRush CLI package and use a pinned version before running npx commands.

Risk: Authentication stores a GoldRush API key in the operating system keychain.

Mitigation: Run goldrush auth only when keychain storage is acceptable for the user's environment.

Risk: MCP installation can persistently modify Claude tool configuration.

Mitigation: Run goldrush install only after understanding which MCP configuration it changes and how to remove it.

## Reference(s):

- [Goldrush CLI on ClawHub](https://clawhub.ai/gane5h/skills/goldrush-cli)
- [Overview](artifact/references/overview.md)
- [Model Context Protocol](https://modelcontextprotocol.io/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include terminal command examples and MCP setup guidance.]

## Skill Version(s):

3.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
