## Description:

Aggregates, classifies, summarizes, and analyzes market news from Chinese financial portals for pre-market briefings, intraday alerts, and end-of-day reviews with sector classification, sentiment tagging, keyword extraction, and importance ranking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaocaixia888](https://clawhub.ai/user/zhaocaixia888)

### License/Terms of Use:

MIT-0

## Use Case:

External users and market analysts use this skill to collect public Chinese financial news, classify it by market sector, and produce concise pre-market, intraday, or end-of-day briefs with source attribution, keywords, sentiment, and importance ranking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market-news summaries may be mistaken for investment advice.

Mitigation: Present outputs as informational summaries and require users to make their own trading or investment decisions.

Risk: Fetched public news pages may be incomplete, stale, or formatted differently than expected.

Mitigation: Include source attribution and timestamps when available, and ask users to request exact source verification for high-impact items.

Risk: Chinese-formatted output may not meet every user's language needs.

Mitigation: Ask users to specify another output language or format when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaocaixia888/skills/market-news-aggregator)
- [Sina Finance](https://finance.sina.com.cn/)
- [Sina Finance Futures](https://finance.sina.com.cn/futures/)
- [EastMoney](https://www.eastmoney.com/)
- [Hexun](https://www.hexun.com/)
- [Jin10](https://www.jin10.com/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown market-news brief with source labels, one-line summaries, keywords, sentiment tags, importance ranking, and sector totals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-formatted output by default; includes timestamps when available and should not be treated as investment advice.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
