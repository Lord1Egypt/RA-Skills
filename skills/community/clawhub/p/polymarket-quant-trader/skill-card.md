## Description:

Professional-grade Polymarket prediction market trading system with Kelly Criterion position sizing, expected-value analysis, Bayesian probability updates, Brier-score strategy optimization, and cross-platform arbitrage detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[henry6262](https://clawhub.ai/user/henry6262)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and traders use this skill to build or review Polymarket prediction-market workflows for EV signal scoring, Kelly-sized positions, Brier-score strategy iteration, and cross-platform arbitrage checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users toward unaudited external bot code and dependencies.

Mitigation: Audit the separate bot repository and dependencies before running npm install or executing workflows.

Risk: Live trading setup can involve wallet private keys and exchange API keys.

Mitigation: Use a dedicated low-balance wallet, avoid storing raw private keys in the repository, and restrict exchange API key permissions.

Risk: Automated trading workflows or strategy changes can create financial exposure.

Mitigation: Keep DRY_RUN enabled until verified, apply risk limits, and manually review every live trade or strategy change.

Risk: Cross-platform arbitrage signals may depend on loose title matching, stale prices, or one-sided execution.

Mitigation: Manually confirm event matches and live prices on both platforms, and do not treat detected spreads as risk-free arbitrage.

## Reference(s):

- [Kelly Criterion Deep Dive for Prediction Markets](references/kelly-criterion-guide.md)
- [Brier Score: Measuring Prediction Calibration](references/brier-score-explained.md)
- [Cross-Platform Arbitrage: Polymarket x 1WIN](references/arb-mechanics.md)
- [Polymarket Gamma API](https://gamma-api.polymarket.com)
- [Polymarket CLOB API](https://clob.polymarket.com)
- [ClawHub Skill Page](https://clawhub.ai/henry6262/skills/polymarket-quant-trader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with TypeScript examples, shell commands, and environment configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference external bot code, market APIs, wallet configuration, and dry-run or live-trading modes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
