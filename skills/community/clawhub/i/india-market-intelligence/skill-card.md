## Description:

Comprehensive India-focused market intelligence tool that fetches real-time data on NIFTY, SENSEX, global indices, market news, geopolitical events, and provides AI-powered analysis with probability predictions, risk assessment, and trading decision support for the Indian stock market.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sshrungare](https://clawhub.ai/user/sshrungare)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to run terminal-based market intelligence checks for Indian and global markets, including index snapshots, news, geopolitical monitoring, watchlists, sector views, and heuristic risk or technical indicators.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading signals, probabilities, risk scores, position sizing, and BUY/SELL/LONG/SHORT labels may be misleading because they are heuristic commentary.

Mitigation: Treat outputs as informational only, verify market data independently, and consult qualified financial professionals before making investment or trading decisions.

Risk: Market and news results depend on third-party services that may be delayed, unavailable, rate-limited, or incomplete.

Mitigation: Cross-check critical prices, headlines, and exchange data with official or trusted financial sources before acting.

Risk: Runtime dependencies are auto-resolved and unpinned.

Mitigation: Review dependencies and pin or lock versions in controlled environments before deployment.

Risk: The scripts contact third-party market and news services during normal use.

Mitigation: Confirm that the egress destinations, provider terms, and data-handling expectations fit the deployment environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sshrungare/skills/india-market-intelligence)
- [Yahoo Finance RSS](https://finance.yahoo.com/news/rssindex)
- [Moneycontrol RSS](https://www.moneycontrol.com/rss/latestnews.xml)
- [Economic Times RSS](https://economictimes.indiatimes.com/rssfeedstopstories.cms)
- [Business Standard RSS](https://www.business-standard.com/rss/home_page_top_stories.rss)
- [Reuters Business Feed](https://www.reutersagency.com/feed/?taxonomy=best-topics&post_type=best)
- [yfinance Documentation](https://github.com/ranaroussi/yfinance)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown instructions and rich terminal text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local Python scripts that contact third-party market and news services; data availability, latency, and freshness depend on those providers.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
