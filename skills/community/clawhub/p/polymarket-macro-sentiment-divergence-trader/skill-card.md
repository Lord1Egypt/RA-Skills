## Description:

Detects macro sentiment divergence across Polymarket prediction markets and trades against the stale side of inconsistent positive and negative sentiment pricing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents can use this skill to scan Polymarket markets for contradictory positive and negative macro sentiment, then produce paper-trading actions by default. Live trading requires an explicit flag and should remain disabled until the identified safeguard gaps are resolved.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live-trading safeguards do not fully match the skill's safety promises.

Mitigation: Use only paper mode until safeguards are fixed; before enabling --live, verify minimum-volume filtering and enforce portfolio caps across open positions and pending orders.

Risk: SIMMER_API_KEY grants trading authority and is a high-value credential.

Mitigation: Restrict the key to the least required permissions, store it only in a managed secret store, and rotate it if exposed.

Risk: The runtime dependency is not pinned in the artifact configuration.

Mitigation: Pin simmer-sdk to an approved version before deployment and re-run release validation after dependency changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-macro-sentiment-divergence-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text with Python execution commands and JSON-backed configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to paper trading; live trading requires SIMMER_API_KEY and the explicit --live flag.]

## Skill Version(s):

0.0.3 (source: server release evidence; artifact metadata version 1.0 and clawhub.json version 0.0.2 differ)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
