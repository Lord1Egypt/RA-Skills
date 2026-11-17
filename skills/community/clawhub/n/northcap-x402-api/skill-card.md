## Description:

Provides pay-per-call crypto trading signals with entry, stop-loss and take-profit via the x402 standard (USDC on Ethereum). Live DRT/ICT signals for agents and traders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[northcap-group](https://clawhub.ai/user/northcap-group)

### License/Terms of Use:

MIT-0

## Use Case:

External agents, developers, and traders use this skill to discover and call Northcap's paid crypto-signal API, retrieve entry, stop-loss, take-profit, and risk-reward data, and optionally register USDC provider accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid API calls can incur USDC charges.

Mitigation: Require explicit user approval before purchase or signal calls, and confirm price, wallet, chain, and subscription terms before use.

Risk: Crypto trading signals may be wrong or financially harmful.

Mitigation: Treat outputs as informational inputs, require human review before trades, and do not rely on backtests as a guarantee of future performance.

Risk: The skill sends an API key and request data to an external service.

Mitigation: Store X402_API_KEY securely, avoid logging credentials, and restrict network access to the documented Northcap API endpoint.

Risk: Provider registration may expose a public acceptance row tied to a wallet address.

Mitigation: Register providers only when public disclosure is intended and use a wallet address appropriate for that exposure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/northcap-group/skills/northcap-x402-api)
- [Northcap API base URL](https://api.northcapgroup.com)
- [Northcap x402 manifest](https://api.northcapgroup.com/.well-known/x402)
- [Northcap Group publisher profile](https://clawhub.ai/user/northcap-group)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Shell commands, JSON]

**Output Format:** [Markdown guidance with HTTP request examples and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires X402_API_KEY and network access to https://api.northcapgroup.com.]

## Skill Version(s):

1.0.15 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
