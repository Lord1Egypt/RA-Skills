## Description: <br>
Routes natural-language blockchain data questions to free on-chain data services and returns structured JSON results for balances, holdings, NFTs, protocol subgraphs, and related queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill to answer wallet, token, NFT, DeFi lending, prediction-market, and protocol subgraph questions without connecting a wallet. It routes requests to free blockchain data services and returns query-ready JSON for follow-up execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: External blockchain-data requests may expose wallet addresses, protocol names, and query details to third-party services. <br>
Mitigation: Avoid sensitive or personally linkable wallet addresses unless needed, and disclose that external services may receive query details. <br>
Risk: The security evidence notes broader agent authority and underspecified network and write instructions. <br>
Mitigation: Require explicit confirmation before save, export, import, modify, package-install, shell, or network diagnostic actions. <br>
Risk: The security verdict is suspicious, so installation carries review risk even though no specific risk findings were reported. <br>
Mitigation: Review the skill behavior and security summary before installing or enabling it in an agent environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/graph-query-tool-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Structured JSON with query_ready parameters, plus concise Markdown guidance when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include route recommendation, rationale, confidence, executable arguments, source data, status codes, logs, cache duration, and free-tier quota information.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
