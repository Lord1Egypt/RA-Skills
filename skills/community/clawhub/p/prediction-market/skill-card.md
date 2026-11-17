## Description:

Helps agents read and participate in Garden Temp Market, a daily Base prediction market for whether the 18:00 UTC garden temperature will be higher than yesterday's.

This skill is ready for commercial/non-commercial use.

## Publisher:

[potdealer](https://clawhub.ai/user/potdealer)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI-agent operators use this skill to inspect GTM market state, build HIGHER or LOWER bet transaction payloads, and produce commands for interacting with the Base contract.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate ready-to-submit Base transaction payloads that spend ETH on prediction-market bets.

Mitigation: Use an explicit spending limit, a dedicated low-value wallet, and human approval for every transaction.

Risk: Examples include raw private-key command patterns that could expose funds if copied into prompts, logs, or shared terminals.

Mitigation: Do not use production private keys; prefer a wallet, hardware signer, or managed keystore that displays chain, contract address, calldata, and ETH value before signing.

Risk: Market settlement depends on a trusted keeper submitting the temperature value.

Mitigation: Treat participation as accepting the keeper trust model and verify the contract, keeper model, and market terms before betting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/potdealer/skills/prediction-market)
- [Publisher profile](https://clawhub.ai/user/potdealer)
- [DailyTempMarket contract on Basescan](https://basescan.org/address/0xA3F09E6792351e95d1fd9d966447504B5668daF6)
- [SensorNet contract on Basescan](https://basescan.org/address/0xf873D168e2cD9bAC70140eDD6Cae704Ed05AdEe0)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON transaction payloads, Guidance]

**Output Format:** [Markdown guidance with shell commands, JavaScript helper output, and JSON transaction payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce ready-to-submit Base transaction payloads; use human approval before any ETH-spending transaction.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
