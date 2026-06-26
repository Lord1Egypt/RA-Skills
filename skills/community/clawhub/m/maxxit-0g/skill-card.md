## Description: <br>
Maxxit trading powered by 0G decentralized AI compute for portfolio-aware trade decisions and 0G decentralized storage for censorship-resistant alpha listings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhi152003](https://clawhub.ai/user/abhi152003) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading agents use this skill to request market research, portfolio-aware trade decisions, DEX perpetuals execution, copy-trading workflows, and alpha marketplace operations through Maxxit. The included scripts can run predefined technical strategies that fetch Binance market data and route qualifying signals to Maxxit trading endpoints. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can exercise live trading authority using sensitive Maxxit credentials and connected wallet or brokerage permissions. <br>
Mitigation: Install only for intended live trading use, keep credentials limited-purpose, use limited funded wallets or accounts, and verify MAXXIT_API_URL points to the legitimate Maxxit origin. <br>
Risk: Strategy scripts can route automated trading signals without a built-in dry-run mode or hard user-specific risk limits. <br>
Mitigation: Review each strategy before running it, add dry-run and risk-limit controls where needed, and avoid unattended execution until collateral, leverage, venue, and stop-loss behavior are acceptable. <br>
Risk: Additional brokerage or OAuth-style permissions may expand the authority granted to the skill. <br>
Mitigation: Do not connect Zerodha/Kite or other brokerage integrations unless the extra account permissions are understood and acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/abhi152003/maxxit-0g) <br>
- [Maxxit App](https://maxxit.ai) <br>
- [Lazy Trading Setup](https://maxxit.ai/lazy-trading) <br>
- [0G](https://0g.ai) <br>
- [Binance Klines API](https://api.binance.com/api/v3/klines) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, code] <br>
**Output Format:** [Markdown with inline shell commands and JSON API payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute live trading API calls when credentials, wallet permissions, venue, market, and trade parameters are available.] <br>

## Skill Version(s): <br>
0.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
