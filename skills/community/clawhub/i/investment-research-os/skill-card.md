## Description:

Investment Research OS coordinates specialized analyst prompts to produce sourced investment research, expectation-gap analysis, valuation scenarios, red-team review, CIO-style decisions, and position-sizing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunhe-8922](https://clawhub.ai/user/sunhe-8922)

### License/Terms of Use:

MIT-0

## Use Case:

External users and investment researchers use this skill to turn a target company or comparison set into a structured investment decision workflow with industry, company, financial, valuation, expectation-gap, red-team, and CIO-style outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate investment ratings, position sizes, stop losses, and other financial recommendations that may be unsuitable or wrong for a user's circumstances.

Mitigation: Treat outputs as research support, not personalized financial advice; require human review before acting on any recommendation.

Risk: Market data, financial metrics, and valuation assumptions may be stale, unavailable, single-sourced, or misread.

Mitigation: Verify cited data independently, prefer cross-checks across independent sources, and preserve the skill's required source URL, coverage period, and verification notes for each data point.

Risk: The artifact references local scripts and data-fetching commands that may save reports or retrieve public market data.

Mitigation: Inspect any referenced workspace scripts before running them and review locally saved research files before sharing or using them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sunhe-8922/skills/investment-research-os)
- [Macrotrends stock charts](https://www.macrotrends.net/stocks/charts/{TICKER}/{slug}/{metric})
- [StockAnalysis forecast data](https://stockanalysis.com/stocks/{TICKER}/forecast/)
- [OpenAlex works API](https://api.openalex.org/works?filter=...)
- [World Bank indicators API](https://api.worldbank.org/v2/country/{code}/indicator/{id})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown research reports with tables, checklists, sourced data annotations, and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Research outputs include source URLs, coverage periods, verification notes, scenario valuations, red-team risks, CIO ratings, and position-sizing guidance.]

## Skill Version(s):

1.2.0 (source: server release metadata; artifact frontmatter reports 1.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
