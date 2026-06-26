## Description: <br>
Identify institutional stop clusters and max pain zones. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssidharhubble](https://clawhub.ai/user/ssidharhubble) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to request market liquidity analysis for an asset ticker, including institutional stop clusters and max pain zones. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts an external service for ticker analysis. <br>
Mitigation: Install only when external API calls for ticker analysis are acceptable for the deployment environment. <br>
Risk: Premium responses may include a cryptocurrency payment request to a fixed wallet address. <br>
Mitigation: Do not send cryptocurrency unless the payment flow, recipient, amount, and refund or support terms are independently verified outside the tool output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ssidharhubble/market-liquidity-map) <br>
- [Premium signal pricing](https://ssyopros.zo.space/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, API Calls, Code, Guidance] <br>
**Output Format:** [JSON response or payment-required error object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a ticker string and calls an external liquidity-analysis API.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
