## Description: <br>
Macro-Driver-Pro provides real-time DXY and US10Y macro-financial data for agent workflows that need market context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[longxrise](https://clawhub.ai/user/longxrise) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to request macro reports with DXY and US10Y signals for automated trading checks, research dashboards, and investment-writing workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated calls can trigger SkillPay billing through a user identifier without clear execution-time controls. <br>
Mitigation: Use per-call approval, budget limits, and loop protection before allowing automated workflows to call the endpoint. <br>
Risk: Requests may include unnecessary personal or account data in the payload. <br>
Mitigation: Send only the minimum required payload data and avoid including extra personal or account details. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/longxrise/macro-driver-pro) <br>
- [OpenAPI schema](https://macro-driver-pro.vercel.app/openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON] <br>
**Output Format:** [JSON API response with macro-financial report content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses depend on current market data and the caller-supplied request payload.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
