## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns price tick + Fear & Greed + regime in one call.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Agents performing crypto market analysis can make one paid request for a bundled snapshot containing a BTC price tick, Fear & Greed data, and a market regime. Developers need an EVM wallet funded with USDC on Base to make the request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad invocation guidance could lead to unnecessary paid market-signal requests outside market-analysis tasks.

Mitigation: Invoke the endpoint only when a market snapshot is relevant to the task.

Risk: Each request incurs a USDC charge and uses an EVM wallet private key.

Mitigation: Keep the private key out of source code and logs, and set a per-call payment cap no higher than the stated list price.

## Reference(s):

- [Market Pulse Bundle endpoint](https://apexrunner.ai/signals/market-pulse-bundle)
- [Trading Intelligence Bundle](https://apexrunner.ai/signals/trading-intelligence-bundle)
- [Regime signal](https://apexrunner.ai/signals/regime)
- [Fear & Greed signal](https://apexrunner.ai/signals/fear-greed)
- [ClawHub release page](https://clawhub.ai/kynto2001-ctrl/skills/market-pulse-bundle)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Code, Guidance]

**Output Format:** [A JSON market snapshot, with a Python request example in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One bundled response includes a price tick, Fear & Greed data, and market regime.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
