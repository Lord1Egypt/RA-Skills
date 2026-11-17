## Description:

Longbridge Openapi helps agents use Longbridge Securities for market data, security analysis, account-state lookups, watchlists, price alerts, and recurring DCA plan workflows across US, Hong Kong, A-share, Singapore, and crypto markets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[genkin-he](https://clawhub.ai/user/genkin-he)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and finance-focused agents use this skill to retrieve Longbridge market data, analyze securities, inspect authenticated brokerage account state, and prepare carefully gated watchlist, alert, or recurring investment changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated workflows can expose private brokerage account data, including holdings, orders, cash flow, statements, watchlists, alerts, and DCA plans.

Mitigation: Install only if you trust Longbridge, and keep detailed account values in direct conversation rather than tickets, pull requests, logs, or other shared records.

Risk: Watchlist, price-alert, and DCA workflows can make persistent account changes.

Mitigation: Use a preview-then-confirm flow and require explicit confirmation before running any mutating command.

Risk: Recurring DCA plans can commit real money on a schedule.

Mitigation: Before confirming DCA changes, read back and verify every symbol, amount, currency, frequency, start date, and end condition.

Risk: Authenticated workflows that write to fixed /tmp paths can leave sensitive financial output on disk.

Mitigation: Avoid fixed temporary paths for authenticated brokerage data and remove temporary files that contain account information.

## Reference(s):

- [Longbridge OpenAPI Documentation](https://open.longbridge.com)
- [Longbridge llms.txt](https://open.longbridge.com/llms.txt)
- [Longbridge Skills Repository](https://github.com/longbridge/skills)
- [Longbridge MCP Endpoint](https://openapi.longbridge.com/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and structured financial summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Matches the user's language and cites Longbridge Securities as the data source for analysis outputs.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
