## Description:

Korean Exchange (KRX) stock market data CLI. Fetch daily OHLCV, latest-close snapshots, market-cap rankings, index histories (KOSPI/KOSDAQ/KOSPI200/KRX100), and ticker↔name lookups for KOSPI/KOSDAQ/KONEX/ETF tickers. Use when a user asks for Korean stock prices, ticker resolution, or KRX market data in JSON or CSV. No API key required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chloepark85](https://clawhub.ai/user/chloepark85)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent workflows use this skill to resolve Korean stock tickers and retrieve KRX market data, including OHLCV history, latest-close snapshots, market-cap rankings, index series, and ticker lists. It is intended for scriptable informational market-data lookup rather than trading advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned Python dependency ranges can reduce reproducibility in higher-assurance environments.

Mitigation: Pin and hash the Python dependencies before installation when reproducibility or supply-chain assurance is required.

Risk: Market-data output may be delayed, incomplete, or unsuitable as the sole basis for trading decisions.

Mitigation: Treat outputs as informational market data and verify material decisions against official KRX disclosures or another authoritative source.

Risk: Public market-data endpoints can rate-limit requests or change response formats.

Mitigation: Keep multi-ticker jobs near the documented request pace, back off on rate-limit responses, and handle upstream errors explicitly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chloepark85/skills/krx-stock-cli)
- [FinanceDataReader](https://github.com/FinanceData/FinanceDataReader)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, text]

**Output Format:** [Markdown guidance with inline shell commands; CLI output is JSON by default or CSV when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python dependencies and network access to public market-data endpoints; no API key is required.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
