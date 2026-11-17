## Description:

Post two-sided GTC limit orders on Polymarket CLOB, manage inventory skew, cancel and replace quotes on price drift, and estimate rebate-eligible volume.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simmer](https://clawhub.ai/user/simmer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external trading operators use this skill to configure, dry-run, monitor, and optionally execute a Polymarket CLOB market-making workflow through Simmer-managed market IDs. It is intended for advanced users who can tune market selection, spread, quote size, inventory skew, and live-trading controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket CLOB orders and on-chain trades cannot be recalled.

Mitigation: Start in dry-run mode, use small balances and restricted API keys, and run live mode only after reviewing market IDs, quote sizes, spread, and cancellation behavior.

Risk: Security evidence says safety checks can fail open and create unintended orders or exposure.

Mitigation: Avoid cron or automaton live mode until fail-closed handling is added for inventory, open-order, and market-metadata failures.

Risk: Default strategy parameters are not validated for profitability and can produce losses under real market conditions.

Mitigation: Treat defaults as plumbing tests, paper trade before scaling, and tune position size, spread, market selection, and skew limits conservatively.

Risk: Dependency or credential exposure can increase financial impact.

Mitigation: Pin and review simmer-sdk before use, keep SIMMER_API_KEY scoped to the minimum needed access, and avoid exposing wallet credentials unless required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simmer/skills/polymarket-clob-maker)
- [Publisher profile](https://clawhub.ai/user/simmer)
- [Risk disclaimer](DISCLAIMER.md)
- [Polymarket winners and losers study](simmer-labs/shared-knowledge/research/2026-04-16-polymarket-winners-losers-study.md)
- [Polymarket quant bot and synthetic sell reference](simmer-labs/shared-knowledge/research/2026-04-14-polymarket-quant-bot-copy-trading.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, JSON]

**Output Format:** [Markdown guidance, command-line output, and optional automaton JSON status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and configured MM_MARKETS; live mode can place real GTC orders.]

## Skill Version(s):

0.9.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
