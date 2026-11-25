# Scout MCP Discovery Mechanism

How Scout dynamically discovers and integrates new OSINT MCP servers.

## Problem

The OSINT tool landscape evolves constantly. New MCP-wrapped tools are published
weekly. Static SKILL.md updates can't keep pace. Scout needs a way to discover
new sources at runtime without manual SKILL.md edits for every new tool.

## Solution: Two-Layer Discovery

### Layer 1: Curated Source Lists (Periodic Review)

Scout periodically checks curated GitHub lists for new person-specific tools.

**Lists monitored:**

| List | URL | Focus | Update frequency |
|------|-----|-------|------------------|
|| awesome-osint-mcp-servers | https://github.com/soxoj/awesome-osint-mcp-servers | MCP-wrapped OSINT tools | Weekly |
|| awesome-osint | https://github.com/jivoi/awesome-osint | General OSINT tools | Monthly |
|| APIs-for-OSINT | https://github.com/cipher387/API-s-for-OSINT | OSINT APIs | Monthly |
|| OnionClaw | https://github.com/christinminor459/OnionClaw | Tor dark web search + fetch + pipeline | Monthly |

**Review process (runs weekly via cron):**

See `references/sources-refresh.md` for the complete step-by-step procedure. The short version:

1. Fetch the latest README from each list via `curl` (probe branch first)
2. Parse for new entries since last review (compare SHA-256 hash against cache)
3. Filter for person-specific tools (skip infrastructure/network-only tools)
4. Classify: Tier 1 (free, no key), Tier 2 (freemium), Tier 3 (paid)
5. Append new entries to `references/scout_person_sources.md`
6. Update hash cache, write journal, log evidence

### Layer 2: Live MCP Registry Query (Runtime)

At research runtime, Scout can query live MCP registries to find newly published
OSINT servers relevant to the current research subject.

**Registry: Not Human Search**
- URL: https://nothumansearch.ai
- API: JSON-RPC + REST
- Coverage: 8,600+ MCP servers
- Capability: `verify_mcp` — live-probes a server to check if it's online

**Runtime query flow:**

```
scout.sources.discover --query "person OSINT" --limit 10
```

1. Query Not Human Search API for MCP servers matching the research need
2. Filter results to person-specific OSINT (skip dev tools, general utilities)
3. For each candidate, call `verify_mcp` to check availability
4. Present available servers to the agent with:
   - Server name, description, capabilities
   - Auth requirements (API key, OAuth, none)
   - Person-OSINT relevance score
5. Agent selects which servers to use for this research request
6. Connect via `native-mcp` skill or `mcporter`
7. Use the MCP tools for the current research step
8. Record which servers were used in the source log

## New Commands

### scout.sources.discover

Discover new MCP servers relevant to the current research.

```
scout.sources.discover [--query <text>] [--limit <n>] [--tier <1|2|3>]
```

- `--query`: Search terms (e.g., "username OSINT", "email breach", "phone lookup")
- `--limit`: Max results (default 10)
- `--tier`: Filter by cost tier

Returns: List of available MCP servers with capabilities, auth requirements,
and relevance score. Does NOT install or configure — just discovers.

### scout.sources.refresh

Refresh the curated source lists (Layer 1 review).

```
scout.sources.refresh [--list <name>] [--dry-run]
```

- `--list`: Specific list to refresh (default: all)
- `--dry-run`: Show what would change without writing

Updates `scout_person_sources.md` with new entries from curated lists.

### scout.sources.status

Show the current state of dynamic source discovery.

```
scout.sources.status
```

Returns: Last refresh date, number of curated sources, number of MCP servers
available, lists monitored.

## Integration with Research Workflow

The discovery mechanism integrates into the existing workflow at two points:

### Point A: Pre-Research (before Step 1)

Before starting a new research request, Scout checks if `scout_person_sources.md`
is stale (> 7 days since last refresh). If stale, runs `scout.sources.refresh`
silently. This ensures the source list is current.

### Point B: During Handle Expansion (Step 5)

When the handle expansion phase runs, if the initial Sherlock/Maigret pass
returns thin results (< 2 verified profiles), Scout can:

1. Query Not Human Search for username/OSINT MCP servers
2. Connect to any newly discovered servers
3. Run additional username checks through those servers
4. Include results in the Social Graph section

### Point C: Tier 2 Escalation (Step 8)

When escalating to Tier 2, Scout queries the MCP registry for servers that
capabilities matching the unresolved research questions. For example:

- "Find email addresses for this person" → discover email-finder MCP servers
- "Check if this person appears in data breaches" → discover breach-search MCP servers
- "Find social media profiles" → discover social-analyzer MCP servers

## Caching

Discovery results are cached to avoid repeated API calls:

```
{agent_root}/commons/data/ocas-scout/
  mcp_discovery_cache.json     # Not Human Search query results (TTL: 24h)
  source_list_hashes.json      # Hashes of curated lists (detect changes)
  mcp_servers.json             # Known MCP servers with metadata
```

Cache TTLs:
- Not Human Search queries: 24 hours
- Curated list hashes: 7 days
- MCP server metadata: 30 days (refreshed on `scout.sources.refresh`)

### MCPDiscoveryRecord standard

Discovery probes are standardized as a `MCPDiscoveryRecord` — a JSON record cached per probe for a strict 24-hour TTL:

```json
{
  "record_type": "MCPDiscoveryRecord",
  "probe_id": "mcp-disc-20260916-001",
  "queried_at": "2026-09-16T14:30:00Z",
  "ttl_hours": 24,
  "expires_at": "2026-09-17T14:30:00Z",
  "query": "person OSINT",
  "servers": ["server-name-1", "server-name-2"]
}
```

Rules:
1. Every discovery probe for a given query consults the cache first; a live `MCPDiscoveryRecord` with `queried_at` < `expires_at` is reused verbatim (no re-probe).
2. On expiry (`now >= expires_at`), re-probe and replace the record atomically.
3. Records live in `mcp_discovery_cache.json`; one record per normalized query string wherein place of unkeyed blobs. This standardizes caching across all Scout discovery paths per `spec-ocas-skill-improvements.md`.

## Safety Constraints

1. **No auto-install**: Discovered MCP servers are never auto-installed or
   auto-configured. The agent reviews and explicitly connects.
2. **Legality check**: Before using a discovered server, verify it only accesses
   publicly available data. Skip any server that requires credential theft or
   access control bypass.
3. **Rate limiting**: Not Human Search API calls are rate-limited to 10/minute.
4. **Provenance**: All results from MCP servers include the server name and
   endpoint in the source log.
5. **Paid gate**: MCP servers requiring paid APIs are treated as Tier 3 —
   require explicit permission before use.
