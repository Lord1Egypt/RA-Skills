## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns grid bot health: fill rate, inventory, and level status across pairs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and grid bot operators use the skill to retrieve fill rate, inventory, active-pair, and status data from the paid endpoint when monitoring bot performance or diagnosing poor fill rates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's crypto trading signal purpose may not fit the user's intended use.

Mitigation: Review whether this signal service fits your needs before installing.

Risk: Requests spend USDC through a wallet and the example reads EVM_PRIVATE_KEY to authorize payment.

Mitigation: Protect the wallet key and set a payment cap that matches the amount you intend to spend.

## Reference(s):

- [Grid Health endpoint](https://apexrunner.ai/signals/grid-health)
- [Related signal: Grid Health Score](https://apexrunner.ai/signals/grid-health-score)
- [Related signal: Grid Levels](https://apexrunner.ai/signals/grid-levels)
- [ClawHub release page](https://clawhub.ai/kynto2001-ctrl/skills/grid-health)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [JSON object returned by the endpoint]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes fill rate, inventory, active-pair count, and status fields.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
