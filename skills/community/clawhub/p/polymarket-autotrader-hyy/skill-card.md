## Description: <br>
Auto-trade BTC, ETH, SOL, XRP on Polymarket price prediction markets at 5-minute and 15-minute intervals using RSI, MACD, and EMA signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hyy2099](https://clawhub.ai/user/hyy2099) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to run a Node.js trading agent that monitors short-term crypto price signals and places Polymarket YES/NO orders for BTC, ETH, SOL, and XRP markets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run unattended with wallet credentials and place repeated live trades. <br>
Mitigation: Use a dedicated low-balance wallet, start with DRY_RUN=true, keep MAX_TRADE_USDC small, and confirm how to stop the scheduler or pm2 service before enabling live trading. <br>
Risk: Each trading cycle can charge billing through SkillPay. <br>
Mitigation: Monitor SkillPay charges and balances while the scheduler is active. <br>
Risk: Runtime dependencies are declared with ranged versions. <br>
Mitigation: Pin dependencies before running the skill in a live trading environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hyy2099/polymarket-autotrader-hyy) <br>
- [Polymarket](https://polymarket.com) <br>
- [Polymarket CLOB](https://clob.polymarket.com) <br>
- [Binance Public API](https://api.binance.com/api/v3) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [SkillPay](https://skillpay.me) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and console output from Node.js scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run recurring trading cycles, place live Polymarket orders, and emit payment links or order results.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
