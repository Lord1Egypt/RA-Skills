## Description:

Track wallet portfolios and transaction history across 88+ blockchains, monitor holdings, analyze trades, and follow whale wallets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flotapponnier](https://clawhub.ai/user/flotapponnier)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to ask an agent for cross-chain wallet portfolio summaries, transaction history, whale monitoring, and portfolio allocation analysis using the Mobula API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses queried through the skill are sent to Mobula and may reveal the user's interest in those public wallets.

Mitigation: Use the skill only for wallet addresses the user is comfortable sending to Mobula, and avoid querying wallets the user wants to keep private.

Risk: MOBULA_API_KEY is a credential required for API access.

Mitigation: Store the API key securely, avoid exposing it in shared logs or prompts, and rotate it if it may have been disclosed.

Risk: Continuous wallet monitoring or alert automation can repeatedly disclose wallet-interest patterns and amplify mistaken alerts.

Mitigation: Review any alerting or monitoring workflow before enabling it, and confirm thresholds, recipients, and queried wallets.

## Reference(s):

- [Mobula](https://mobula.io)
- [Mobula API Docs](https://docs.mobula.io)
- [Supported Blockchains](https://docs.mobula.io/blockchains)
- [ClawHub Skill Page](https://clawhub.ai/flotapponnier/skills/mobula-wallet)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with wallet portfolio summaries, transaction summaries, and inline shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MOBULA_API_KEY; wallet queries send public wallet identifiers to Mobula's API and may be rate-limited.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
