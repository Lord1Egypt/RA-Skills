## Description:

Fundamental equity analysis and peer ranking for one or more stock tickers using a structured scoring playbook covering quality, balance-sheet safety, cash flow, valuation, sector adjustments, confidence modifiers, best-pick selection, and fundamentals-based verdicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to analyze one or more public stock tickers, compare peers, and produce fundamentals-based verdicts with confidence levels, stale-data warnings, and invalidation triggers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock conclusions may be wrong, stale, or unsuitable for a user's financial situation.

Mitigation: Treat outputs as informational, verify material claims against current filings and reputable finance sources, and require human judgment before investment decisions.

Risk: Ticker analysis may rely on public web retrieval and could include incomplete or conflicting market data.

Mitigation: Use ticker-relevant filings, investor materials, public fundamental datasets, and relevant financial news; mark missing metrics as NA and reduce confidence for stale or conflicting data.

Risk: Web activity could exceed the intended finance-analysis scope if prompts are ambiguous.

Mitigation: Restrict retrieval to ticker-relevant financial statements, filings, market datasets, and relevant news; do not request credentials, inspect local files, or explore arbitrary URLs.

## Reference(s):

- [Fundamental Stock Analysis Playbook](references/playbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with scored analysis sections, peer rankings when applicable, source links, and concise investment-risk context]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Educational and informational content only; user-facing output avoids machine-readable JSON blocks and calls out stale, conflicting, or unavailable metrics.]

## Skill Version(s):

1.0.0 (source: server release evidence, created 2026-04-24)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
