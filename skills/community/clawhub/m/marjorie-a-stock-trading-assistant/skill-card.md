## Description: <br>
Provides Chinese A-share market quotes, index sentiment, sector heat, technical and fundamental analysis, trading strategy suggestions, and price alert support using public finance data sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marjoriebroad](https://clawhub.ai/user/marjoriebroad) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve and summarize China A-share market data, analyze individual stocks and market conditions, identify hot sectors, and draft risk-labeled trading strategy suggestions. It is intended as an analysis helper, not as personalized investment advice or a guarantee of trading outcomes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading suggestions may be incorrect, stale, or unsuitable for a specific user's financial situation. <br>
Mitigation: Present outputs as analysis support only, include risk notes with price or position suggestions, and require users to verify decisions with qualified financial sources. <br>
Risk: The skill fetches public market data from third-party finance sites that may be unavailable, delayed, or inconsistent. <br>
Mitigation: Show the data source and fetch time in responses and cross-check important figures before relying on them. <br>
Risk: Price alert or watchlist details may be saved locally when users configure alerts. <br>
Mitigation: Avoid storing sensitive personal financial details and review local watchlist contents before sharing or publishing the workspace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marjoriebroad/marjorie-a-stock-trading-assistant) <br>
- [Analysis Method Reference](references/analysis.md) <br>
- [Data Source API Reference](references/data-sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style analysis with optional shell command usage and JSON-formatted market data from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should include data source and fetch time, use concise tables or bullets, and attach risk notes to price or position suggestions.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
