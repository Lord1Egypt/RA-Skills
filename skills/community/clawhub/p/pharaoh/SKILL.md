---
name: pharaoh
description: "Codebase knowledge graph with 23 development workflow skills. Query architecture, dependencies, blast radius, dead code, and test coverage via MCP. Requires GitHub App installation (read-only repo access) and OAuth authentication. Connects to external MCP server at mcp.pharaoh.so."
version: 0.3.5
homepage: https://pharaoh.so
metadata: {"emoji": "☥", "openclaw": {"requires": {"bins": ["npx", "node"], "env": [], "config": "~/.pharaoh/credentials.json"}, "permissions": {"network": ["mcp.pharaoh.so", "github.com"], "filesystem": ["~/.pharaoh/", "~/.openclaw/"]}, "always": false}, "tags": ["code-intelligence", "architecture", "mcp", "knowledge-graph", "dependencies", "blast-radius", "dead-code", "code-review", "refactoring", "test-coverage", "codebase-understanding", "developer-tools", "ai-coding"]}
---

# Pharaoh — Codebase Knowledge Graph + Developer Skill Library

Pharaoh parses your source files server-side to extract structural metadata (names, signatures, imports, relationships) and stores that metadata — not source code bodies — in a knowledge graph. AI agents then query the graph instead of reading files one at a time.

## What the Installer Does

Running `npx @pharaoh-so/mcp --install-skills` performs these actions:

1. **Downloads** the `@pharaoh-so/mcp` npm package ([source](https://github.com/Pharaoh-so/pharaoh-mcp), [npm](https://www.npmjs.com/package/@pharaoh-so/mcp))
2. **Copies 23 skill directories** (SKILL.md markdown files) into `~/.openclaw/skills/` — **warning: overwrites existing pharaoh skill files on reinstall** (uses `cpSync` with `force: true`; does not touch non-pharaoh skills)
3. **Adds an MCP server entry** `"pharaoh"` to `~/.openclaw/openclaw.json` under `mcpServers` (skips if already present, refuses to write if JSON is corrupted)
4. If OpenClaw is not detected (`~/.openclaw/` doesn't exist), prints manual installation instructions and exits — **does not create directories or modify config**

Authentication happens separately when the MCP server first runs (not during `--install-skills`):
- **Device flow** ([RFC 8628](https://datatracker.ietf.org/doc/html/rfc8628)) — displays a code, you authorize on any device with a browser
- **Credentials stored** at `~/.pharaoh/credentials.json` (file permissions `0600`, owner-only)

No background processes are installed. No cron jobs. No system services.

**Architecture:** The `@pharaoh-so/mcp` package runs a local stdio proxy process — it starts when your AI client launches it and stops when the session ends. This proxy relays MCP messages to the remote Pharaoh server at `mcp.pharaoh.so`, where parsing and graph queries execute. Your repository metadata is sent to and stored on Pharaoh's servers (see Data & Privacy below). The proxy itself does not parse code or store data locally.

## Authentication & Permissions

**OAuth flow:** GitHub device authorization grant (RFC 8628). You approve access in your browser — no secrets are embedded in the package.

**GitHub App scopes** (when installed on your org):
- `contents: read` — read-only access to parse repository files via tree-sitter
- `metadata: read` — repo names, languages, default branch
- Webhooks on `push` events — triggers automatic graph refresh when code changes

**No write access.** The GitHub App cannot modify code, create branches, open PRs, or change settings.

**Credential storage:** `~/.pharaoh/credentials.json` — OAuth access token + refresh token. Tokens expire after 7 days with automatic refresh. Clear with `npx @pharaoh-so/mcp --logout`.

## Data & Privacy

**How parsing works:** Pharaoh clones your repos server-side using GitHub App installation tokens, then runs its [open-source parser](https://github.com/Pharaoh-so/pharaoh-parser) (tree-sitter based, MIT licensed) to extract structural metadata. **Source files are read during parsing** to build the AST. After parsing, cloned files are deleted from disk. The extracted metadata is:
- Function/class **names**, signatures, and export visibility
- File paths and module membership
- Import/export relationships and call chains
- Complexity scores (cyclomatic complexity)
- JSDoc/docstring text (encrypted at rest with per-tenant AES-256-GCM keys)

**What is NOT stored:** Source code bodies (function implementations, template literals, string contents, etc.). The graph contains names, paths, relationships, and scores. Source files are cloned temporarily for parsing, then deleted — they are not persisted or logged.

**Where data lives:** Neo4j knowledge graph on Neo4j Aura (cloud, GCP). Pharaoh is a remote service — your metadata is stored on Pharaoh's infrastructure, not locally. Each tenant's data is isolated via application-level repo-anchoring (every query scoped to your repos) and ownership checks. For self-hosted options, see [documentation](https://pharaoh.so/docs).

**Data retention:** Graph data persists while your account is active. Deleting a repo from Pharaoh purges all its nodes and relationships. Account deletion removes all tenant data.

**Network endpoints contacted:**
- `mcp.pharaoh.so` — MCP server (tool calls and responses)
- `github.com` — OAuth authorization and API calls (repo metadata, installation tokens)

## When to Use

After installation, the core `pharaoh` skill loads automatically in sessions where Pharaoh MCP tools are available. It teaches your agent to query architecture before reading files, check blast radius before modifying code, and search functions before creating duplicates. The 22 other skills are invoked on-demand by name.

## What You Get

**22 MCP Tools** — codebase map, module context, function search, blast radius, dependency queries, dead code detection, test coverage, regression risk, and more.

**23 Development Skills:**

| Category | Skills |
|----------|--------|
| **Core** | `pharaoh` (architectural habits, loads when MCP tools are present) |
| **Planning** | `pharaoh:plan`, `pharaoh:brainstorm`, `pharaoh:execute`, `pharaoh:sessions`, `pharaoh:parallel` |
| **Implementation** | `pharaoh:tdd`, `pharaoh:debug`, `pharaoh:refactor`, `pharaoh:investigate`, `pharaoh:explore` |
| **Verification** | `pharaoh:verify`, `pharaoh:wiring`, `pharaoh:review`, `pharaoh:review-receive`, `pharaoh:pr`, `pharaoh:review-codex` |
| **Maintenance** | `pharaoh:health`, `pharaoh:debt`, `pharaoh:audit-tests`, `pharaoh:onboard` |
| **Git** | `pharaoh:worktree`, `pharaoh:finish` |

## Setup Steps

1. **Install the GitHub App** on your org at [github.com/apps/pharaoh-so](https://github.com/apps/pharaoh-so) — grants read-only access to selected repos
2. Pharaoh auto-maps selected repos into a knowledge graph (typically < 5 minutes)
3. Run `npx @pharaoh-so/mcp --install-skills` — installs skills + connects MCP server
4. Authorize via the device code shown in terminal (opens GitHub OAuth in browser)
5. Your agent now queries architecture instead of reading files one at a time

## Uninstall

```bash
# Remove skills (installed by --install-skills)
rm -rf ~/.openclaw/skills/pharaoh*
# Remove MCP server entry from ~/.openclaw/openclaw.json (delete the "pharaoh" key under mcpServers)

# If using Claude Code directly (without OpenClaw):
claude mcp remove pharaoh

# Remove stored credentials
npx @pharaoh-so/mcp --logout
# or: rm ~/.pharaoh/credentials.json
```

## Links

- Documentation: https://pharaoh.so/docs
- GitHub (parser, open-source): https://github.com/Pharaoh-so/pharaoh-parser
- GitHub (MCP proxy): https://github.com/Pharaoh-so/pharaoh-mcp
- npm: https://www.npmjs.com/package/@pharaoh-so/mcp
- MCP Server: https://mcp.pharaoh.so
- Security contact: security@pharaoh.so
