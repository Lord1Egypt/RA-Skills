## Description: <br>
Track wallet portfolios and transaction history across 88+ blockchains. Monitor holdings, analyze trades, and follow whale wallets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flotapponnier](https://clawhub.ai/user/flotapponnier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query Mobula wallet analytics for cross-chain portfolio holdings, transaction history, and whale wallet monitoring. It is suited for read-only wallet analysis and portfolio review workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet addresses queried through the skill are sent to Mobula and may reveal interest in those wallets. <br>
Mitigation: Query only wallets you are comfortable sending to Mobula, and avoid addresses that you need to keep private or unlinkable. <br>
Risk: The skill requires a Mobula API key that could be exposed through shell history, logs, or agent transcripts. <br>
Mitigation: Use a rotatable API key, store it in environment or secret management, and avoid printing it in logs. <br>
Risk: Ongoing monitoring or alert workflows may depend on a mutable install source or changing API behavior. <br>
Mitigation: Prefer a pinned or versioned install source before enabling continuous monitoring or alerts. <br>


## Reference(s): <br>
- [Mobula homepage](https://mobula.io) <br>
- [Mobula API documentation](https://docs.mobula.io) <br>
- [Mobula supported blockchains](https://docs.mobula.io/blockchains) <br>
- [ClawHub skill page](https://clawhub.ai/flotapponnier/mobula-wallet) <br>
- [Publisher profile](https://clawhub.ai/user/flotapponnier) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and API request details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the MOBULA_API_KEY environment variable and returns read-only wallet portfolio and transaction analysis.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
