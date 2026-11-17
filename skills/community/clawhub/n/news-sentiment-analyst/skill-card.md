## Description:

Aggregate and classify financial news sentiment into Risk-On / Risk-Off signals for market and individual stocks using the Finskills API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[finskills](https://clawhub.ai/user/finskills)

### License/Terms of Use:

MIT-0

## Use Case:

Investors, analysts, and market-focused agents use this skill to retrieve financial news, classify market and ticker sentiment, identify catalysts, and produce concise market sentiment reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested tickers, symbols, sectors, or market-news topics may be sent to Finskills when retrieving news.

Mitigation: Avoid using proprietary watchlists or confidential trading research unless sharing that information with Finskills is acceptable.

Risk: Financial news latency and AI-assisted sentiment classification may produce incomplete or incorrect market signals.

Mitigation: Verify high-impact news with primary sources such as company investor relations pages, official filings, or original publisher reports before acting on the report.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/finskills/skills/news-sentiment-analyst)
- [Publisher profile](https://clawhub.ai/user/finskills)
- [Project homepage](https://github.com/finskills/news-sentiment-analyst)
- [Finskills API](https://finskills.net)
- [Finskills registration](https://finskills.net/register)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured Markdown market sentiment report with summaries, catalyst lists, sector maps, and stock-specific news sections.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FINSKILLS_API_KEY. General financial news is available on the free plan; latest and symbol-specific news may require a Pro plan.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
