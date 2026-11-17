## Description:

InvestLog AI helps agents answer US stock research questions with real-time quotes, valuation metrics, financials, analyst ratings, ownership data, technical indicators, dividends, splits, news, and related market data through the InvestLog API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nblicb](https://clawhub.ai/user/nblicb)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to research publicly traded US equities and market activity in English or Chinese. It is suited for stock quote checks, earnings and valuation analysis, ownership research, analyst sentiment review, and market overview queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys passed in URL query strings can be exposed in browser history, server logs, proxy logs, or shared transcripts.

Mitigation: Avoid placing valuable API keys in URLs; prefer an Authorization header when supported and rotate any key that may have been exposed.

Risk: Stock questions are sent to the InvestLog API and may reveal sensitive portfolio interests or personal context.

Mitigation: Avoid including private portfolio details, account data, personal identifiers, or secrets in prompts sent through this skill.

## Reference(s):

- [InvestLog API homepage](https://api.investlog.ai)
- [ClawHub skill page](https://clawhub.ai/nblicb/skills/investlog-ai)
- [Publisher profile](https://clawhub.ai/user/nblicb)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or text summaries based on JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses may include stock tickers, tables, metrics, trends, and query quota information.]

## Skill Version(s):

1.0.2 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
