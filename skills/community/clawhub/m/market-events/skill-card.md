## Description:

Reports upcoming or recent earnings, dividends, and stock splits from FMP for a watchlist of tickers, accepting a comma-separated ticker list or a file of tickers and returning events in a requested date range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[khaney64](https://clawhub.ai/user/khaney64)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to check upcoming or recent corporate market events for specified stock tickers. It is suited for earnings dates, dividend schedules, and stock split lookups over a bounded date window.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an FMP API key to query market-event data.

Mitigation: Use an FMP API key intended for this workflow and keep it scoped to the execution environment.

Risk: Ticker-list files are read from paths supplied by the user.

Mitigation: Pass ticker files intentionally and review file paths before execution.

Risk: FMP rate limits or API errors can produce partial results.

Mitigation: Review warnings in the command output and verify important market events against an authoritative source.

Risk: Dependency behavior may change if requests is installed without a pinned version.

Mitigation: Install from a locked environment or pin dependencies when reproducibility matters.

## Reference(s):

- [Financial Modeling Prep stable API](https://financialmodelingprep.com/stable)
- [Market Events on ClawHub](https://clawhub.ai/khaney64/skills/market-events)
- [Publisher profile](https://clawhub.ai/user/khaney64)

## Skill Output:

**Output Type(s):** [Text, JSON, Markdown]

**Output Format:** [Plain text table, JSON object, or Discord-style Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results include event date, ticker, event type, detail text, and raw FMP response data when JSON output is requested.]

## Skill Version(s):

0.1.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
