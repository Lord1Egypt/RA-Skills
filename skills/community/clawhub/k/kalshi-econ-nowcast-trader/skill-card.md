## Description:

Trades CPI bin markets on Kalshi using the Cleveland Fed CPI Nowcast to compute fair bin probabilities via a normal distribution model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to analyze Kalshi CPI bin markets with a Cleveland Fed CPI nowcast model and, when explicitly enabled, place bounded trades through Simmer/DFlow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use high-value trading credentials and a Solana private key for real-money trading.

Mitigation: Use a dedicated low-balance trading account or wallet, rotate credentials after testing, and avoid sharing production credentials with this skill.

Risk: Live-trading safeguards are not consistently fail-closed.

Mitigation: Keep the skill in dry-run mode until market selection, nowcast freshness, slippage limits, and fail-closed behavior are reviewed and controlled.

Risk: Trading decisions depend on nowcast values and market parsing that may be stale or incorrect.

Mitigation: Verify the current nowcast source, selected CPI markets, and configured risk limits before enabling live trading.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/skills/kalshi-econ-nowcast-trader)
- [Cleveland Fed Inflation Nowcasting](https://www.clevelandfed.org/indicators-and-data/inflation-nowcasting)
- [Simmer Markets Skills](https://simmer.markets/skills)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk Repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON automaton status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dry-run by default; live trading only when --live is explicitly passed.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
