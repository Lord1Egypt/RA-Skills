## Description:

Generates Indonesian-language morning and closing IHSG market summaries with top net buy/sell, foreign flow, year-to-date flow, and narrative insights using Yahoo Finance, Infovesta, and Tavily-sourced data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raufimusaddiq](https://clawhub.ai/user/raufimusaddiq)

### License/Terms of Use:

MIT

## Use Case:

External users and market analysts use this skill to produce scheduled Bahasa Indonesia summaries for IHSG morning and closing sessions. The skill gathers index, stock-flow, foreign-flow, and price-change data, then formats a session report with actionable market commentary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tavily API keys can be exposed if supplied on the command line or stored in shared job definitions.

Mitigation: Set TAVILY_API_KEY through the runtime environment and avoid passing secrets with --tavily-api-key in scheduled jobs.

Risk: The skill performs scheduled external web searches and financial-data requests to Yahoo Finance, Tavily, and Infovesta.

Mitigation: Run it in a dedicated environment, monitor network egress and Tavily usage, and confirm the schedule is appropriate before production use.

Risk: Dependency ranges are not pinned, so future package updates may change behavior.

Mitigation: Use pinned dependencies or a lockfile before production deployment.

Risk: Generated market summaries may reflect incomplete, stale, or unavailable source data.

Mitigation: Review generated reports before relying on them for market decisions, especially when the script flags missing top-flow, price-change, foreign-flow, or YTD data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raufimusaddiq/skills/ihsg-session-summary)
- [Yahoo Finance IHSG chart endpoint](https://query1.finance.yahoo.com/v8/finance/chart/%5EJKSE)
- [Tavily API](https://app.tavily.com)
- [Infovesta top buy data](https://www.infovesta.com/index/data_info/saham/topbuy)
- [Infovesta top sell data](https://www.infovesta.com/index/data_info/saham/topsell)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Plain text reports with ASCII tables, or JSON from the extractor script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are written in Bahasa Indonesia and differ by morning or closing session.]

## Skill Version(s):

4.0.1 (source: skill metadata and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
