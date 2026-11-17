## Description:

Detects doji patterns (48-52% probability) in crypto 5-minute interval markets on Polymarket and trades the post-doji breakout in the direction of the pre-doji trend.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading agents use this skill to scan Polymarket crypto interval markets for doji-after-trend breakout setups and place paper or explicitly enabled live trades with configurable risk parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place live Polymarket trades when run with --live.

Mitigation: Run in paper mode first, require an explicit --live invocation for real trades, and use a least-privilege or low-balance API key.

Risk: Automated financial safeguards are reported as under-enforced.

Mitigation: Independently enforce position, volume, spread, and open-position limits before relying on live execution.

Risk: The trading SDK dependency is unpinned.

Mitigation: Pin and review simmer-sdk before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/diagnostikon/skills/polymarket-candle-doji-breakout-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and terminal output from the trading script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; defaults to paper trading unless run with --live.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
