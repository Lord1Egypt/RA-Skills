## Description: <br>
Recommends the best exchange and order type for minimum-cost crypto execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading agents use this skill to request paid, real-time routing recommendations for choosing an exchange and order type before crypto orders where execution cost matters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic wallet-based x402 requests can spend funds without strong in-skill consent or spend-limit guidance. <br>
Mitigation: Use a dedicated low-balance wallet, confirm the expected per-call cost before use, and avoid exposing a primary trading wallet private key. <br>
Risk: The skill depends on EVM_PRIVATE_KEY for payment authorization. <br>
Mitigation: Store the key only in the agent runtime's secret environment and rotate it if it may have been exposed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kynto2001-ctrl/skills/optimal-order-routing) <br>
- [APEX Runner Optimal Order Routing Signal](https://apexrunner.ai/signals/optimal-order-routing) <br>
- [APEX Runner Slippage Forecast Signal](https://apexrunner.ai/signals/slippage-forecast) <br>
- [APEX Runner Execution Window Optimizer Signal](https://apexrunner.ai/signals/execution-window-optimizer) <br>
- [APEX Runner Arbitrage Spread Signal](https://apexrunner.ai/signals/arb-spread) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown usage guidance with an x402-authenticated GET request and JSON response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for wallet-based x402 payment authorization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
