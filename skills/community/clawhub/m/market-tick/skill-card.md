## Description:

Paid x402 endpoint: $0.014 USDC per call on Base. Returns BTC, ETH and SOL prices, market regime, Fear & Greed, and a momentum label.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers can use the endpoint to retrieve a compact BTC, ETH, and SOL market snapshot with regime, sentiment, and momentum indicators for monitoring or as an input to an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented x402 flow signs paid requests using an EVM wallet and each request incurs a USDC charge.

Mitigation: Protect EVM_PRIVATE_KEY, set a per-request spending cap, and confirm the current price before repeated polling.

Risk: Market snapshots and derived indicators may be incomplete or unsuitable as the sole basis for automated trading decisions.

Mitigation: Check response availability and timestamp, and validate signals against independent sources before acting on them.

## Reference(s):

- [Market Tick endpoint](https://apexrunner.ai/signals/market-tick)
- [BTC Price Tick](https://apexrunner.ai/signals/btc-price-tick)
- [APEX Pulse](https://apexrunner.ai/signals/apex-pulse)
- [Volume Analysis](https://apexrunner.ai/signals/volume-analysis)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Code]

**Output Format:** [JSON market snapshot from the endpoint, with a Python request example in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A request returns one compact snapshot; the endpoint may return HTTP 503 when an input is unavailable.]

## Skill Version(s):

1.0.4 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
