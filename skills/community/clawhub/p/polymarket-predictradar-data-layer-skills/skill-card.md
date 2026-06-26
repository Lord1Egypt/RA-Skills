## Description: <br>
Shared Polymarket and prediction-market data access layer. Use this skill whenever another skill or task needs trader positions, trade history, market metadata, leaderboard data, win-rate or PnL statistics, or any other read-only market intelligence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cnica](https://clawhub.ai/user/cnica) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent workflows use this skill as a shared data layer for Polymarket and prediction-market analysis. It supports trader positions, trade history, market metadata, leaderboards, preview SQL analytics, streamed exports, and local cache-backed enrichment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes network requests and sends query data plus API-key headers to configured endpoints. <br>
Mitigation: Use a trusted MCP_URL, avoid sensitive private API keys, and review endpoint configuration before deployment. <br>
Risk: Gamma API requests disable HTTPS certificate verification. <br>
Mitigation: Fix TLS certificate validation before relying on generated reports or production workflows. <br>
Risk: Broad SQL and tool access can exceed a narrow read-only analytics boundary if reused carelessly. <br>
Mitigation: Prefer preview queries with tight limits, validate wallet inputs, and review SQL examples before execution. <br>
Risk: Trader and market data may be cached locally. <br>
Mitigation: Protect the workspace cache, clear cached data when no longer needed, and bypass cache when freshness is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/cnica/polymarket-predictradar-data-layer-skills) <br>
- [Fallback Queries](references/fallback-queries.md) <br>
- [Polymarket Shared Analytics Fields / API Field Reference](references/table-schema.md) <br>
- [PredicTradar MCP endpoint](https://api.predictradar.ai/api/mcp/v2) <br>
- [Polymarket Data API](https://data-api.polymarket.com) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [Polymarket CLI](https://github.com/Polymarket/polymarket-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell snippets; helper scripts and API calls return JSON-like market and trader data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-oriented market-data workflows may use network calls, preview SQL queries, streamed exports, and local file-backed cache entries.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
