## Description: <br>
Mobula provides real-time crypto market data, wallet portfolio tracking, and token analytics across 88+ blockchains through authenticated Mobula API queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Flotapponnier](https://clawhub.ai/user/Flotapponnier) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to answer crypto market and wallet intelligence questions, including token prices, historical performance, wallet holdings, portfolio changes, and recent on-chain activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mobula API keys may be exposed if users paste them into chat or commit them into shared files. <br>
Mitigation: Store the key in the MOBULA_API_KEY environment variable, avoid sharing it in prompts or repositories, and rotate or revoke keys from Mobula when needed. <br>
Risk: Wallet queries are sent to Mobula and can reveal interest in a wallet address or its public holdings. <br>
Mitigation: Query only public wallet addresses the user is comfortable sharing, and avoid addresses that should remain private or personally identifying. <br>
Risk: Users may provide private keys, seed phrases, exchange keys, passwords, or other secrets while asking for wallet help. <br>
Mitigation: Reject secret material and request only public wallet addresses, token names, symbols, or contract addresses required for read-only market data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Flotapponnier/mobula) <br>
- [Mobula Website](https://mobula.io) <br>
- [Mobula API Documentation](https://docs.mobula.io) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with concise market summaries and inline shell commands for API key setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public wallet addresses, token identifiers, market metrics, transaction hashes, and Mobula API setup guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
