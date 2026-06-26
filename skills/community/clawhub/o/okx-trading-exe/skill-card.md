## Description: <br>
A standardized adapter gateway skill exclusively for OKX exchange to execute trading actions (buy/sell) and query capabilities across OKX Live and Demo environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iceonme](https://clawhub.ai/user/iceonme) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading agents use this skill to query OKX balances, positions, and recent trades, and to submit market or limit orders in OKX demo or live environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live OKX trades using locally stored exchange credentials. <br>
Mitigation: Use OKX demo mode first, manually review every live order before execution, and avoid credentials for accounts holding significant funds. <br>
Risk: Stored OKX credentials could enable unintended account access if over-permissioned or exposed. <br>
Mitigation: Use a restricted OKX API key with withdrawals disabled and IP restrictions enabled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iceonme/okx-trading-exe) <br>
- [OKX](https://www.okx.com) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Text, Shell commands, Guidance] <br>
**Output Format:** [JSON responses and stdout text from command-line execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OKX credentials in environment variables or a .env file; supports demo and live OKX providers.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
