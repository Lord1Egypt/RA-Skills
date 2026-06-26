## Description: <br>
Matic Trades API — AI toolbox (AI_PICK), Twelve Data (SMART_SEARCH), autonomous charting. Use for stocks, crypto, indicators, charts, news, sentiment. Triggers analyze NVDA, bitcoin RSI, unusual options, chart patterns, Matic, Twelve Data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ortmind](https://clawhub.ai/user/Ortmind) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to ask finance and market-analysis questions through Matic Trades, including stock, crypto, indicator, chart, news, and sentiment requests. The skill routes natural-language prompts to toolbox, data, or autonomous charting API commands and summarizes returned JSON and image links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-analysis prompts are sent to an external Matic Trades service. <br>
Mitigation: Install only when external processing is intended and avoid sending secrets, proprietary trading context, or other sensitive information in prompts. <br>
Risk: A misconfigured API base URL could send prompts and bearer credentials to an unintended host. <br>
Mitigation: Verify MATIC_TRADES_API_BASE before use and keep the default Matic Trades API host unless a trusted deployment requires an override. <br>
Risk: The skill requires a bearer API key for Matic Trades access. <br>
Mitigation: Use a dedicated API key, store it in the agent environment, and do not print or log the key. <br>


## Reference(s): <br>
- [Matic Trades API reference](references/api.md) <br>
- [Matic Trades product site](https://matictrades.com) <br>
- [Matic Trades API base](https://api.matictrades.com/api/v1) <br>
- [ClawHub skill page](https://clawhub.ai/Ortmind/matic-trades) <br>
- [Publisher profile](https://clawhub.ai/user/Ortmind) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries of JSON API responses, with optional image URLs and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided MATIC_API_KEY or MATIC_TRADES_API_KEY and may use MATIC_TRADES_API_BASE to select the intended API host.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
