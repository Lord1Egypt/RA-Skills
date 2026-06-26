## Description: <br>
NEPSE stock market analyst for Nepal that helps with stock prices, technical analysis, market alerts, stock screening, watchlists, portfolio tracking, and Nepal investing questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uddin-rajaul](https://clawhub.ai/user/uddin-rajaul) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze Nepal Stock Exchange equities, check prices, manage watchlists, and configure alerts with NEPSE-specific technical and fundamental signals. <br>

### Deployment Geography for Use: <br>
Global, with analysis focused on Nepal Stock Exchange market data. <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot tokens, chat IDs, stock symbols, prices, and alert thresholds may be exposed if credentials are pasted into logged setup flows or broad shell startup files. <br>
Mitigation: Use a dedicated Telegram bot and chat, store credentials in OpenClaw-scoped secret configuration, and avoid storing tokens in ~/.bashrc. <br>
Risk: Watchlists and alert thresholds are stored locally and may reveal investment interests. <br>
Mitigation: Keep the skill data directory private and avoid sharing generated watchlist, alert, or history files. <br>
Risk: Scraped market data may be stale or unavailable, and indicators can be unreliable for stocks with limited trading history or low liquidity. <br>
Mitigation: Confirm data freshness, review the skill's data quality notes, and treat outputs as analysis only rather than trading instructions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/uddin-rajaul/nepse-skill) <br>
- [Publisher profile](https://clawhub.ai/user/uddin-rajaul) <br>
- [Merolagani company detail data source](https://merolagani.com/CompanyDetail.aspx?symbol={symbol}) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with structured market analysis and inline shell commands when setup or alert automation is needed.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes data quality notes, risk disclaimers, optional watchlist and alert state, and optional Telegram alert delivery when configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
