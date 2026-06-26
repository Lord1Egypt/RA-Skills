## Description: <br>
Query Kraken crypto account balances, portfolio, trades, staking positions, and market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheSethRose](https://clawhub.ai/user/TheSethRose) <br>

### License/Terms of Use: <br>


## Use Case: <br>
ClawHub users with Kraken accounts use this skill to check portfolio value, holdings, staking rewards, trade history, ledger entries, deposit methods, and Kraken market data through command-line API queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Kraken account data and API credentials. <br>
Mitigation: Use a least-privilege Kraken API key, avoid trading and withdrawal permissions, protect any .env file, and keep credentials out of chat, logs, and version control. <br>
Risk: Raw account-history and deposit-address commands can display sensitive financial or wallet information. <br>
Mitigation: Run those commands only when you intentionally need that data, and review outputs before sharing or storing them. <br>
Risk: Manual portfolio calculations can double-count Kraken Earn allocations. <br>
Mitigation: Use the summary or net-worth commands for totals, or count main wallet equity plus bonded Earn allocations only. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheSethRose/kraken) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command output and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads Kraken API credentials from environment variables or a local .env file when private account commands are run.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
