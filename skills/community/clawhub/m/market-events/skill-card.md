## Description: <br>
Reports upcoming or recent earnings, dividends, and stock splits from Financial Modeling Prep for a watchlist of tickers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[khaney64](https://clawhub.ai/user/khaney64) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to check earnings, dividend, and stock split calendars for specified tickers over a configurable past or future date range. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an FMP API key for market-event lookups. <br>
Mitigation: Use a dedicated, revocable FMP key and rotate it if it is exposed. <br>
Risk: Dependency hygiene is the main security concern because the release depends on requests without a pinned version. <br>
Mitigation: Install in an isolated environment and prefer a maintained, pinned requests release. <br>
Risk: The --file option reads local ticker lists supplied by path. <br>
Mitigation: Point --file only at trusted, simple .txt or .csv ticker lists. <br>
Risk: FMP rate limits or API errors can produce partial results. <br>
Mitigation: Check warnings, narrow the ticker/date range, or retry after the provider rate limit resets. <br>


## Reference(s): <br>
- [Financial Modeling Prep Stable API](https://financialmodelingprep.com/stable) <br>
- [Market Events on ClawHub](https://clawhub.ai/khaney64/market-events) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [Plain text tables, JSON objects, or Discord-flavored Markdown emitted to stdout] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes event dates, tickers, event types, formatted details, and raw FMP event data in JSON mode.] <br>

## Skill Version(s): <br>
0.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
