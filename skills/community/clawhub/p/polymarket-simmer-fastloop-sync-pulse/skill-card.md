## Description:

Trades Polymarket BTC/ETH/SOL 5-minute binary markets using a Triple-Trigger strategy based on Binance momentum, NOFX OI/netflow, L2 wall detection, and cached market IDs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrewbrownrd](https://clawhub.ai/user/andrewbrownrd)

### License/Terms of Use:

MIT-0

## Use Case:

External traders and automation operators use this skill to run or adapt a Polymarket 5-minute market trading script that can operate in paper mode or, with a wallet key, place live trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can automate real-money Polymarket trades when a wallet private key is configured.

Mitigation: Use a dedicated low-balance wallet and omit WALLET_PRIVATE_KEY unless live trading is intended.

Risk: Dependency, secret, and embedded credential controls require review before installation.

Mitigation: Pin and audit simmer-sdk, rotate or remove the embedded NOFX credential, and review credentials before running the skill.

Risk: The daily budget control may not be sufficient as a sole loss-control mechanism.

Mitigation: Require stronger live-trade confirmation and atomic budget enforcement before relying on the daily limit.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/andrewbrownrd/skills/polymarket-simmer-fastloop-sync-pulse)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration values, and console status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local JSON cache, spend, and ledger files during execution.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
