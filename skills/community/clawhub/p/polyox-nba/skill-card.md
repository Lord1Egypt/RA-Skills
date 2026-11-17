## Description:

Query the PolyOx API for NBA data, Polymarket predictions, and AI matchup analysis, including a paid x402 analysis endpoint using USDC on Base Sepolia.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jambocoder159](https://clawhub.ai/user/jambocoder159)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to query NBA schedules, teams, players, stats, injuries, Polymarket markets, and paid AI matchup analysis from the PolyOx API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill combines wallet payments with command execution and weak spending safeguards.

Mitigation: Use only testnet or low-value wallets and require explicit checks of amount, recipient, token, network, and maximum spend before any x402 payment.

Risk: Wallet private keys may be exposed in broad agent environments.

Mitigation: Prefer wallet tooling that avoids raw private key handling, and keep any EVM private key scoped to the minimum environment needed for the paid request.

Risk: The artifact recommends running package-manager commands for wallet tooling.

Mitigation: Pin and verify wallet tooling before running npx or npm commands.

## Reference(s):

- [PolyOx API base URL](https://api-hoobs.polyox.io)
- [PolyOx NBA skill page](https://clawhub.ai/jambocoder159/skills/polyox-nba)
- [Coinbase Agentic Wallet quickstart](https://docs.cdp.coinbase.com/agentic-wallet/quickstart)
- [Coinbase Agentic Wallet skills overview](https://docs.cdp.coinbase.com/agentic-wallet/skills/overview)
- [x402 protocol documentation](https://docs.x402.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON, bash, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers JSON API responses, paginated endpoints, curl calls, and x402 wallet payment flows.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
