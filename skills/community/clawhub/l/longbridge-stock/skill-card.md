## Description: <br>
Real-time stock quotes and account queries for Longbridge users, covering US, Hong Kong, and China stocks, account balance, and positions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weipapa](https://clawhub.ai/user/weipapa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and Longbridge users use this skill to let an agent retrieve stock quotes, account balances, and portfolio positions after Longbridge credentials are configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Longbridge credentials can allow access to brokerage account balances and holdings. <br>
Mitigation: Keep the config outside shared workspaces and repositories, restrict file permissions, and rotate tokens if they are exposed. <br>
Risk: Account balance or position queries can expose sensitive brokerage data more broadly than intended. <br>
Mitigation: Run balance and position queries only after the user explicitly asks for account data. <br>


## Reference(s): <br>
- [Longbridge stock on ClawHub](https://clawhub.ai/weipapa/longbridge-stock) <br>
- [Longbridge Open Platform](https://open.longport.com/) <br>
- [Configuration guide](references/config.md) <br>
- [Stock symbol guide](references/symbols.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance] <br>
**Output Format:** [Markdown tables and command-line text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include sensitive brokerage balances and holdings when account scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
