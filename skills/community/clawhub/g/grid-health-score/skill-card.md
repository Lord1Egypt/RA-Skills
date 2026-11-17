## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns comprehensive grid health score with recommendations for optimisation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Crypto grid operators and developers use the endpoint to review grid performance, inform parameter changes, and prepare weekly reports. It returns a score, grade, and recommendations based on live market data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The paid request uses an EVM private key to authorize a USDC payment.

Mitigation: Protect the private key in a secret store, use a dedicated wallet funded only for intended calls, and set an explicit maximum payment amount.

Risk: Recommendations could influence changes to a live crypto grid.

Mitigation: Check recommendations against independent strategy and risk limits before changing live parameters.

Risk: ClawScan reports no issues in its completed scan of the single Markdown component, while noting that a benign result is not risk-free.

Mitigation: Review the skill's stated purpose and linked resources before installing.

## Reference(s):

- [Grid Health Score endpoint](https://apexrunner.ai/signals/grid-health-score)
- [Related Grid Health signal](https://apexrunner.ai/signals/grid-health)
- [Related Grid Levels signal](https://apexrunner.ai/signals/grid-levels)
- [ClawHub skill release](https://clawhub.ai/kynto2001-ctrl/skills/grid-health-score)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance]

**Output Format:** [JSON containing a grid health score, grade, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A paid x402 request using USDC on Base mainnet returns the endpoint response.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
