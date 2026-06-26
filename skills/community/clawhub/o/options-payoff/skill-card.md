## Description: <br>
Generate an interactive options payoff curve chart with dynamic parameter controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[himself65](https://clawhub.ai/user/himself65) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to turn described or screenshot-based options positions into interactive payoff and theoretical P&L visualizations with adjustable pricing assumptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated payoff charts may rely on defaulted or misread strikes, premiums, expiry, spot price, volatility, or broker screenshot details. <br>
Mitigation: Review extracted inputs and generated chart assumptions before relying on the visualization for trading or risk decisions. <br>
Risk: Broker screenshots can contain sensitive account or position information. <br>
Mitigation: Avoid sharing unnecessary account details and review screenshots for sensitive data before using them with the skill. <br>


## Reference(s): <br>
- [Options Payoff on ClawHub](https://clawhub.ai/himself65/options-payoff) <br>
- [Options Strategy Payoff Formulas](references/strategies.md) <br>
- [Black-Scholes JavaScript Implementation](references/bs_code.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, code, guidance] <br>
**Output Format:** [Markdown response with an interactive HTML widget and embedded JavaScript] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include chart controls for strikes, premium, quantity, multiplier, implied volatility, days to expiry, risk-free rate, and spot price.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
