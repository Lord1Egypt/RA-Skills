## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns aggregate liquidation pressure score across tracked perpetuals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading agents can monitor aggregate liquidation pressure across tracked perpetual markets as a systemic risk signal or market-stress overlay before entering leveraged positions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An automatically signed request may cost $0.01 per call even though the release summary advertises $0.007; repeated calls can increase total spend.

Mitigation: Review the endpoint's current payment terms and x402 quote before enabling calls. Set a per-call payment cap at or below the amount you approve, monitor call counts and wallet spending, and stop if the quoted amount exceeds your limit.

## Reference(s):

- [Liquidation Pressure endpoint and pricing](https://apexrunner.ai/signals/liquidation-pressure)
- [Liquidation Magnet signal](https://apexrunner.ai/signals/liquidation-magnet)
- [Crowded Trade Detector signal](https://apexrunner.ai/signals/crowded-trade-detector)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance, Code]

**Output Format:** [JSON market-pressure response with Python x402 usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A response may include pressure_score, at_risk_usd, and level.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
