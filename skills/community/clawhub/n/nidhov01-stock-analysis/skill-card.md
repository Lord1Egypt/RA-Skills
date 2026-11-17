## Description:

Analyzes stocks and cryptocurrencies using Yahoo Finance data, supporting portfolio management, watchlists with alerts, dividend analysis, 8-dimension stock scoring, viral trend detection, and rumor or early-signal detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidhov01](https://clawhub.ai/user/nidhov01)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to analyze stocks and cryptocurrencies, track portfolios and watchlists, review dividend metrics, and scan market, news, and social signals. Outputs are informational and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce stock and cryptocurrency analysis that may be incomplete, stale, or misleading if treated as investment advice.

Mitigation: Use the output for informational review only, verify market data against authoritative sources, and consult a licensed financial advisor before making investment decisions.

Risk: The skill can store local portfolio and watchlist data.

Mitigation: Run it only in workspaces appropriate for private financial data and review the local storage paths before adding portfolio details.

Risk: Optional X/Twitter scanners can use session cookies through the bird CLI.

Mitigation: Avoid enabling those scanners unless bird is pinned or isolated and only the AUTH_TOKEN and CT0 values are provided.

Risk: Feishu daily-review scripts may transmit portfolio or report content outside the local workspace.

Mitigation: Review or remove the Feishu scripts before use, especially when the workspace contains private portfolio data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nidhov01/skills/nidhov01-stock-analysis)
- [Yahoo Finance](https://finance.yahoo.com)
- [CoinGecko](https://coingecko.com)
- [CNN Fear and Greed Index](https://money.cnn.com/data/fear-and-greed/)
- [SEC EDGAR](https://www.sec.gov/edgar)
- [Google News](https://news.google.com)
- [bird CLI](https://github.com/steipete/bird)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text and JSON reports with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local portfolio, watchlist, hot-scan, and rumor-scan JSON files.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 6.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
