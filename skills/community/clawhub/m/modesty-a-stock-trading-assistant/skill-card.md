## Description:

Provides real-time China A-share market quotes, individual stock analysis, market sentiment review, sector hotspot identification, trading strategy support, and price alert assistance for Shanghai and Shenzhen A-share stocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer China A-share quote, technical analysis, market sentiment, hotspot sector, trading strategy, and alert-related questions. It is limited to Shanghai and Shenzhen A-share securities and should be treated as informational support rather than a substitute for a trusted broker or financial adviser.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce specific trading suggestions based on market feeds that can be delayed, incomplete, or tampered with when fetched over plaintext HTTP.

Mitigation: Verify quotes and recommendations with a trusted broker or market data provider before making investment decisions, and treat outputs as informational only.

Risk: Price alert workflows may save watchlist entries that become stale or expose sensitive trading interests.

Mitigation: Review saved alerts periodically and remove stale or sensitive watchlist entries.

## Reference(s):

- [Individual Stock Analysis Method Reference](references/analysis.md)
- [Market Data Source API Reference](references/data-sources.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown with tables, structured recommendations, and optional JSON or shell command outputs from the stock data script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include data source attribution, retrieval time, concise risk reminders, and two-decimal numeric formatting where applicable.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
