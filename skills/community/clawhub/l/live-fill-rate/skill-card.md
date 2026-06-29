## Description: <br>
Live grid fill rate across all pairs, measuring execution efficiency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading agents use this skill to request real-time grid fill-rate data for monitoring execution efficiency, detecting liquidity degradation, and diagnosing underperforming grids. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires agent access to an EVM private key for x402-authenticated paid requests. <br>
Mitigation: Use a dedicated low-balance wallet and expose EVM_PRIVATE_KEY only in the environment needed for the call. <br>
Risk: Repeated or automated invocations can spend USDC on Base according to the listed per-call price. <br>
Mitigation: Confirm the current price before repeated use, monitor wallet balance, and avoid unattended loops unless spending limits are controlled. <br>


## Reference(s): <br>
- [APEX Runner Live Fill Rate](https://apexrunner.ai/signals/live-fill-rate) <br>
- [APEX Runner Pricing](https://apexrunner.ai/signals/my-pricing) <br>
- [ClawHub Skill Page](https://clawhub.ai/kynto2001-ctrl/skills/live-fill-rate) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown instructions with a Python example; API response is JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY and USDC on Base for paid x402 requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
