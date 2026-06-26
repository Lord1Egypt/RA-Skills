## Description: <br>
Access personal finance data from Konto, including accounts, transactions, investments, assets, loans, subscriptions, and net worth summaries through authenticated API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[angelstreet](https://clawhub.ai/user/angelstreet) <br>

### License/Terms of Use: <br>


## Use Case: <br>
People using a Konto instance can ask an agent to retrieve specific financial snapshots, such as net worth, account balances, investments, loans, subscriptions, and filtered transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill queries sensitive personal financial data from a Konto service. <br>
Mitigation: Use a least-privilege or read-only personal API key, keep the local Konto environment file private, and ask the agent to fetch only the specific financial fields needed. <br>
Risk: Analytics endpoints can expose broader aggregate data when an analytics-scope key is used. <br>
Mitigation: Avoid analytics scope unless it is required for the task and the Konto publisher and service are trusted. <br>


## Reference(s): <br>
- [Konto API Reference](api.md) <br>
- [Konto API ClawHub Release](https://clawhub.ai/angelstreet/konto-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses authenticated read-only API requests and may return sensitive personal financial data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
