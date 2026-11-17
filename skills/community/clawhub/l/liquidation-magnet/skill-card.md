## Description:

Returns price levels with dense liquidation clusters through a paid x402 endpoint on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and trading agents use this skill to identify price zones with dense liquidation clusters and inform stop-loss placement and position sizing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each x402 request authorizes a paid call from a Base wallet, and the example reads its signing key from EVM_PRIVATE_KEY.

Mitigation: Store the private key securely and retain a max_amount payment cap, as shown in the example.

Risk: The security scan covered the Markdown artifact; linked pages were outside its scope.

Mitigation: Review linked services before use and check the endpoint response before relying on it.

## Reference(s):

- [Liquidation Magnet endpoint](https://apexrunner.ai/signals/liquidation-magnet)
- [Liquidation Magnet on ClawHub](https://clawhub.ai/kynto2001-ctrl/skills/liquidation-magnet)
- [Related signal: Liquidation Pressure](https://apexrunner.ai/signals/liquidation-pressure)
- [Related signal: Crowded Trade Detector](https://apexrunner.ai/signals/crowded-trade-detector)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Code]

**Output Format:** [JSON response with liquidation levels, risk, and distance; Python request example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One paid response per call; requires an EVM wallet private key and USDC on Base.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
