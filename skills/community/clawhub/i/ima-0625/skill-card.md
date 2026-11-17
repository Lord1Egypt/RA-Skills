## Description:

Analyze stocks and cryptocurrencies using Yahoo Finance data, with portfolio management, watchlist alerts, dividend analysis, eight-dimension stock scoring, hot-trend scanning, and rumor or early-signal detection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate stock, crypto, dividend, portfolio, watchlist, trend, and rumor analyses from market and news sources. It is intended for informational analysis workflows, not as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional X/Twitter scanning can require reusable browser session tokens or broad environment secrets.

Mitigation: Use the scanners without social media when possible, keep tokens out of repos and shared skill directories, avoid Terminal Full Disk Access, and run only with a minimal environment and a trusted pinned bird installation.

Risk: Ticker, portfolio-interest, and watchlist data may be sent to external financial, news, and optional social-media services.

Mitigation: Review the data sources before use, avoid submitting sensitive portfolio interests, and run the skill in an environment appropriate for external network requests.

Risk: Market, news, short-interest, and scanner data can be delayed, incomplete, rate-limited, or keyword-derived.

Mitigation: Treat outputs as informational analysis, confirm material decisions against authoritative sources, and do not rely on the skill as financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/ima-0625)
- [Usage Guide](docs/USAGE.md)
- [Hot Scanner](docs/HOT_SCANNER.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Yahoo Finance](https://finance.yahoo.com)
- [CoinGecko](https://coingecko.com)
- [SEC EDGAR](https://www.sec.gov/edgar)
- [Google News](https://news.google.com)
- [bird CLI](https://github.com/steipete/bird)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Console text reports and optional JSON, with Markdown documentation for commands and setup.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local portfolio, watchlist, and scanner cache JSON files; results depend on external financial, news, and optional social-media services.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 6.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
