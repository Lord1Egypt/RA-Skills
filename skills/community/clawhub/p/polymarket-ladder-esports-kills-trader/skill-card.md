## Description:

Trades monotonicity violations in esports Total Kills O/U market ladders on Polymarket, sizing by conviction with violation magnitude scaling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to identify and optionally trade monotonicity breaks across esports Total Kills O/U market ladders on Polymarket. The skill defaults to paper trading and requires explicit live mode for real USDC trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live execution can place real Polymarket trades, and the security review warns that safeguards may not reliably prevent trades in low-liquidity, misgrouped, or stale-context markets.

Mitigation: Run in paper mode first, review candidate trades manually, and use --live only after accepting the live trading risk.

Risk: The skill requires a high-value Simmer API credential for trading authority.

Mitigation: Use a limited Simmer or Polymarket credential, store it securely, and rotate it if exposed.

Risk: The skill depends on simmer-sdk for market discovery and order placement.

Mitigation: Pin and review the SDK version before live deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-ladder-esports-kills-trader)
- [ClawHub publisher profile](https://clawhub.ai/user/diagnostikon)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with command-line usage and configurable environment variables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May place simulated or live trade orders through the Simmer SDK depending on execution mode.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
