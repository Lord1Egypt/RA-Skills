## Description:

Autonomous BTC-USDC trading bot on Hyperliquid mainnet using multi-timeframe anchored VWAP, market signals, and configured safety limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidm413](https://clawhub.ai/user/davidm413)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading operators use this skill to configure and run an agent-assisted BTC-USDC trading workflow on Hyperliquid mainnet, inspect generated market signals, and trigger the bundled Python trader.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real-money autonomous trades and asks for a wallet private key.

Mitigation: Use testnet or paper trading first, use only a dedicated low-balance wallet key, and never expose a primary private key to the agent environment.

Risk: Security evidence says safety controls and stop mechanisms are under-scoped or not implemented.

Mitigation: Require an independent code and trading-safety audit, an explicit live-trading enable switch, a working kill switch, and exchange-state risk reconciliation before live deployment.

Risk: Unpinned dependencies can change trading behavior or introduce supply-chain risk.

Mitigation: Pin and review dependencies before any deployment involving real funds.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davidm413/skills/hyperliquid-btc-auto-trader)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls]

**Output Format:** [Markdown instructions, environment-variable configuration, Python execution commands, and runtime trading status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate Hyperliquid mainnet trade orders when run with wallet credentials.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact/skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
