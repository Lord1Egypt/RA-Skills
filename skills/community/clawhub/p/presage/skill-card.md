## Description: <br>
Connect to Presage prediction market terminal on Solana (powered by Kalshi). Analyze live markets, find trading opportunities, and get AI-powered insights on YES/NO outcomes for sports, crypto, politics, and more. Use when you want market analysis, opportunity discovery, or portfolio tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Seenfinity](https://clawhub.ai/user/Seenfinity) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to analyze live Presage prediction markets, inspect market detail, find possible pricing opportunities, and review portfolio data for a provided agent ID. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts presage.market for market and portfolio data. <br>
Mitigation: Install and use it only when that external network access is acceptable for the deployment environment. <br>
Risk: Agent IDs and returned portfolio or trade-history data may be sensitive. <br>
Mitigation: Treat agent IDs and returned portfolio data as sensitive and avoid sharing them beyond the intended agent workflow. <br>
Risk: The bundled API reference documents register and trade endpoints even though the implemented skill behavior is read-only. <br>
Mitigation: Do not use trading or registration endpoints unless they are separately verified as intended, authorized, and gated by explicit user approval. <br>


## Reference(s): <br>
- [Presage API Reference](references/api-docs.md) <br>
- [Presage Market](https://presage.market) <br>
- [Presage API](https://presage.market/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/Seenfinity/presage) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [JSON-like analysis objects and Markdown guidance with JavaScript and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Market and portfolio outputs depend on live responses from presage.market.] <br>

## Skill Version(s): <br>
1.3.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
