## Description:

Paid x402 endpoint: $0.007 USDC per call on Base. Returns current portfolio heat level: normal, elevated, or emergency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Crypto portfolio agents use this skill before adding positions, enforcing risk limits, or considering exposure reductions. It requests a current portfolio heat level and returns a score and suggested action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each request authorizes a USDC payment from the configured wallet.

Mitigation: Use a dedicated wallet with limited funds, verify the current price, and retain a strict maximum payment policy.

Risk: The client signs payments using the EVM private key supplied through EVM_PRIVATE_KEY.

Mitigation: Use a dedicated key with limited funds, keep it in a protected secret store, and never include it in source files or logs.

## Reference(s):

- [Portfolio Heat endpoint](https://apexrunner.ai/signals/portfolio-heat)
- [ClawHub skill page](https://clawhub.ai/kynto2001-ctrl/skills/portfolio-heat)
- [Agent Stress Index](https://apexrunner.ai/signals/agent-stress-index)
- [Risk Assessment Bundle](https://apexrunner.ai/signals/risk-assessment-bundle)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Code, Guidance]

**Output Format:** [JSON response with a Python request example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The response includes a heat level, score, and suggested action based on current market data.]

## Skill Version(s):

1.0.2 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
