## Description:

Real-time crypto market data, wallet portfolio tracking, and token analytics across 88+ blockchains for token prices, wallet holdings, historical prices, portfolio PnL, whale monitoring, new-token discovery, and oracle-grade pricing with a Mobula API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flotapponnier](https://clawhub.ai/user/flotapponnier)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to retrieve Mobula-powered crypto market data, wallet portfolio analytics, token metadata, recent trades, and transaction history. It also guides agents in setting up portfolio, whale, token discovery, and contextual price monitoring workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried token names, contract addresses, and wallet addresses are sent to Mobula and may reveal user interests or identity-linked wallet activity.

Mitigation: Only query public wallet addresses the user is comfortable sharing, avoid personal wallets when privacy matters, and review Mobula privacy practices before use.

Risk: The required Mobula API key can be exposed through shell history, logs, screenshots, or direct environment-variable printing.

Mitigation: Store MOBULA_API_KEY in a protected secret manager or environment file, use a separate revocable key for testing, rotate keys periodically, and verify only that the variable is set without printing the key.

Risk: Users may mistakenly provide private keys, seed phrases, passwords, or other sensitive credentials while asking for wallet analysis.

Mitigation: Never request or enter private keys, seed phrases, or passwords; this skill only needs public wallet addresses and a Mobula API key.

## Reference(s):

- [Mobula Website](https://mobula.io)
- [Mobula API Documentation](https://docs.mobula.io)
- [Mobula Skill Repository](https://github.com/Flotapponnier/Crypto-date-openclaw)
- [Mobula Skill Page](https://clawhub.ai/flotapponnier/skills/mobula)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Guidance]

**Output Format:** [Markdown or concise text containing crypto market data, wallet analytics, token research, monitoring recommendations, and API setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MOBULA_API_KEY and sends queried token identifiers, contract addresses, and wallet addresses to Mobula.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
