## Description: <br>
Current position exposure by pair, strategy, and exchange. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading operators use this skill to retrieve real-time APEX Runner position exposure by pair, strategy, and exchange before monitoring portfolios, adding correlated positions, or rebalancing across exchanges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an EVM private key to authorize paid x402 requests that can spend USDC on Base mainnet. <br>
Mitigation: Use a dedicated low-balance wallet and require confirmation before repeated or automated use. <br>


## Reference(s): <br>
- [ClawHub listing: Position Exposure](https://clawhub.ai/kynto2001-ctrl/skills/position-exposure) <br>
- [APEX Runner position exposure endpoint](https://apexrunner.ai/signals/position-exposure) <br>
- [APEX Runner pricing tier check](https://apexrunner.ai/signals/my-pricing) <br>
- [Related signal: portfolio-heat](https://apexrunner.ai/signals/portfolio-heat) <br>
- [Related signal: live-atr-sizing](https://apexrunner.ai/signals/live-atr-sizing) <br>
- [Related signal: agent-stress-index](https://apexrunner.ai/signals/agent-stress-index) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [JSON response with agent-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and can spend USDC on Base mainnet through paid x402 requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
