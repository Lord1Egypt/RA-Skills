## Description: <br>
Comprehensive grid health score with recommendations for optimisation <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading workflow operators use this skill to request a paid, real-time grid health signal and optimisation recommendations before adjusting grid parameters or preparing performance reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires EVM_PRIVATE_KEY, which can authorize USDC spending on Base mainnet for paid signal calls. <br>
Mitigation: Use a dedicated low-balance wallet, avoid keys with unrelated funds, and verify each paid call before execution. <br>
Risk: Automatic x402 payment authorization may result in paid calls without clear per-call consent controls. <br>
Mitigation: Configure the agent workflow to require explicit user confirmation before each paid request and review the quoted price before proceeding. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kynto2001-ctrl/skills/grid-health-score) <br>
- [APEX Runner Grid Health Score Signal](https://apexrunner.ai/signals/grid-health-score) <br>
- [APEX Runner Pricing Tier Check](https://apexrunner.ai/signals/my-pricing) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Analysis, Guidance] <br>
**Output Format:** [JSON returned from an authenticated signal request, typically summarized by the agent in text or Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns score, grade, and recommendation fields when the paid request succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
