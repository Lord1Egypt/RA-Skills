---
name: mcp-registry
description: Discover, search, and browse MCP servers from the official MCP Registry
  and MCPCentral. Find servers, get specs, and generate setup configurations. Use
  when the user wants to find, install, or configure MCP servers or tools.
compatibility: Requires internet access to registry.modelcontextprotocol.io and mcpcentral.io
metadata:
  author: mcpcentral.io
  version: "1.0.0"
---

# MCPCentral - MCP Server Discovery

Discover and search MCP servers using two real data sources:

1. **Official MCP Registry** (`registry.modelcontextprotocol.io`) — canonical source for server metadata, versions, packages, transport config, and environment variables. Public, no auth required.
2. **MCPCentral** (`mcpcentral.io`) — enrichment data: GitHub stars, npm downloads, editorial picks. Paginated bulk endpoint.

## Gotchas

- **Server names contain `/` and must be URL-encoded.** Names like `io.github.owner/server-name` must be encoded as `io.github.owner%2Fserver-name` in URL path segments. Forgetting this causes 404 "Endpoint not found" errors.
- **`cursor` vs `next_cursor` naming inconsistency.** The MCPCentral API accepts a `cursor` query parameter for pagination, but the response field containing the next token is named `next_cursor`. These are different names for input and output.
- **MCPCentral has no search parameter.** The `mcpcentral.io/api/servers` endpoint only supports paginated browsing sorted by stars. Use the official registry for keyword search.
- **`title` and `websiteUrl` may be null.** Fall back to `name` for display and `repository.url` for linking when these fields are absent.
- **MCPCentral enrichment data may lag the official registry.** Always use the official registry for authoritative version and package data; treat MCPCentral metrics as supplemental.

## Important: What the Registry Contains (and Doesn't)

**Contains:** Package metadata (npm/pypi/docker identifiers), install commands, transport configuration (stdio/SSE/streamable-http), environment variables, remote URLs, repository links, version history.

**Does NOT contain:** Tool schemas, tool lists, or runtime behavior. The registry stores *how to install and connect* to a server, not *what tools it exposes*.

**To discover a server's actual tools:** Install it and call `tools/list` via MCP protocol, or read its README/documentation.

## API Reference

All endpoints are public. No authentication required.

### Official Registry Endpoints

**Search servers:**
```
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=QUERY&limit=N&version=latest"
```
Parameters: `search` (substring match on name/description), `limit` (results per page, default 100), `cursor` (pagination token from previous response), `updated_since` (ISO 8601 datetime), `version=latest` (only latest versions).

**Get specific server version:**
```
curl "https://registry.modelcontextprotocol.io/v0.1/servers/SERVER_NAME_URL_ENCODED/versions/latest"
```
The server name contains a `/` (e.g., `io.github.owner/server-name`), so it must be URL-encoded as `%2F` in the path. Example: `io.github.Digital-Defiance%2Fmcp-filesystem`.

**List all versions:**
```
curl "https://registry.modelcontextprotocol.io/v0.1/servers/SERVER_NAME_URL_ENCODED/versions"
```

### MCPCentral Endpoint

**Browse servers with enrichment data:**
```
curl "https://mcpcentral.io/api/servers?limit=N&cursor=TOKEN"
```
Returns servers sorted by stars (descending). Response includes: `count` (total), `limit`, `next_cursor` (base64 pagination token), `servers[]`. No search parameter — use for browsing popular servers or enriching data from the official registry.

**Note:** The pagination query parameter is `cursor`, but the response field containing the next token is `next_cursor`.

## Capabilities

### Searching for Servers

Use the official registry search endpoint. The search is a **substring match** on server names and descriptions — it is not NLP or semantic search.

```
curl "https://registry.modelcontextprotocol.io/v0.1/servers?search=postgres&limit=5&version=latest"
```

**Parse the response:** Each result is in `servers[].server` with fields: `name`, `description`, `version`, `repository.url`, `packages[]`, `remotes[]`. Metadata is in `servers[]._meta["io.modelcontextprotocol.registry/official"]` with `status`, `publishedAt`, `updatedAt`, `isLatest`.

**Pagination:** If `metadata.nextCursor` is present, pass it as `cursor` to get the next page.

**Fallback strategies for few/no results:**
- Try shorter or alternative keywords (e.g., "db" instead of "database")
- Try the package name (e.g., "mcp-server-sqlite" instead of "sqlite tool")
- Browse recent servers without a search term

### Getting Server Details

Fetch the latest version of a specific server by name:

```
curl "https://registry.modelcontextprotocol.io/v0.1/servers/io.github.owner%2Fserver-name/versions/latest"
```

**Key fields to extract from the response:**
- `server.name` — canonical identifier
- `server.title` — human-readable display name (may be null)
- `server.description` — what it does
- `server.version` — current version
- `server.repository.url` — source code link
- `server.websiteUrl` — project homepage (may be absent)
- `server.packages[]` — install methods, each with:
  - `registryType` (npm, pypi, docker)
  - `identifier` (package name)
  - `transport.type` (stdio, sse, streamable-http)
  - `environmentVariables[]` (name, description, isRequired, isSecret)
  - `runtimeHint` (e.g., "node", "python", "uvx")
  - `runtimeArguments[]`, `packageArguments[]`
- `server.remotes[]` — hosted endpoints (type, url, headers)
- `server.icons[]` — server icons (src, theme, sizes)
- `_meta["io.modelcontextprotocol.registry/official"].status` — active, deprecated, or deleted
- `_meta["io.modelcontextprotocol.registry/official"].publishedAt`, `.updatedAt`, `.isLatest`

### Listing Versions

Get all published versions of a server:

```
curl "https://registry.modelcontextprotocol.io/v0.1/servers/io.github.owner%2Fserver-name/versions"
```

Response is `servers[]` array, each with full server metadata. Version status is in `_meta["io.modelcontextprotocol.registry/official"]` with `status` (active/deprecated/deleted) and `isLatest` (boolean).

### Browsing Recent/Popular Servers

To explore without a specific search term:

**Browse by recency (official registry):**
```
curl "https://registry.modelcontextprotocol.io/v0.1/servers?limit=10&version=latest&updated_since=2026-01-01T00:00:00Z"
```

**Browse by popularity (MCPCentral):**
```
curl "https://mcpcentral.io/api/servers?limit=10"
```
Results are sorted by GitHub stars descending. Pass the `next_cursor` value from the response as the `cursor` query parameter to get the next page.

### Recommending Servers (AI-Synthesized)

There is no recommendation API. To recommend servers for a user's task:

1. **Extract keywords** from the user's request (e.g., "I need to query a database" → search "database", "query", "sql")
2. **Run multiple searches** with different keywords against the official registry
3. **Merge and rank results** based on: description relevance, number of keyword matches, whether the server has packages (installable) vs only remotes (hosted)
4. **Present as AI recommendations** — clearly label these as your synthesis, not an API result

### Generating Setup Guides

Extract installation and configuration from real server metadata. After fetching a server's details:

**1. Determine install method from `packages[]`:**

For `registryType: "npm"`:
```bash
npx -y PACKAGE_IDENTIFIER
```

For `registryType: "pypi"`:
```bash
uvx PACKAGE_IDENTIFIER
# or: pip install PACKAGE_IDENTIFIER && python -m PACKAGE_IDENTIFIER
```

For `registryType: "docker"`:
```bash
docker run PACKAGE_IDENTIFIER
```

**2. Extract environment variables from `packages[].environmentVariables[]`:**
List each with its `name`, `description`, and whether `isRequired`/`isSecret`.

**3. Check for remote endpoints in `remotes[]`:**
If the server has `remotes[]`, it can be used without local installation via its hosted URL.

**4. Generate MCP client configuration** (see "Next Steps After Discovery" below).

### Reading Server Documentation

The registry does not store READMEs. To discover a server's actual tools and capabilities:

1. Extract `repository.url` from the server metadata
2. Construct the raw README URL:
   - GitHub: `https://raw.githubusercontent.com/OWNER/REPO/HEAD/README.md`
   - If the repo has a `subfolder`, try: `https://raw.githubusercontent.com/OWNER/REPO/HEAD/SUBFOLDER/README.md`
3. Fetch and summarize the README content

This is the best way to discover what tools a server actually exposes, since the registry only stores package metadata.

## MCPCentral Enrichment

Use the MCPCentral endpoint to add community metrics when presenting servers to users:

```
curl "https://mcpcentral.io/api/servers?limit=100"
```

**Enrichment fields per server:**
- `stars` — GitHub stars count
- `npm_weekly_downloads` — npm download volume
- `npm_license` — package license
- `recommended` — MCPCentral editorial recommendation (boolean or null)
- `admin_favorite` — MCPCentral staff pick (boolean or null)
- `official` — officially maintained (boolean or null)
- `owner.name`, `owner.avatar_url` — author info

**When to use:** When a user wants to compare servers by popularity, or when browsing for well-maintained options. Match servers between the two sources using the `name` field (format: `io.github.owner/server-name`).

**Note:** MCPCentral has no search parameter. To find a specific server's enrichment data, fetch pages and filter client-side by name, or use it for popularity-sorted browsing.

## Next Steps After Discovery

After a user finds a server, provide setup configuration for their MCP client. Generate these from the server's real `packages[]`, `remotes[]`, and `environmentVariables[]` data.

### For stdio-based servers (local install)

**Claude Desktop** (`claude_desktop_config.json`):
```json
{
  "mcpServers": {
    "SERVER_NAME": {
      "command": "npx",
      "args": ["-y", "PACKAGE_IDENTIFIER"],
      "env": {
        "ENV_VAR_NAME": "your-value-here"
      }
    }
  }
}
```

**VS Code** (`.vscode/mcp.json`):
```json
{
  "servers": {
    "SERVER_NAME": {
      "command": "npx",
      "args": ["-y", "PACKAGE_IDENTIFIER"],
      "env": {
        "ENV_VAR_NAME": "your-value-here"
      }
    }
  }
}
```

**Generic** (`.mcp.json` / `mcp.json`):
```json
{
  "mcpServers": {
    "SERVER_NAME": {
      "command": "npx",
      "args": ["-y", "PACKAGE_IDENTIFIER"],
      "env": {
        "ENV_VAR_NAME": "your-value-here"
      }
    }
  }
}
```

Adapt the `command` and `args` based on `registryType`:
- **npm**: `"command": "npx", "args": ["-y", "IDENTIFIER"]`
- **pypi**: `"command": "uvx", "args": ["IDENTIFIER"]`
- **docker**: `"command": "docker", "args": ["run", "-i", "--rm", "IDENTIFIER"]`

If the package has `runtimeHint` or `runtimeArguments`, use those to build the command instead.

### For remote servers (hosted endpoint)

If the server has `remotes[]` entries, provide the URL-based config:

```json
{
  "mcpServers": {
    "SERVER_NAME": {
      "url": "REMOTE_URL",
      "transport": "sse"
    }
  }
}
```

Use the `remotes[].type` to set the transport (`sse`, `streamable-http`).

### Required environment variables

Always list any environment variables from `packages[].environmentVariables[]`, noting which are required and which are secrets. Example:

> **Required environment variables:**
> - `DATABASE_URL` (required) — PostgreSQL connection string
> - `API_KEY` (required, secret) — Authentication token

## Error Handling

**404 "Endpoint not found":** The server name must be URL-encoded. The `/` in names like `io.github.owner/repo` must be encoded as `%2F`.

**Empty search results:** Try shorter keywords, alternative terms, or browse without a search term. The search is substring-based, not fuzzy.

**Rate limiting:** The official registry is public with generous limits. If you encounter rate limits, add a brief pause between requests.

**Stale MCPCentral data:** The MCPCentral bulk endpoint may lag behind the official registry. Always prefer the official registry for version and package data; use MCPCentral only for enrichment metrics.

## Limitations

- **No tool schemas in the registry.** The registry stores package/install metadata only. To see what tools a server exposes, read its README or install it and call `tools/list`.
- **Search is substring-based.** The official registry search matches substrings in name and description fields. It does not support semantic/NLP search, relevance scoring, or category filtering.
- **MCPCentral has no search.** The MCPCentral endpoint returns servers sorted by stars with pagination, but has no search parameter.
- **Server names must be URL-encoded** in path parameters since they contain `/`.
