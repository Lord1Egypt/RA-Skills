## Description:

Trades mean-reversion on crypto 5-minute interval markets after detecting a single extreme probability pulse (p > 70% or p < 30%) on Polymarket.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading-system operators use this skill to run a configurable micro-position mean-reversion strategy for short-duration Polymarket crypto Up/Down markets. It defaults to simulated trading and can place live trades only when explicitly launched with live mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real-money trades.

Mitigation: Keep the skill in paper mode until reviewed, use live mode only intentionally, and scope SIMMER_API_KEY to the minimum authority needed.

Risk: Documented trading safeguards may not be fully enforced.

Mitigation: Review and test volume filtering, open-position limits, and interval-continuity behavior before allowing live execution.

Risk: Overlapping live instances can duplicate exposure.

Mitigation: Run at most one live instance per account or add external coordination before scheduling repeated execution.

Risk: Unpinned dependencies can change runtime behavior.

Mitigation: Pin and review simmer-sdk and related dependencies before deploying outside a controlled environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-micro-pulse-revert-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, API Calls, Guidance]

**Output Format:** [Console logs, runtime configuration, and simulated or live trade requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; paper trading is the default and live trading requires an explicit --live flag.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
