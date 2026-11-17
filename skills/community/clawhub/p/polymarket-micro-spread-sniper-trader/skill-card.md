## Description:

Scans all Polymarket categories for tight spreads (<= 8%) combined with extreme probabilities (<= 15% or >= 85%), placing many tiny conviction-based micro bets on near-certain outcomes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to scan Polymarket markets for tight-spread extreme-probability signals and place configurable micro trades. It defaults to paper trading, with live trading available only when explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate real-money trading when live mode is enabled.

Mitigation: Run in simulation first and avoid enabling --live until thresholds, market-discovery claims, liquidity checks, and safeguards have been reviewed.

Risk: The security summary says the documented strategy and implemented safeguards do not align well enough for low-risk installation.

Mitigation: Review and control the trading script before installation, and fix the threshold, liquidity, slippage, and flip-flop safeguard issues before live use.

Risk: SIMMER_API_KEY grants trading authority.

Mitigation: Use a dedicated low-limit key that can be revoked quickly.

## Reference(s):

- [Polymarket Micro Spread Sniper Trader on ClawHub](https://clawhub.ai/diagnostikon/skills/polymarket-micro-spread-sniper-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API Calls]

**Output Format:** [Console text logs, environment-variable configuration, and Simmer SDK trade requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY and simmer-sdk; paper trading is the default unless --live is supplied.]

## Skill Version(s):

0.0.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
