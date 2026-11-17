## Description:

Analyze cryptocurrency, stock, and forex trading charts using GPTChart.ai's AI-powered technical analysis engine, with basic and expert modes and account-credit usage tied to GPTCHART_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiasheng98](https://clawhub.ai/user/jiasheng98)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request GPTChart.ai chart analysis for crypto, stock, and forex symbols, including indicator-based, multi-timeframe, custom-prompt, and strategy-based analysis. It helps agents format API calls and present bias, price levels, reasoning, and credits used.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Analysis calls send chart symbols, custom prompts, and strategy IDs to GPTChart.ai and may consume account credits.

Mitigation: Use only an intended GPTCHART_API_KEY, avoid secrets or proprietary trading logic in customPrompt, and report credits used after each analysis.

Risk: Trading analysis can be incomplete or misleading if treated as a standalone investment decision.

Mitigation: Present the returned bias, entry, stop loss, take profit, confirmation price, and reasoning clearly so users can review the analysis before acting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiasheng98/skills/gptchart-analysis)
- [GPTChart.ai](https://gptchart.ai)
- [GPTChart API keys](https://gptchart.ai/account/api-keys)
- [GPTChart pricing plan](https://gptchart.ai/account/pricing-plan)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON and bash snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API request payloads, trading-analysis summaries, formatted price levels, market bias, and credits used.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
