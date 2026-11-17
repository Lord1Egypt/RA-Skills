## Description:

Trades CS2 BO3 Winner markets when individual map winner probabilities imply a different BO3 outcome on Polymarket.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to monitor Polymarket CS2 best-of-three and map winner markets, compare BO3 prices against map-implied probabilities, and place simulated or explicitly live trades through Simmer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live mode can place real Polymarket trades, and the security review warns that some documented volume and concurrent-position safeguards are not fully enforced by the code.

Mitigation: Use paper mode by default, review the implementation before live use, and only run with --live after accepting the remaining trading-control risk.

Risk: The skill requires SIMMER_API_KEY, which grants trading authority.

Mitigation: Use a narrowly scoped key, protect it as a high-value credential, and rotate it if exposure is suspected.

Risk: The skill depends on simmer-sdk for market access and trade execution.

Mitigation: Pin or otherwise verify the SDK dependency before installing or running the skill in live environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-bundle-cs2-maps-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, API calls]

**Output Format:** [Console text, Python execution, and Simmer trading requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading unless the live flag is supplied.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
