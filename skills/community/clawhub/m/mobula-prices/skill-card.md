## Description:

Real-time token prices, market caps, volume, and analytics across 88+ blockchains. Free tier, no credit card required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flotapponnier](https://clawhub.ai/user/flotapponnier)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill with OpenClaw agents to retrieve current and historical crypto market data, compare tokens, inspect token metadata, and review recent pool trades. The skill is read-only and does not execute trades, access wallets, sign transactions, or manage private keys.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mobula receives token lookup queries and the Mobula API key used for requests.

Mitigation: Use the skill only when that data sharing is acceptable, store the API key in a protected environment or secret manager, and rotate the key if it is exposed.

Risk: Recent-trades queries can be incorrect when a token address is supplied where the Mobula endpoint expects a liquidity pool address.

Mitigation: Verify that recent-trades requests use a pool or pair address, and use token metadata or other supported endpoints when the pool address is not known.

## Reference(s):

- [Mobula Homepage](https://mobula.io)
- [Mobula API Documentation](https://docs.mobula.io)
- [Mobula Supported Blockchains](https://docs.mobula.io/blockchains)
- [ClawHub Skill Page](https://clawhub.ai/flotapponnier/skills/mobula-prices)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown market-data summaries with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MOBULA_API_KEY; recent trades queries require a liquidity pool address rather than a token address.]

## Skill Version(s):

1.0.1 (source: server release evidence and artifact version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
