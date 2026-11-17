## Description:

Fades strong directional crypto moves on Polymarket 5-minute interval markets after consecutive high-conviction BTC, ETH, or SOL Up/Down intervals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diagnostikon](https://clawhub.ai/user/diagnostikon)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to identify and optionally execute mean-reversion trades on Polymarket crypto interval markets. It defaults to paper trading and requires an explicit live flag before placing real USDC trades.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live execution can place real USDC trades, and the authoritative security summary says the live-trading safeguards and dependency controls do not fully match the authority requested.

Mitigation: Keep the skill in paper mode unless YES/NO trade semantics, pinned and reviewed simmer-sdk dependency, account-wide position limits, volume limits, and spend limits have been verified.

Risk: SIMMER_API_KEY grants trading authority and is identified as a required high-value credential.

Mitigation: Restrict the API key to the smallest practical trading scope, enforce spend limits, and avoid using unrestricted credentials for live execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diagnostikon/skills/polymarket-bundle-crypto-fade-trader)
- [simmer-sdk on PyPI](https://pypi.org/project/simmer-sdk/)
- [simmer-sdk GitHub repository](https://github.com/SpartanLabsXyz/simmer-sdk)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and Python runtime logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May place simulated or live market orders through simmer-sdk depending on execution mode.]

## Skill Version(s):

0.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
