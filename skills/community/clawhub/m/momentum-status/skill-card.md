## Description: <br>
Current momentum engine status across BTC, ETH, SOL, and AVAX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading agents use this skill to check whether APEX Runner's real-time momentum engine is active for BTC, ETH, SOL, and AVAX before momentum-based entries or multi-coin alignment checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an EVM wallet private key for paid x402 requests. <br>
Mitigation: Use a dedicated low-balance Base wallet, keep the private key out of logs and shared environments, and rotate it if exposure is suspected. <br>
Risk: Each invocation may authorize the disclosed per-call charge. <br>
Mitigation: Review the pricing endpoint and wallet activity before automated or repeated use. <br>
Risk: Trading signals can be misread or treated as guarantees. <br>
Mitigation: Use the returned momentum status as one input in a broader trading workflow and review decisions before execution. <br>


## Reference(s): <br>
- [Momentum Status on ClawHub](https://clawhub.ai/kynto2001-ctrl/skills/momentum-status) <br>
- [Publisher profile](https://clawhub.ai/user/kynto2001-ctrl) <br>
- [Momentum Status signal endpoint](https://apexrunner.ai/signals/momentum-status) <br>
- [APEX Runner](https://apexrunner.ai) <br>
- [Signal pricing](https://apexrunner.ai/signals/my-pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Markdown with Python and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill describes an x402-authenticated GET request and a JSON status response for BTC, ETH, SOL, and AVAX.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
