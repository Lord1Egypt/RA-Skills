## Description:

Helps agents inspect and operate OpenClawCash-managed EVM and Solana wallets, including transfers, swaps, escrow checkout, and Polymarket activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentwalletapi](https://clawhub.ai/user/agentwalletapi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can guide an agent to inspect wallets and balances or perform explicitly authorized transactions, swaps, escrow checkout, and Polymarket actions through OpenClawCash.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Transfers, swaps, and checkout actions can move real funds.

Mitigation: Use scoped API keys, destination whitelists, spending limits, and approval for each write when handling real funds.

Risk: Exposure of the API key or wallet export passphrase could compromise wallet access.

Mitigation: Protect the skill's .env file and any WALLET_EXPORT_PASSPHRASE value.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/agentwalletapi/skills/open-claw-cash)
- [OpenClawCash](https://openclawcash.com)
- [API endpoints](references/api-endpoints.md)
- [Polymarket venue guide](https://openclawcash.com/venues/polymarket)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance and bash commands; wallet API results are JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require confirmation or a previously approved session mode.]

## Skill Version(s):

1.31.0 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
