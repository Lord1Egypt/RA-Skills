## Description: <br>
An investment portfolio tracker that runs entirely locally. All data stays in ~/.portfolio-tracker/. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aigeneralstore](https://clawhub.ai/user/aigeneralstore) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users use this skill to track local investment portfolios, refresh prices, sync read-only account balances from supported financial services, and request portfolio allocation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles financial credentials stored in ~/.portfolio-tracker/config.json. <br>
Mitigation: Use read-only API keys with withdrawals and trading disabled, restrict config file permissions, and avoid use on shared machines. <br>
Risk: The skill makes online calls to financial services, market-data providers, brokerage services, blockchain RPC endpoints, and AI-session contexts. <br>
Mitigation: Install only when those network interactions are acceptable for the portfolio data being processed. <br>
Risk: Account sync can overwrite or remove local portfolio records when reconciling external balances. <br>
Mitigation: Review sync results before relying on the updated portfolio and keep backups of local portfolio data when needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aigeneralstore/portfolio-tracking-skill) <br>
- [Publisher profile](https://clawhub.ai/user/aigeneralstore) <br>
- [Binance API Management](https://www.binance.com/en/my/settings/api-management) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with tables, inline shell commands, JSON-backed local data, and concise portfolio guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local portfolio data and configuration under ~/.portfolio-tracker/.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
