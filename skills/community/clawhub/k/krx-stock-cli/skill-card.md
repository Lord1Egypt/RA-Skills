## Description: <br>
KRX Stock CLI gives agents zero-config command-line access to Korean Exchange market data, including OHLCV history, latest-close snapshots, market-cap rankings, index histories, and ticker/name lookup in JSON or CSV. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chloepark85](https://clawhub.ai/user/chloepark85) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, quant analysts, retail investors, and fintech builders use this skill to resolve Korean tickers and retrieve scriptable KRX market data for analysis workflows. It is suited to end-of-day market data lookup, ticker search, index history, and CSV or JSON export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency versions are specified with lower bounds, so future dependency changes may affect behavior. <br>
Mitigation: Install in a virtual environment and pin or review dependency versions before production use. <br>
Risk: The skill retrieves public market data through upstream sources and may be affected by data delays, schema changes, rate limits, or temporary access errors. <br>
Mitigation: Back off on rate-limit responses and verify important trading or financial decisions against official KRX or disclosure sources. <br>
Risk: The CLI is designed for end-of-day and latest-close data, not real-time ticks or order-book data. <br>
Mitigation: Use a real-time market-data provider for intraday execution, tick, or order-book workflows. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/chloepark85/krx-stock-cli) <br>
- [FinanceDataReader](https://github.com/FinanceData/FinanceDataReader) <br>
- [Command reference](SKILL.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, CSV, Text] <br>
**Output Format:** [JSON by default, CSV when requested, and JSON-formatted errors on stderr] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [UTF-8 output with Korean text preserved; time-series dates are formatted as YYYY-MM-DD.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
