## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns mean-reversion opportunity scan across RANGING and CHOPPY regimes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and crypto trading agents use this paid endpoint to identify potential oversold or overbought opportunities in RANGING or CHOPPY market regimes before considering mean-reversion entries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The request flow uses an EVM wallet private key and authorizes a paid USDC request.

Mitigation: Keep EVM_PRIVATE_KEY secret, review the payment terms and configured spending cap, and use a wallet funded only for intended requests.

## Reference(s):

- [Mean-reversion scan endpoint](https://apexrunner.ai/signals/mean-reversion-scan)
- [APEX Runner](https://apexrunner.ai)
- [Related signal: bb-analysis](https://apexrunner.ai/signals/bb-analysis)
- [Related signal: regime](https://apexrunner.ai/signals/regime)
- [Related signal: liquidation-magnet](https://apexrunner.ai/signals/liquidation-magnet)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Code, Guidance]

**Output Format:** [JSON scan response with Markdown instructions and an inline Python request example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One paid endpoint request returns an opportunity signal and market indicators, such as coin, RSI, and signal type.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
