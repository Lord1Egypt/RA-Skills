## Description: <br>
Get real-time exchange rates and currency conversion using free public ExchangeRate-API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alone86136](https://clawhub.ai/user/alone86136) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and end users use this skill to fetch current exchange rates, convert amounts between currencies, and list supported currency codes through a public exchange-rate API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Currency lookup requests are sent to open.er-api.com. <br>
Mitigation: Use the skill only when external exchange-rate lookup is acceptable for the task. <br>
Risk: The scripts require Python 3 and the requests package. <br>
Mitigation: Confirm the runtime has Python 3 and requests installed before invoking the scripts. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/alone86136/open-exchange-rate) <br>
- [ExchangeRate-API public latest rates endpoint](https://open.er-api.com/v6/latest/USD) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command output with exchange rates, conversion results, or currency-code lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and the requests package; sends currency lookup requests to open.er-api.com.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
