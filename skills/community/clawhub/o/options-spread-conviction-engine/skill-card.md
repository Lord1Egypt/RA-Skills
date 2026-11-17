## Description:

Analyzes market data to score vertical and multi-leg options spread strategies using technical indicators, regime detection, volatility forecasting, Kelly position sizing, and walk-forward backtesting.

This skill is for research and development only.

## Publisher:

[adamnaghs](https://clawhub.ai/user/adamnaghs)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and traders can use this skill to evaluate options spread setups, compare conviction scores, and generate risk-aware sizing and backtesting guidance. Outputs are analytical aids only and should be independently reviewed before trading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill emits trading-style action tiers and sizing guidance that may be mistaken for financial advice.

Mitigation: Treat outputs as analytical aids only, independently verify market data and assumptions, and do not use them as sole basis for investment decisions.

Risk: Under-disclosed mock or fallback logic may produce misleading analysis when live data is unavailable.

Mitigation: Review whether fallback data was used before acting on a result and prefer validated live options-chain and volatility inputs.

Risk: The documented setup includes a sudo symlink command and dependencies without a reviewed lockfile.

Mitigation: Avoid privileged symlink installation where possible and install from pinned, reviewed dependencies in an isolated environment.

Risk: Existing pickle-based option-cache files can carry stale or unsafe local state.

Mitigation: Clear or migrate existing .pkl option-cache files before first use and keep cache directories scoped to trusted local data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adamnaghs/skills/options-spread-conviction-engine)
- [README](artifact/README.md)
- [Skill Source Overview](artifact/SKILL.md)
- [Quantitative Scanner Documentation](artifact/QUANT_SCANNER.md)
- [Multi-Leg Strategy Report](artifact/MULTI_LEG_REPORT.md)
- [Code Review Report](artifact/CODE_REVIEW_REPORT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, JSON when requested, Python code examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trading-style action tiers, option strikes, conviction scores, and position sizing guidance; outputs are not financial advice.]

## Skill Version(s):

2.2.1 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
