## Description:

Trades mean reversion on geopolitical Polymarket markets pushed to probability extremes by breaking news, using days-to-resolution to size conviction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to discover geopolitical prediction markets at extreme probabilities and place paper or explicitly enabled live mean-reversion trades with configurable risk thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket trades using SIMMER_API_KEY, and security evidence reports that some promised live-trading safeguards are not actually enforced.

Mitigation: Use paper mode first, enable live mode only deliberately, use limited and rotatable credentials where possible, and confirm trade-size, minimum-volume, and maximum-position controls are enforced before live deployment.

Risk: The skill depends on simmer-sdk for market discovery and trade execution.

Mitigation: Pin or verify the Simmer SDK version before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-geopolitics-sentiment-reversal-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance, API Calls]

**Output Format:** [Markdown guidance, Python execution, and console trade logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket orders require the --live flag and SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
