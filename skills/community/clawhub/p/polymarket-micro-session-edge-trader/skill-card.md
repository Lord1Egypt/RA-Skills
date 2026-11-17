## Description:

Trades session-transition mean-reversion in 5-minute crypto "Up or Down" markets on Polymarket, fading directional bursts that occur during US, Asia, and Europe session opens.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run or adapt a Polymarket trading agent that detects session-transition burst patterns in short-interval crypto markets and proposes or places mean-reversion fade trades. It defaults to paper trading and requires an explicit live flag before routing trades to Polymarket.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live trading can place real USDC orders when --live is supplied, and the security summary says live-trading safety controls do not fully match the documented promises.

Mitigation: Review before installing, start in simulation mode, use a low-limit or simulation-only API key, and do not rely on the documented volume, threshold, or open-position limits to cap real exposure.

Risk: The skill depends on the external simmer-sdk package for market discovery and trade execution.

Mitigation: Pin or lock the SDK dependency before deployment and review dependency updates before enabling live trading.

Risk: SIMMER_API_KEY grants trading authority and is treated as a high-value credential by the artifact documentation.

Mitigation: Store the key in a managed secret store, scope it to the minimum required trading authority, and rotate it if exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-micro-session-edge-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Trading actions]

**Output Format:** [Console text with Simmer SDK trade requests and configurable environment variables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SIMMER_API_KEY; default execution uses simulation mode unless --live is supplied.]

## Skill Version(s):

0.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
