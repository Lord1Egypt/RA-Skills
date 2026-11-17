## Description:

Trade on Phemex spot, USDT-M futures, and Coin-M futures by checking market data, managing account state, placing or cancelling orders, moving funds, and streaming real-time updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phemex](https://clawhub.ai/user/phemex)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to ask an agent for Phemex market data, account and position checks, order management, leverage changes, transfers, and streaming crypto market updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release asks users to install a mutable global CLI.

Mitigation: Use a pinned, verified phemex-cli version when available and avoid global installs where possible.

Risk: The skill uses financial API credentials and may store them persistently in plaintext configuration.

Mitigation: Prefer environment variables or an OS secret store over ~/.phemexrc, restrict API keys to the minimum permissions needed, disable withdrawals, and consider IP allowlisting.

Risk: Trading commands can place orders, change leverage, transfer funds, or cancel orders.

Mitigation: Require explicit user confirmation for trading actions, explain leverage risk, show current balances or positions before trade suggestions, and use testnet or small limits until the setup is trusted.

## Reference(s):

- [Phemex Cli on ClawHub](https://clawhub.ai/phemex/skills/phemex-cli)
- [Phemex](https://phemex.com)
- [Phemex production API endpoint](https://api.phemex.com)
- [Phemex testnet API endpoint](https://testnet-api.phemex.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The underlying CLI returns JSON for tool calls and may stream JSON events to stdout for WebSocket subscriptions.]

## Skill Version(s):

2.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
