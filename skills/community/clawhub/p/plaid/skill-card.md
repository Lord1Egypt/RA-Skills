## Description: <br>
plaid-cli a cli for interacting with the plaid finance platform. link accounts from various institutions, query balances, and transactions by date range listing accounts/balances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jverdi](https://clawhub.ai/user/jverdi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to operate plaid-cli for linking Plaid institutions, checking account balances, and querying transaction history by account or date range. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent access Plaid-linked balances, transactions, and local token data. <br>
Mitigation: Use it only with trusted accounts, protect ~/.plaid-cli, and avoid printing or logging access tokens. <br>
Risk: The skill depends on the external plaid-cli module. <br>
Mitigation: Install only after trusting the external module and its requested Plaid access. <br>
Risk: Cron-style monitoring can repeatedly query financial transaction data. <br>
Mitigation: Enable scheduled monitoring only intentionally and review where state files and command output are stored. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jverdi/plaid) <br>
- [jverdi publisher profile](https://clawhub.ai/user/jverdi) <br>
- [plaid-cli Go module](https://pkg.go.dev/github.com/jverdi/plaid-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide the agent to request Plaid credentials, run plaid-cli, and handle JSON or CSV account and transaction output.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
