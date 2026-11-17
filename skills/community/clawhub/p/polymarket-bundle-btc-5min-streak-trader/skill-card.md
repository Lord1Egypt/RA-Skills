## Description:

Trades BTC "Up or Down" 5-minute Polymarket intervals by detecting streaks of three or more same-direction markets and placing mean-reversion trades on the next interval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading operators use this skill to configure and run a BTC 5-minute interval trading workflow for Polymarket through Simmer. It defaults to paper trading and can place live trades only when explicitly run in live mode.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unintended live trading or larger-than-expected positions could occur because the security evidence reports implementation gaps in safety controls.

Mitigation: Review the skill before installation, run in paper mode first, and only enable live mode after confirming position and volume settings.

Risk: A high-value trading credential could be exposed or reused beyond the intended trading context.

Mitigation: Use a restricted or sandbox trading key when available, scope it only to this workflow, and rotate it if live testing is no longer needed.

Risk: State could carry across paper and live use if the same long-lived Python process is reused.

Mitigation: Start a fresh process when switching between paper and live modes.

Risk: Documented volume or open-position limits may not behave as account-wide protections.

Mitigation: Do not rely on those limits as sole safeguards until the implementation is fixed; monitor account exposure externally when testing live mode.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-bundle-btc-5min-streak-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python command examples and environment-variable configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket trading requires SIMMER_API_KEY and the --live flag.]

## Skill Version(s):

0.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
