## Description:

Provides a paid x402 endpoint that recommends an exchange and order type for lower-cost execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use the endpoint to compare supported exchanges and order types when considering execution cost. The skill provides a JSON recommendation and an example x402 client request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each x402 request spends USDC on Base, and the client signs requests using EVM_PRIVATE_KEY.

Mitigation: Use a dedicated wallet funded for intended calls, protect its private key, and set a per-call amount cap at the expected price as shown in the example.

## Reference(s):

- [Optimal Order Routing endpoint](https://apexrunner.ai/signals/optimal-order-routing)
- [Slippage Forecast](https://apexrunner.ai/signals/slippage-forecast)
- [Execution Window Optimizer](https://apexrunner.ai/signals/execution-window-optimizer)
- [Arb Spread](https://apexrunner.ai/signals/arb-spread)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Code, Configuration instructions]

**Output Format:** [JSON recommendation with a Python x402 request example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid per call in USDC on Base; wallet signing uses EVM_PRIVATE_KEY.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
