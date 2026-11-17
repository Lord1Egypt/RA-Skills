## Description:

Stock Watcher Pro helps an agent monitor a user's portfolio and watchlist, track SEC filings and market news, generate scheduled briefings, and compare new information against the user's investment thesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nollio](https://clawhub.ai/user/nollio)

### License/Terms of Use:

MIT

## Use Case:

Individual investors and their agents use this skill to organize portfolio intelligence, monitor public sources such as SEC EDGAR and investor-relations pages, and produce briefings and thesis updates. The skill is for information gathering and research support, not financial advice or trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores sensitive portfolio holdings, cost basis, thesis notes, and generated briefings locally.

Mitigation: Use private workspaces, restrictive file permissions, encrypted storage and backups, and avoid portfolio queries in shared chat contexts.

Risk: Recurring checks can create scheduled automation that reads local portfolio data and performs web requests.

Mitigation: Review or disable heartbeat, cron, or Trigger.dev scheduling before enabling recurring briefings and filing checks.

Risk: Server security evidence reports conflicting local-only and dashboard cloud-sync claims.

Mitigation: Keep dashboard cloud synchronization disabled unless the user explicitly wants Supabase storage and understands what data will be synced.

Risk: Financial summaries and thesis classifications can be wrong or incomplete and are not financial advice.

Mitigation: Verify material filings and market data from primary sources and do not treat outputs as recommendations or trade instructions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/nollio/skills/normieclaw-stock-watcher-pro)
- [README](README.md)
- [Security audit notes](SECURITY.md)
- [First-run setup guide](SETUP-PROMPT.md)
- [Source categories reference](config/source-categories.md)
- [Dashboard companion specification](dashboard-kit/DASHBOARD-SPEC.md)
- [SEC EDGAR full-text search endpoint](https://efts.sec.gov/LATEST/search-index)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown briefings, JSON records, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read and write local portfolio, watchlist, briefing, filing, source, and thesis-log files when the host agent grants file access.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
