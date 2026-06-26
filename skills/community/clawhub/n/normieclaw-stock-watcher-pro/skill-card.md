## Description: <br>
Stock Watcher Pro helps an agent monitor a user's stock portfolio and watchlist, summarize SEC filings and market news, produce scheduled briefings, and compare new information against the user's investment thesis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and individual investors use this skill to organize portfolio monitoring, SEC filing checks, market briefings, and thesis tracking in an agent workspace. The skill is intended for information gathering and research support, not financial advice or trade execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores portfolio positions, cost basis, price targets, watchlists, filing summaries, and investment thesis notes. <br>
Mitigation: Use it only in a private workspace, keep data directory access restricted, and avoid exposing portfolio queries in shared chats. <br>
Risk: Local-only privacy claims conflict with dashboard materials that describe syncing financial data to Supabase. <br>
Mitigation: Leave dashboard or Supabase sync disabled unless remote sync is intentional and configured with proper authentication and row-level security. <br>
Risk: The package includes shell scripts for scheduling and EDGAR checks. <br>
Mitigation: Review or fix the scripts before granting exec permission or scheduling access. <br>
Risk: Market summaries, filing analysis, and thesis evaluations may be incomplete or inaccurate. <br>
Mitigation: Treat outputs as information only and verify material claims against primary sources before making financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nollio/normieclaw-stock-watcher-pro) <br>
- [README](README.md) <br>
- [Security audit notes](SECURITY.md) <br>
- [Source categories](config/source-categories.md) <br>
- [Dashboard specification](dashboard-kit/DASHBOARD-SPEC.md) <br>
- [SEC EDGAR full-text search](https://efts.sec.gov/LATEST/search-index) <br>
- [SEC company search](https://www.sec.gov/cgi-bin/browse-edgar) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown briefings and analysis, JSON portfolio and source records, shell command snippets, and configuration guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local workspace data files; no trade execution.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
