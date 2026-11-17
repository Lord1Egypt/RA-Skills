## Description:

Trades distribution-sum violations in F1 championship winner markets on Polymarket by identifying when driver winner probabilities collectively drift above or below about 100%.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and trading-system developers use this skill to monitor Polymarket F1 championship winner markets and place paper or explicitly enabled live trades when distribution-sum violations exceed configured thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real Polymarket orders when run with --live.

Mitigation: Keep live runs manual, use constrained credentials where available, and confirm all tunables before enabling --live.

Risk: Documented volume and concurrent-position limits may not be fully enforced by the implementation.

Mitigation: Do not rely on those limits without code review and live-environment testing; set external account or venue-level limits where possible.

Risk: The skill depends on simmer-sdk for market access and trading behavior.

Mitigation: Pin and review simmer-sdk before use, and retest after dependency updates.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-ladder-f1-championship-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk on GitHub](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API calls, Trading orders]

**Output Format:** [Console text and Simmer SDK trade requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live Polymarket orders require an explicit --live flag and a SIMMER_API_KEY.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
