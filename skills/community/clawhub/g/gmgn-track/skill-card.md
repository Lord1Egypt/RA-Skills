## Description:

Gets real-time crypto buy/sell activity from Smart Money wallets, KOL influencer wallets, and personally followed wallets through the GMGN API, including wallet-followed token queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmgnai](https://clawhub.ai/user/gmgnai)

### License/Terms of Use:

MIT-0

## Use Case:

Crypto analysts, traders, and agent operators use this skill to inspect GMGN wallet-tracking feeds, followed-token lists, KOL activity, and Smart Money activity across Solana, BSC, Base, and Ethereum. It supports concise signal analysis for wallet monitoring and token research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow can persist GMGN API keys and private signing keys in local configuration.

Mitigation: Configure secrets outside the agent or through a secret manager, restrict file permissions, and create a private signing key only when the follow-wallet command is required.

Risk: The skill recommends installing a mutable global gmgn-cli package.

Mitigation: Install a verified and pinned gmgn-cli version through a controlled package-management process before enabling the skill.

Risk: follow-wallet output can expose the user's personally followed GMGN wallet list.

Mitigation: Avoid sharing follow-wallet raw output in public channels and review results before forwarding them.

Risk: Wallet-tracking signals can be mistaken for investment advice.

Mitigation: Treat outputs as informational crypto data, verify signals independently, and avoid automated trading decisions based only on this skill's output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gmgnai/skills/gmgn-track)
- [GMGN API key setup](https://gmgn.ai/ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown trade summaries with inline shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include raw JSON command output when explicitly requested; outputs are informational crypto data, not trading advice.]

## Skill Version(s):

1.4.6 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
