# Source Evaluation Framework

Framework for evaluating data sources used by Reach.

## Criteria

1. **Reliability** — Uptime and consistency
2. **Coverage** — Data breadth and depth
3. **Latency** — Data freshness
4. **Cost** — Free vs. paid tiers
5. **Rate Limits** — Request quotas

## Evaluation Process

1. Check source against each criterion
2. Score 1-5 per criterion
3. Rank sources by total score
4. Select best source for each data need

## MCP Connector Sources

Some sources are accessed via MCP (Model Context Protocol) servers rather than direct HTTP APIs. These use a `custom: <name>_mcp` module that handles the MCP client session.

**Additional criteria for MCP sources:**

6. **Transport** — Streamable HTTP preferred (no local process); stdio requires installed binary
7. **Auth model** — OAuth, API key, or none; may be handled by the MCP gateway
8. **Async support** — Some MCP tools return async job IDs with polling URLs; the custom module must handle poll/retry logic
9. **Tool coherence** — MCP tools should have clear, distinct purposes (check Glama quality scores)

**Registration pattern:**
- Set `mcp: true`, `mcp_url`, `transport` in sources.yml
- No `base_url` for pure MCP servers
- Custom module at `scripts/sources/<name>.py` exports `query(action, params, auth)`
- Module manages MCP session lifecycle and async polling if needed

## MCP Source Discovery Workflow

When evaluating a candidate MCP connector source:

1. **Fetch the Glama page** (`https://glama.ai/mcp/connectors/<namespace>/<slug>`) for description, status, categories, quality score
2. **Connect directly** — send MCP `initialize` + `tools/list` to the endpoint to get full tool schemas (params, descriptions, annotations)
3. **Check the GitHub repo** for README context, license, account requirements
4. **Score the source** using the 9 criteria above (especially tool coherence and async patterns)
5. **Register** using the MCP connector pattern in sources.yml

The MCP protocol itself is the most reliable source for tool schemas — prefer `tools/list` over README docs when they differ.
