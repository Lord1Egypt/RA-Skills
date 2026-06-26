## Description: <br>
Professional-grade Polymarket prediction market trading system with Kelly Criterion position sizing, expected-value scoring, Bayesian probability updating, cross-platform arbitrage scanning, and Brier-score strategy optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Henry6262](https://clawhub.ai/user/Henry6262) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to evaluate Polymarket prediction-market opportunities, size positions with quantitative risk controls, scan cross-platform price spreads, and tune trading strategies against calibration metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can support real-money trading and depends on wallet or exchange credentials. <br>
Mitigation: Use a dedicated low-balance wallet, avoid broad API permissions, keep secrets out of chat and logs, and require explicit manual approval before any live trade. <br>
Risk: The trading behavior depends on external bot code and dependencies that are not fully reviewed in the packaged skill evidence. <br>
Mitigation: Independently audit the external bot repository, dependency tree, and live trading controls before installation or deployment. <br>
Risk: Model calibration or Brier-score implementation errors can lead to poor position sizing and trading losses. <br>
Mitigation: Verify the Brier-score implementation, paper trade with DRY_RUN enabled, and enforce strict exposure and stop-loss limits. <br>


## Reference(s): <br>
- [Kelly Criterion Deep Dive for Prediction Markets](references/kelly-criterion-guide.md) <br>
- [Brier Score: Measuring Prediction Calibration](references/brier-score-explained.md) <br>
- [Cross-Platform Arbitrage: Polymarket x 1WIN](references/arb-mechanics.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Henry6262/polymarket-quant-trader) <br>
- [Publisher Profile](https://clawhub.ai/user/Henry6262) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with TypeScript examples, shell commands, and configuration instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require external trading bot code, wallet configuration, market data APIs, and manual approval before live trading.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
