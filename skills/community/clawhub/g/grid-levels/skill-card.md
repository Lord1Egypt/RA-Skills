## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns active grid levels, spacing, and next buy/sell prices per pair.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to retrieve current grid levels and next buy/sell prices for manually managing grid inventory or populating reports and dashboards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each request incurs a USDC charge and the documented client signs payment using an EVM private key.

Mitigation: Keep the private key in a secret store, use a wallet funded only with the intended spending balance, and retain the documented maximum-payment policy.

## Reference(s):

- [Grid Levels endpoint](https://apexrunner.ai/signals/grid-levels)
- [Grid Health signal](https://apexrunner.ai/signals/grid-health)
- [Grid Health Score signal](https://apexrunner.ai/signals/grid-health-score)
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/grid-levels)

## Skill Output:

**Output Type(s):** [API data, JSON]

**Output Format:** [JSON response with active grid levels and next buy/sell prices by pair]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One response stream per endpoint call; each call is paid in USDC.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
