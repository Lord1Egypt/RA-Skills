## Description: <br>
A China A-share market assistant that retrieves real-time quotes, analyzes individual stocks, market sentiment and hot sectors, and provides risk-aware trading strategy and price alert guidance for Shanghai and Shenzhen A-share tickers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[modestyrichards](https://clawhub.ai/user/modestyrichards) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer China A-share quote, stock analysis, market sentiment, hot sector, trading strategy, and price alert questions. It is scoped to Shanghai and Shenzhen A-shares and should be treated as informational market analysis rather than licensed financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce stock analysis and trading strategy guidance that may be mistaken for licensed financial advice or guaranteed outcomes. <br>
Mitigation: Treat outputs as informational only, verify assumptions and market data independently, and avoid relying on the skill as the sole basis for trading decisions. <br>
Risk: Ticker queries are sent to public finance data providers, and alert workflows may store watchlist details locally. <br>
Mitigation: Avoid entering sensitive portfolio information unless necessary and review any locally stored watchlist content before sharing or deployment. <br>
Risk: The skill is scoped to China A-shares and may ignore or mis-handle ambiguous, Hong Kong, US, or other non-A-share tickers. <br>
Mitigation: Confirm ticker market and code prefix before acting on analysis, especially for ambiguous numeric symbols. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/modestyrichards/modesty-a-stock-trading-assistant) <br>
- [Individual Stock Analysis Method Reference](references/analysis.md) <br>
- [Data Source API Reference](references/data-sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown with tables, structured analysis, risk reminders, shell commands, and optional JSON from the stock data script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should cite data source and retrieval time, keep price figures to two decimals, and include risk reminders with trading guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
