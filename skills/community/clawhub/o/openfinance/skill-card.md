## Description: <br>
Connect bank accounts to AI models using openfinance.sh. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Winxton](https://clawhub.ai/user/Winxton) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to let an agent query connected financial accounts, retrieve transaction data, and run read-only SQL-style transaction analysis through the OpenFinance API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transaction queries and account results can expose sensitive financial information to the OpenFinance API and the active agent session. <br>
Mitigation: Use trusted OpenFinance endpoints, narrow date ranges, limited account scopes, and field filters that return only the data needed for the task. <br>


## Reference(s): <br>
- [OpenFinance](https://openfinance.sh) <br>
- [OpenFinance API](https://api.openfinance.sh) <br>
- [ClawHub skill page](https://clawhub.ai/Winxton/openfinance) <br>
- [Publisher profile](https://clawhub.ai/user/Winxton) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, text] <br>
**Output Format:** [Markdown with inline bash, curl, SQL, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OPENFINANCE_API_KEY; OPENFINANCE_URL is optional.] <br>

## Skill Version(s): <br>
0.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
