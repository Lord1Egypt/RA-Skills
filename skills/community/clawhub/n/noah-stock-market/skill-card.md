## Description:

Provides read-only Hong Kong and U.S. stock market data queries and structured market summaries, including quotes, snapshots, intraday and K-line data, market status, capital flow, fundamentals, rankings, IPO data, financial data, shareholder activity, and supported wealth or asset lookups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuyun9160-lgtm](https://clawhub.ai/user/xuyun9160-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to retrieve and summarize read-only Hong Kong and U.S. market data through the configured Noah securities API token. It is intended for factual market and supported wealth or asset lookups, not order placement, trading execution, account changes, or investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access private wealth or asset data through the configured Noah API token.

Mitigation: Install only for users who need those lookups and configure a dedicated, least-privileged read-only token.

Risk: A broad token or changed base URL could expose data beyond normal market-data use.

Mitigation: Keep the base URL fixed to the documented production host and avoid credentials that permit trading or broader account actions.

Risk: Some routes are only partially verified or unavailable in the current environment.

Mitigation: Do not overstate unverified capabilities; report API failures or unsupported symbols directly instead of fabricating market data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xuyun9160-lgtm/skills/noah-stock-market)
- [References Index](references/README.md)
- [Usage Guide](references/usage-guide.md)
- [Authentication and Preflight](references/auth-and-preflight.md)
- [Current Availability](references/current-availability.md)
- [Known Limitations](references/known-limitations.md)
- [Output Policy](references/output-policy.md)
- [API Mapping](references/api-mapping.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with optional inline shell commands and concise status or error messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to summary-first responses; detail mode is limited to recent records and raw JSON is avoided unless explicitly requested.]

## Skill Version(s):

1.2.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
