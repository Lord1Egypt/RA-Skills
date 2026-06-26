## Description: <br>
Real-time token prices, market caps, volume, and analytics across 88+ blockchains. Free tier, no credit card required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[flotapponnier](https://clawhub.ai/user/flotapponnier) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for public crypto prices, token market data, historical price trends, recent pool trades, and token metadata from Mobula. It is intended for market-data lookup and analysis, not trading execution or investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a Mobula API key, which could be exposed if printed in logs or saved carelessly. <br>
Mitigation: Use a dedicated Mobula API key, pass it through temporary environment configuration when practical, and avoid logging or committing the key. <br>
Risk: Crypto market data can be misread as trading or investment advice. <br>
Mitigation: Treat returned prices, volume, and analytics as informational only and avoid using the skill to execute trades or make investment decisions without independent review. <br>


## Reference(s): <br>
- [Mobula](https://mobula.io) <br>
- [Mobula API documentation](https://docs.mobula.io) <br>
- [ClawHub skill page](https://clawhub.ai/flotapponnier/mobula-prices) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with market data summaries and occasional inline shell commands for API key setup] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MOBULA_API_KEY for Mobula API access; market data should be treated as informational.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
