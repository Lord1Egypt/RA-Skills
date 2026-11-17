## Description:

Detects logically linked Polymarket markets with incoherent YES-price sums and, by default in simulation, proposes or executes trades to move cheap or rich legs back toward coherence.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bridgeaisocial](https://clawhub.ai/user/bridgeaisocial)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and prediction-market operators use this skill to detect mutually exclusive Polymarket market sets whose YES prices do not sum near one and to run guarded simulation-first arbitrage passes. It is intended for users who can review trading configuration, market-set assumptions, and live execution risk before enabling real-money trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automated live trading can use real financial authority and the evidence security summary says live-trading safeguards are too weak.

Mitigation: Keep the skill in dry-run or paper mode unless the operator intentionally accepts the risk; require explicit live flags, a minimally scoped SIMMER_API_KEY, pinned dependencies, and low MAX_TRADE_USD and DAILY_BUDGET_USD limits.

Risk: Prediction-market execution can lose money through spreads, fees, slippage, illiquidity, adverse selection, or total loss of staked funds.

Mitigation: Review every setting before funding live use, start with small exposure caps, and treat output as trading automation rather than financial advice or performance evidence.

Risk: Configured COHERENCE_GROUPS are trusted as mutually exclusive, and incorrect market grouping can create false arbitrage signals.

Mitigation: Manually verify each configured market set before enabling trades; rely on alert-only behavior for unconfirmed discovered sets.

Risk: Legs are entered one at a time and partial-fill unwind is basic, so non-atomic execution can leave unintended exposure.

Mitigation: Avoid large live positions until enforceable limit-price controls, depth checks, and stronger partial-fill handling are reviewed or added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bridgeaisocial/skills/polymarket-coherence-arb)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown documentation with bash commands, environment configuration, and command-line status or trade-action text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs as a simulation-first trading agent requiring SIMMER_API_KEY; live trading requires explicit CLI flags and configured venue.]

## Skill Version(s):

0.1.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
