## Description:

Identify institutional stop clusters and max pain zones.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to request liquidity-map and max-pain market signals for a supplied asset ticker. It can return basic market-signal data or a premium-response notice requiring payment proof.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticker queries are sent to an external Zo Computer API.

Mitigation: Install only if users are comfortable sharing ticker queries with that external service.

Risk: Premium responses may present a 402 payment request with a crypto payment prompt.

Mitigation: Review any payment request manually; the artifact does not auto-pay, trade, alter accounts, read local files, or persist data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/market-liquidity-map)
- [Publisher profile](https://clawhub.ai/user/ssidharhubble)
- [Pricing information](https://ssyopros.zo.space/pricing)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [JSON response or payment-required object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a ticker input; premium signals may return a 402 payment-required response.]

## Skill Version(s):

1.1.2 (source: server release metadata; package.json reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
