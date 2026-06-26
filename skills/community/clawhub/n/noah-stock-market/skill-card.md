## Description: <br>
Provides read-only Hong Kong and U.S. stock market data queries and structured market summaries for quotes, market snapshots, intraday and K-line data, market depth, trades, broker queues, market status, capital flow, fundamentals, options, and related lookup scenarios; it does not place orders or provide investment advice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuyun9160-lgtm](https://clawhub.ai/user/xuyun9160-lgtm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer Hong Kong and U.S. equity market-data questions with concise, structured summaries. It is suited for read-only quote, chart, market status, capital-flow, financial-data, and shareholder-information lookups when the user has configured the required market-data token. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive credentials and can access private wealth, balance, total-asset, fixed-income, and private-asset data. <br>
Mitigation: Install only when private securities-account data access is intended, use a least-privilege market-data token, and avoid trading-capable or broadly privileged tokens. <br>
Risk: Market-data results may be unavailable, permission-limited, stale, or unsupported for some symbols, markets, and endpoints. <br>
Mitigation: Check the response status and data timestamp, explain 401/403/404 or empty-data cases directly, and do not fabricate missing market data. <br>
Risk: Structured market summaries could be mistaken for trading recommendations. <br>
Mitigation: Keep responses objective, avoid buy or sell advice, and present market observations as data summaries rather than investment guidance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xuyun9160-lgtm/noah-stock-market) <br>
- [Usage Guide](references/usage-guide.md) <br>
- [Current Availability](references/current-availability.md) <br>
- [Authentication and Preflight](references/auth-and-preflight.md) <br>
- [Routing Specification](references/routing-spec.md) <br>
- [Known Limitations](references/known-limitations.md) <br>
- [Output Policy](references/output-policy.md) <br>
- [OpenAPI Protocol Reference](references/openapi.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with occasional inline shell commands or configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default responses summarize market data, translate enum values into readable labels, include data time or status when available, and avoid raw JSON unless details are explicitly requested.] <br>

## Skill Version(s): <br>
1.2.10 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
