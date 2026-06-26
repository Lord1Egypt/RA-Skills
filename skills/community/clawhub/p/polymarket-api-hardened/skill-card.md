## Description: <br>
Query Polymarket prediction markets for market questions, odds, prices, event probabilities, and related Polymarket data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to query live Polymarket prediction market data, search active markets, inspect event groups, and interpret Yes/No prices as implied probabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes live requests to gamma-api.polymarket.com, so excessive or broad queries could create resource-abuse concerns. <br>
Mitigation: Use targeted searches, slugs, or small result limits, and avoid repeated polling or bulk enumeration. <br>
Risk: Saved or redirected market data could leave the local working context unintentionally. <br>
Mitigation: Save files only inside the current working directory when explicitly requested, and do not pipe or send output to external services. <br>
Risk: Market prices and implied probabilities can be misread as betting or investment advice. <br>
Mitigation: Present outputs as informational market data and avoid recommending trades, wagers, or financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/polymarket-api-hardened) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/polymarket-api) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text market summaries or JSON returned from shell command execution.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public API queries with optional result limits; no credentials required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
