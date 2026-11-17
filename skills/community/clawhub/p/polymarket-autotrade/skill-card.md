## Description:

Polymarket prediction market CLI - Browse markets, check prices, execute trades, and manage portfolio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aplanckfish](https://clawhub.ai/user/aplanckfish)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to browse Polymarket prediction markets, inspect market prices, execute USDC buy or sell trades, and review wallet positions and balances through a CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit live Polymarket trades when wallet credentials are configured.

Mitigation: Use a dedicated wallet with limited funds and manually review intended trades outside the skill before execution.

Risk: Wallet private keys and generated API credentials are required for trading and may be stored in local configuration files.

Mitigation: Prefer environment variables where practical, restrict credential-file permissions, and avoid using a main wallet.

Risk: The trading dependency is specified without an upper bound or lockfile in the release evidence.

Mitigation: Treat dependency installation as a supply-chain risk and pin or review dependency versions before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aplanckfish/skills/polymarket-autotrade)
- [Polymarket events API](https://gamma-api.polymarket.com/events/pagination)
- [Polymarket positions API](https://data-api.polymarket.com/positions)
- [Polymarket CLOB API](https://clob.polymarket.com)
- [Polygon RPC endpoint](https://polygon-rpc.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [CLI text and Markdown-style command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, pip, POLYMARKET_PRIVATE_KEY, POLYMARKET_PROXY_ADDRESS, requests, and py-clob-client on Linux or macOS.]

## Skill Version(s):

1.2.3 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
