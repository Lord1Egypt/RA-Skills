## Description:

A gold investment analysis skill that helps agents retrieve current gold-market information, summarize technical indicators, review relevant news and fundamentals, and produce structured analysis reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fmouseboy](https://clawhub.ai/user/fmouseboy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to gather gold price, technical indicator, news, and macroeconomic context for market analysis. The skill can support informational investment discussions by producing structured reports with price overview, technical and fundamental factors, and risk notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gold-market search queries are sent to Tavily when live data is requested.

Mitigation: Use the skill only when sharing those queries with Tavily is acceptable, and do not include confidential portfolio, account, or regulated client data in prompts.

Risk: Investment-oriented analysis may be incomplete, outdated, or influenced by the search results returned at runtime.

Mitigation: Treat outputs as informational market analysis, review cited sources, and apply independent financial judgment before making investment decisions.

## Reference(s):

- [Gold Technical Indicators Reference](references/technical-indicators.md)
- [Tavily](https://tavily.com/)
- [Tavily Search API Endpoint](https://api.tavily.com/search)
- [ClawHub Skill Page](https://clawhub.ai/fmouseboy/skills/gold-investment)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown analysis report with source summaries and optional shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TAVILY_API_KEY for live Tavily search.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
