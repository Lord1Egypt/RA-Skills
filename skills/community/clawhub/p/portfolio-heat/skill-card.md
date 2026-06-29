## Description: <br>
Provides the current portfolio heat level: normal, elevated, or emergency. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External agents and portfolio risk operators use this skill before adding positions, enforcing portfolio risk limits, or deciding whether to reduce exposure based on APEX Runner's paid live signal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to an EVM wallet private key for paid x402 requests. <br>
Mitigation: Use a dedicated low-balance Base wallet and provide the key only to the agent environment that needs this skill. <br>
Risk: Repeated or automated calls can incur per-call USDC charges. <br>
Mitigation: Set spending controls, monitor wallet activity, and avoid unattended loops unless call volume is bounded. <br>


## Reference(s): <br>
- [ClawHub Portfolio Heat skill page](https://clawhub.ai/kynto2001-ctrl/skills/portfolio-heat) <br>
- [APEX Runner Portfolio Heat signal](https://apexrunner.ai/signals/portfolio-heat) <br>
- [APEX Runner pricing tier check](https://apexrunner.ai/signals/my-pricing) <br>
- [APEX Runner Position Exposure signal](https://apexrunner.ai/signals/position-exposure) <br>
- [APEX Runner Agent Stress Index signal](https://apexrunner.ai/signals/agent-stress-index) <br>
- [APEX Runner Risk Assessment Bundle signal](https://apexrunner.ai/signals/risk-assessment-bundle) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, JSON, Guidance] <br>
**Output Format:** [JSON response that an agent can summarize as text or Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires EVM_PRIVATE_KEY for x402-authenticated paid requests; responses may include heat_level, heat_score, and action.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
