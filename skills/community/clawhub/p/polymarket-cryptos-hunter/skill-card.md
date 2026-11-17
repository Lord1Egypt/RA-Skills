## Description:

HFT Market Making bot for Polymarket. Live execution via Web3 and CLOB API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thony32](https://clawhub.ai/user/thony32)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to start a continuous Polymarket market-making bot for cryptocurrency up/down markets. The bot reads wallet balance on Polygon, posts live CLOB orders, manages open positions, and records local trade audit data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts live real-money trading with broad wallet authority.

Mitigation: Use only an isolated wallet funded with money you are prepared to lose, and require explicit confirmation before allowing live trading.

Risk: The documented command runs the bot indefinitely in the background, reducing visibility into active orders and losses.

Mitigation: Run it in the foreground first, set hard runtime and exposure limits, and confirm how to cancel all open orders before starting.

Risk: Wallet and Polymarket API secrets are required for operation.

Mitigation: Avoid project-local secrets and use narrowly scoped credentials where available.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown instructions with bash commands and Python runtime behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a long-running live trading process, terminal status output, log files, and a local SQLite audit database.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
