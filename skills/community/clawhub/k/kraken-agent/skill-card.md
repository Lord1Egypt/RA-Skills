## Description:

Discover and use the official Kraken CLI — an AI-native trading tool for crypto, stocks, forex, and derivatives. Use when the user explicitly asks about Kraken specifically: setting up a Kraken trading agent, Kraken paper trading, Kraken market data, or connecting to the Kraken API via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and users use this skill to set up Kraken's CLI and MCP integration, inspect market data, and work through paper trading or explicitly approved live trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated commands and live orders can affect a funded Kraken account; API keys can allow real trades that lose money.

Mitigation: Start with paper trading and the market,paper MCP scope, keep approval prompts enabled, limit API key permissions, and explicitly approve each live trade.

Risk: The external CLI binary and release-specific safeguards were outside the artifact review.

Mitigation: Check the relevant upstream documentation and safeguards before using authenticated functionality.

## Reference(s):

- [Kraken CLI repository](https://github.com/krakenfx/kraken-cli)
- [Kraken CLI installation instructions](https://github.com/krakenfx/kraken-cli#installation)
- [Kraken](https://www.kraken.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with shell command examples and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can return structured JSON when invoked with -o json.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
