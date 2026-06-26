## Description: <br>
Polymarket BTC Trader helps agents configure and operate a BTC 5-minute Up/Down trading bot with AI-assisted signals, risk checks, and a local web dashboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[billychoiu](https://clawhub.ai/user/billychoiu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading automation operators use this skill to set up, configure, and monitor a Polymarket BTC 5-minute Up/Down trading bot that combines AI decisions with price-divergence signals. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated trading behavior may place real-money Polymarket orders despite paper-trading language in parts of the artifact. <br>
Mitigation: Review and modify before installation, default to dry-run or paper mode, and require explicit confirmation, position limits, and loss limits before enabling live orders. <br>
Risk: The local dashboard and related web actions are weakly controlled. <br>
Mitigation: Bind the dashboard to localhost, add authentication before remote access, and isolate or remove the Simmer trading panel unless it is intentionally used. <br>
Risk: API keys and wallet credentials used by the bot could be exposed through local configuration or browser-facing code. <br>
Mitigation: Keep secrets out of frontend assets, store credentials only in protected local environment files or a secret manager, and rotate any credentials previously entered into unsafe locations. <br>


## Reference(s): <br>
- [Strategy Details](references/STRATEGY.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/billychoiu/polymarket-btc-trader) <br>
- [Polymarket CLOB API](https://clob.polymarket.com) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [Polymarket Data API](https://data-api.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with shell commands, environment variable configuration, and operational notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to run local scripts, configure API credentials, and inspect dashboard or bot status files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
