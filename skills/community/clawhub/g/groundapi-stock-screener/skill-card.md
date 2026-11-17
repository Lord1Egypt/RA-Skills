## Description:

Screens A-share stocks by valuation, market cap, dividend yield, industry, and concept using GroundAPI MCP tools, with macro context and result deep dives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingkongzhiqian](https://clawhub.ai/user/qingkongzhiqian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert natural-language A-share screening requests into GroundAPI-backed filters, macro context checks, and concise stock-screening reports. Outputs are intended as informational market screening rather than financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock-screening queries and the GroundAPI key are sent to GroundAPI's MCP service.

Mitigation: Install only when this data sharing is acceptable, store the API key securely, and avoid exposing the key in prompts, logs, or shared configuration.

Risk: Generated stock reports may be mistaken for investment advice.

Mitigation: Treat outputs as informational screening, confirm user intent in ambiguous finance conversations, and require independent review before trading decisions.

Risk: Screening may rely on database snapshot data rather than real-time trading data.

Mitigation: Verify time-sensitive prices, market status, and fundamentals against current authoritative sources before acting.

## Reference(s):

- [GroundAPI](https://groundapi.net)
- [ClawHub skill page](https://clawhub.ai/qingkongzhiqian/skills/groundapi-stock-screener)

## Skill Output:

**Output Type(s):** [markdown, configuration, guidance]

**Output Format:** [Markdown reports with tables and optional JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Follows the user's language, requires GROUNDAPI_KEY, and depends on GroundAPI MCP market-data tools.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
