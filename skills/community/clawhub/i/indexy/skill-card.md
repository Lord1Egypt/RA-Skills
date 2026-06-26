## Description: <br>
Manage, create, update, and analyze custom crypto indices with detailed asset weights, methodologies, and performance metrics via API or Web3 authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hsantana](https://clawhub.ai/user/hsantana) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent builders use this skill to connect agents to Indexy market data and, when authorized, create, update, or analyze cryptocurrency indices. It supports read-only public analytics as well as credentialed index management workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Credentialed API use can create or modify Indexy indices when an API key or Web3 signature is available. <br>
Mitigation: Use a dedicated API key when possible and require explicit user confirmation before create, update, or rebalance actions. <br>
Risk: Credentials could be exposed through logs, chat transcripts, or requests to the wrong domain. <br>
Mitigation: Keep credentials out of logs and chat, use HTTPS, and verify programmatic requests are sent to indexy.co. <br>
Risk: Crypto index data or performance metrics may be misread as investment advice. <br>
Mitigation: Present outputs as market and index analytics, and ask users to confirm methodology, assets, and weights before taking index management actions. <br>


## Reference(s): <br>
- [Indexy API Documentation](https://docs.indexy.xyz/api) <br>
- [CoinGecko Networks API](https://docs.coingecko.com/reference/networks-list) <br>
- [ClawHub Skill Page](https://clawhub.ai/hsantana/indexy) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration instructions] <br>
**Output Format:** [Markdown with HTTP headers, endpoint descriptions, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authentication guidance, request payloads, response interpretation, pagination, rate-limit handling, and confirmation steps for create or update actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and artifact version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
