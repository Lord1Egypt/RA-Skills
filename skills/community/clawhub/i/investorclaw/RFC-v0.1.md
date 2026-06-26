# RFC v0.1 — InvestorClaw 4.1.22 Application Service Architecture

**Status:** Draft (pre-implementation)
**Author:** Claude (jperlow@gmail.com), in collaboration with the user
**Date:** 2026-04-30
**Supersedes:** the v2.6.3 skill-bundle install model
**Cross-references:**
- `project_investorclaw_v4_0_pivot_2026_04_30.md` (full strategic memory)
- `feedback_v4_0_engine_deterministic_no_llm_in_parse.md`
- `feedback_v4_0_agent_driven_install.md`
- `feedback_v4_0_license_slot_apache_mit_split.md`
- `project_ic_engine_v4_0_audit_2026_04_30.md` (ic-engine already deterministic)
- GRAEAE consultation `f1bea48c-f6c6-42eb-b741-0594079fedcb` (architecture review)

---

## 1. Context — what changed and why

InvestorClaw v2.x ships as a **skill bundle** that installs INTO each agent
runtime container (openclaw, zeroclaw, hermes, claude code). Each agent does
its own `uv sync`, npm install, PATH symlinks, plugin manifest registration,
config patching. The 2026-04-30 TYPHON Windows-WSL Docker barrage hit
**21/30 / 6/30 / 6/30** vs the 2026-04-28 Linux v2.5.0 baseline of
**26/30 / — / 23/30 / 30/30 (InvestorClaude)**. Every failure was install
friction, not analytical capability. Eight hours of debugging produced
~12 fixable bugs, and the underlying pattern was clear: **shipping the same
analytical engine four different ways per release cycle, against four
different agent runtimes that each rev breaking changes every ~2 weeks, is
a permanent maintenance tax that no patching strategy escapes.**

The v4.0 pivot inverts the dependency. The analytical engine ships **once**,
as a containerized service. Every agent runtime connects to it via MCP-HTTP
(an Anthropic-stewarded, versioned, broadly-adopted spec). Agents can churn
their internals as much as they want — as long as they keep speaking MCP,
the service stays compatible.

This RFC captures the architecture that emerged from that pivot session.

## 2. Goals

- **Drift-proof:** one stable interface (MCP-HTTP) instead of four volatile
  per-agent install paths.
- **Self-contained + deterministic:** the container ships with everything it
  needs (parsers, market data fetchers, analyzers, dashboard, MCP server,
  sqlite, mnemos-lite). No LLM call in the data extraction path. Unknown
  formats return structured errors, never LLM disambiguation.
- **Agent-side artifact reduces to a single MIT-licensed SKILL.md** plus one
  MCP server config block. No bundle, no plugin manifest, no Python on the
  agent side.
- **Agent-driven install:** the user's existing agent (Claude, zeroclaw,
  etc.) executes the install via its existing shell + Edit tools reading a
  canonical compose.yml from a stable URL. No native installer codebase.
- **Cloud-ready:** same compose.yml deploys on user laptop / Pi / homelab
  VPS / cloud VM / managed multi-tenant SaaS. Unlocks the SaaS revenue
  ladder.
- **Web dashboard served by the container** at `:8092` — config UI, portfolio
  upload, agent connect wizard, bundle import/export, diagnostics. Not a
  separate native app.
- **30/30 ship gate** N=3 on Tier-1 (Claude + zeroclaw on master) becomes
  empirically achievable because all install friction is eliminated.

## 3. Non-goals

- Not a rewrite of ic-engine (Python stays Python; existing analytical code
  lands in the container as-is).
- Not a rewrite of mnemos (Python server tier continues separately under
  mnemos-claude's ownership).
- Not a new MCP spec. We're using existing MCP unmodified, plus a
  documented Docker Compose convention.
- Not a native desktop installer (no Tauri / Electron / MSI / PKG / DEB).
  `docker compose up` is the install.
- Not a vendor lock-in to any specific agent runtime. The architecture is
  agent-agnostic; Claude and zeroclaw are *recommended*, not required.

## 4. Architecture overview

```
HOST (laptop / Pi / homelab VPS / cloud VM)
┌──────────────────────────────────────────────────────────────────┐
│  docker-compose:                                                 │
│                                                                  │
│  mnemos-os/mnemos-rs:4.2  (Rust, sqlite, ~30-50 MB image)        │
│  ┌──────────────────────┐                                        │
│  │  MCP-HTTP :5002      │  /data/mnemos.db (sqlite WAL)          │
│  │  search/create/list   │                                        │
│  └──────────────────────┘                                        │
│           ▲                                                      │
│           │ HTTP (compose bridge net)                            │
│           │                                                      │
│  ┌──────────────────────┐                                        │
│  │  ic-engine:4.1.22-cpu       │  /data/ic-engine.db (sqlite WAL)       │
│  │  Python 3.12 +        │  /data/portfolios/                     │
│  │  pandas/numpy/scipy   │  /data/keys.env (mode 0600)            │
│  │  + ic-engine pinned   │  /data/reports/                        │
│  │                       │                                        │
│  │  MCP-HTTP :8090       │                                        │
│  │  Dashboard :8092      │                                        │
│  │  MnemosClient → :5002 │                                        │
│  └──────────────────────┘                                        │
│           ▲                                                      │
│           │ MCP-HTTP                                             │
│           │                                                      │
└───────────┼──────────────────────────────────────────────────────┘
            │
   ┌────────┴───────┬──────────┬────────────┬────────────┐
   │ Claude Code    │ zeroclaw │  openclaw  │  hermes    │
   │ Claude Desktop │ (master) │            │            │
   │ (Tier-1)       │ (Tier-1) │  (Tier-2)  │  (Tier-2)  │
   └────────────────┴──────────┴────────────┴────────────┘
   Each agent registers BOTH MCP servers in its config (mnemos + ic-engine).
   The LLM sees `mnemos.search_memories`, `investorclaw.portfolio_ask`, etc.
   as separate tool namespaces. Clean discovery, no umbrella gateway needed.
```

### Why two containers, not one fat image

Bundling Python ic-engine into Rust mnemos-rs (via PyO3 / subprocess pool /
embedded CPython) costs the lean Rust binary advantage and pulls Python
ABI complexity into the desktop tier. Instead: each container is
single-language, single-runtime, single-purpose. They communicate via
HTTP/MCP over compose's bridge network — the same wire format both speak
natively. `docker compose up` is the user-facing artifact regardless.

This is also the **GENERIC EXTENSION SUBSYSTEM** pattern — ic-engine is the
first instance. Future Python tools (riskyeats, etlantis, etc.) each get
their own `mnemos-<name>-runtime` repo using the same two-container
pattern. mnemos-rs stays Rust + lean; each Python tool stays Python +
free to use whatever scientific stack it wants.

## 5. Compose convention (x-mcp-services)

InvestorClaw 4.1.22 distribution = a single `compose.yml` at a stable URL
(`https://raw.githubusercontent.com/mnemos-os/mnemos-ic-runtime/main/compose.yml`) with two extension keys
that describe the MCP servers:

```yaml
x-mcp-services:                              # Compose ignores x-* keys; tools read them
  investorclaw:
    transport: http
    url: http://127.0.0.1:8090/mcp
    description: "Portfolio analysis (FINOS CDM 5.x deterministic)"
    health: http://127.0.0.1:8090/healthz
  mnemos:
    transport: http
    url: http://127.0.0.1:5002/mcp
    description: "Memory + knowledge graph"
    health: http://127.0.0.1:5002/healthz

x-mcp-service-meta:
  version: "4.0"
  bundle_url: https://raw.githubusercontent.com/mnemos-os/mnemos-ic-runtime/main/v4.0/install.yaml
  dashboard: http://127.0.0.1:8092/
  required_keys: []
  optional_keys: [TOGETHER_API_KEY, FINNHUB_KEY, FRED_API_KEY, NEWSAPI_KEY]

services:
  mnemos:
    image: mnemos-os/mnemos-rs:4.2
    volumes: [data:/data]
    ports: ["5002:5002"]

  ic-engine:
    image: mnemos-os/ic-engine:4.1.22-cpu
    volumes: [data:/data]
    environment:
      MNEMOS_BASE: http://mnemos:5002
    ports: ["8090:8090", "8092:8092"]
    depends_on: [mnemos]

volumes:
  data:
```

This is **not a new spec** — it's a documented use of Compose's existing
`x-*` extension key mechanism (Compose ignores them by design). Tools that
implement the convention (like `zeroclaw services install`) read the
extension keys; tools that don't simply run `docker compose up` and ignore
the manifest. **Adoption friction approaches zero.** Service author writes
one compose.yml with two `x-*` blocks; install-tool author reads two `x-*`
blocks. No standards body, no spec doc, no working group.

### Distribution

A few static files at a CDN. **Entire** distribution surface:

- `/v4.0/compose.yml` — what `docker compose up` reads
- `/v4.0/install.yaml` — derived view (ordered shell steps for shell-tool
  agents that don't have native Docker integration)
- `/v4.0/skill.md` — MIT-licensed agent-readable installer instructions

No installer codebase. No platform-specific packaging. No code-signing.
No App Store dance.

## 6. ic-engine container

**Base:** `python:3.12-slim`. **Build:** `uv sync --python 3.12` against a
pinned `argonautsystems/InvestorClaw` SHA. **Image size target:** 250-400 MB.

**Ships with:**
- All format converters (UBS xls/xlsx, Schwab CSV, Vanguard CSV, Fidelity
  CSV, E*TRADE CSV, Robinhood CSV, generic-CSV-with-column-map, PDF via
  pdfplumber, OFX via ofxtools) — all deterministic, header-signature
  classified.
- All market data fetchers (yfinance default, FRED, Finnhub, NewsAPI,
  Alpha Vantage, massive.com / Massive — all gracefully degrade if keys
  absent).
- All ic-engine analyzers (PerformanceAnalyzer, BondAnalyzer with FRED
  yield curve, AnalystFetcher, NewsAnalyzer, PortfolioAnalyzer, Optimizer,
  PeerAnalyzer).
- Narrative synthesis layer (configurable: heuristic / local LLM / cloud
  LLM / off — already implemented in `rendering/stonkmode.py`,
  per `project_ic_engine_v4_0_audit_2026_04_30.md`).
- FastMCP server at `:8090/mcp` exposing 15+ tools (one per ic-engine
  command verb).
- Dashboard static files served at `:8092/` (web app — vanilla JS or
  preact, no build pipeline complexity).
- MnemosClient HTTP wrapper to mnemos-rs container.
- BundleImporter / BundleExporter (atomic two-file rename for cross-DB
  consistency, per GRAEAE recommendation).
- Auth: localhost-only by default; token-auth for remote.
- Sqlite + WAL at `/data/ic-engine.db`.

**Per the deterministic-engine constraint:** no LLM call in the parse/extract
path. Confirmed: ic-engine v2.6.3 already meets this (zero LLM imports in
`commands/`; LLM HTTP calls isolated to `rendering/stonkmode.py` narrative
layer). For v4.0, the narrative-tier provider config moves from env vars
to dashboard-driven config (small refactor, same code path).

## 7. mnemos-rs container

**Base:** `scratch` or `alpine` (minimal). **Build:** Rust 2024 edition,
sqlite, axum (HTTP). **Image size target:** 30-50 MB. **RSS target:** ~52 MB
per the desktop-tier envelope mnemos-claude is enforcing.

**Ships with:**
- Rust binary serving MCP-HTTP at `:5002/mcp`
- Sqlite at `/data/mnemos.db` (WAL mode)
- Memory tools: `search_memories`, `create_memory`, `list_memories`,
  `update_memory`, `delete_memory` (matching the Python server's tool
  catalog where it makes sense at desktop scale)
- Bundle import/export for memories portion of the bundle
- Auth: localhost-only by default; token-auth for remote
- `mnemosctl` CLI bundled or as separate binary in same image (TBD per
  codex orientation findings)

Mnemos-rs is mine to drive. Coordination boundary with mnemos-claude:
the public Python API + MCP tool catalog + schema migrations spanning
both desktop+server.

## 8. Bundle.json v4.0 schema

The bundle is **the dashboard's config state + data references** in a JSON
file. Drag-drop into the dashboard to import / export to back up. Same
fields, same validation, two interfaces.

**Critical security property:** API keys NEVER stored as raw values.
Always env-var **references**:

```json
{
  "version": "4.0",
  "providers": {
    "together": {
      "api_key_ref": "$TOGETHER_API_KEY",
      "default_model": "MiniMaxAI/MiniMax-M2.7"
    },
    "openai": {
      "api_key_ref": "$OPENAI_API_KEY",
      "default_model": "gpt-5"
    }
  },
  "data_sources": {
    "finnhub": { "api_key_ref": "$FINNHUB_KEY" },
    "fred":    { "api_key_ref": "$FRED_API_KEY" }
  },
  "portfolios": [
    {
      "id": "ubs_taxable",
      "source_file": "portfolios/ubs_07_04_2026.xls",
      "broker": "ubs",
      "account_type": "taxable"
    }
  ],
  "narrative": {
    "tier": "auto",
    "depth": "standard",
    "provider_route": "together"
  },
  "mcp": {
    "bind": "127.0.0.1",
    "port": 8090,
    "auth_token_ref": "$IC_MCP_TOKEN"
  },
  "memory": {
    "retention_days": 365,
    "embedding_model": "all-MiniLM-L6-v2"
  },
  "metadata": {
    "exported_at": "2026-04-30T...",
    "from_host": "studio.local"
  }
}
```

Resolved at runtime from `/data/keys.env` (mode 0600). Bundle.json is
safe to back up to git, share with co-admin, etc., because it never
contains secrets.

**Atomic cross-DB import** (per GRAEAE consultation `f1bea48c`): bundle
import touches BOTH `mnemos.db` and `ic-engine.db`. The import process
must be transactional across two sqlite files:

1. Import to temp files: `mnemos.db.tmp`, `ic-engine.db.tmp`
2. Validate both
3. Atomically rename both into place

If validation fails OR rename fails: leave existing dbs untouched. ~30
LOC, design-in-now to prevent the first-bundle-import-corrupted-state
support ticket.

## 9. Agent integration

**Agent-side artifact = a single MIT-licensed `SKILL.md` + one MCP server
config block.** No bundle, no plugin manifest, no Python on the agent
side.

For each Tier-1 / Tier-2 agent:

| Agent | Config file | MCP block |
|---|---|---|
| Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` (mac) / `%APPDATA%\Claude\claude_desktop_config.json` (win) | `mcpServers.{investorclaw,mnemos}` JSON entries |
| Claude Code (marketplace) | bundled in v4.0 thin-client plugin | same |
| zeroclaw (master) | `~/.zeroclaw/config.toml` | `[mcp.servers.{investorclaw,mnemos}]` TOML blocks |
| openclaw 4.29-beta.4 | `openclaw mcp set` CLI or `~/.openclaw/openclaw.json` `mcp.servers` | both work |
| hermes 0.12 | `~/.hermes/config.yaml` `mcp_servers:` | YAML entry |

The dashboard's "Connect an agent" wizard generates these blocks per
detected agent and offers copy-paste or one-click write (with permission).

### Agent-driven install (the elegant loop)

```
User: "What's in my portfolio?"

Agent (notices investorclaw MCP server isn't responding):
  "I don't have InvestorClaw set up yet. Want me to install it? ~30s, requires Docker."

User: "Yes"

Agent (executes via its existing shell + Edit tools):
  1. docker --version                        # verify prereq
  2. mkdir -p ~/.investorclaw
  3. curl -sSL https://raw.githubusercontent.com/mnemos-os/mnemos-ic-runtime/main/compose.yml > ~/.investorclaw/compose.yml
  4. cd ~/.investorclaw && docker compose up -d
  5. wait_for http://127.0.0.1:8090/healthz
  6. write its own MCP server config (file Edit, runtime-specific path)
  7. reload config / restart
  8. retry the original query

Agent: "InvestorClaw is set up. Drop your portfolio CSV at http://localhost:8092 — or I can guide you through it here."
```

Each agent's existing trust model gates this naturally. **No new trust
model, no new code. The agent IS the installer.**

## 10. Dashboard

**Single-page web app served by ic-engine container at `:8092/`.** Vanilla
JS or preact (small footprint, no build pipeline).

**Sections:**

1. **First-run wizard:** portfolio upload (drag-drop) → keys/providers →
   connect-an-agent (copy-paste configs for Tier-1 + Tier-2) → done
2. **Portfolio:** holdings table, performance, accounts breakdown, refresh
   button (calls investorclaw_refresh server-side, no file upload needed)
3. **Providers / Keys:** Together / OpenAI / Anthropic / Groq / etc. with
   "test" buttons + last-known-good timestamps; per-purpose routing
   (narrative vs consult vs stonkmode)
4. **Data Sources:** Finnhub, FRED, NewsAPI, Alpha Vantage, massive.com
5. **Narrative tier:** heuristic / local-LLM / cloud-LLM / auto + depth
   slider
6. **MCP Server:** bind addr, port, auth token (display / regenerate /
   revoke), connected-agents list ("openclaw last seen 30s ago")
7. **Memory (mnemos):** retention, categories, embedding model
8. **Bundle:** export download, import upload, auto-backup schedule
9. **Diagnostics:** live MCP request stream, tool call log, sqlite db
   sizes, container resource usage

**Auth model:**
- Local-host deploy (default): container binds `127.0.0.1`. No auth needed.
- Remote deploy (Tailscale / cloud VM): container binds `0.0.0.0`,
  one-time setup token shown on first start, stored as cookie + bearer.

## 11. License slot

| Artifact | License |
|---|---|
| `argonautsystems/InvestorClaw` (ic-engine source) | Apache 2.0 |
| `mnemos-os/mnemos-rs` (Rust desktop, mine) | Apache 2.0 |
| `mnemos-os/mnemosctl` (CLI, mine) | Apache 2.0 |
| `mnemos-os/mnemos-ic-runtime` (this repo: bridge code, MnemosClient, Dockerfile) | Apache 2.0 |
| **`SKILL.md`** at distribution edge | **MIT** |
| **`install.yaml`** | **MIT** |
| **`compose.yml`** at `raw.githubusercontent.com/mnemos-os/mnemos-ic-runtime/main/` | **MIT** |
| Trademark on "InvestorClaw" name | (separate from copyright) |

Distribution-edge artifacts are MIT for max redistributor friction-free
redistribution. Substantive code is Apache 2.0 (patent grant, NOTICE).
SKILL.md must be **rewritten from scratch** for v4.0 — never paste
verbatim from existing Apache 2.0 COMMANDS.md / CAPABILITIES.md.

Per `feedback_v4_0_license_slot_apache_mit_split.md`.

## 12. Security model

- **API keys never in bundle.json** — references only.
- **Keys mounted from `/data/keys.env`** at container startup, mode 0600.
- **Agent containers have ZERO Python, ZERO API keys, ZERO portfolio
  data.** Agents are pure MCP clients.
- **Compromised agent can call MCP tools** but cannot exfiltrate raw
  portfolio files, raw API keys, or anything outside the MCP API surface.
- **Network egress concentrated in one container.** ic-engine is the
  only container making upstream calls (Together, FRED, Finnhub, etc.) —
  iptables / Tailscale ACL / egress proxy can govern that single boundary.
- **Audit log centralized.** One container, one append-only sqlite +
  file log. `sqlite3 ic-engine.db ".dump audit_log"` is the entire
  forensic surface.
- **Localhost-only default.** Dashboard + MCP servers bind `127.0.0.1`
  unless explicitly opened.
- **Token auth for remote deploys.** Required when binding to `0.0.0.0`.
  Same pattern Claude Desktop's MCP server uses.

For enterprise futures: mTLS / OIDC / SAML at the MCP-HTTP layer drops
in **at one boundary** instead of four.

## 13. Compatibility test harness (cutover gate)

Per GRAEAE consultation `f1bea48c`: build a harness that feeds the same
30 cobol prompts to both v2.6.3-skill (current marketplace submission)
and v4.0-service (the new container), diffs **raw tool outputs** (not
agent responses — those are non-deterministic — but underlying portfolio
calculations + memory retrievals + ic_result envelopes).

- **Byte-identical:** cutover gate met, ship v4.0 with confidence.
- **Divergent:** bugs found pre-ship that would otherwise show up as
  mysterious score regressions post-cutover.

This harness is also the v4.x → v4.0 release verification: when v4.0
service produces analytically equivalent outputs to v2.6.3 skill bundle,
v4.0 is validated for migration.

## 14. Ship gates

| Gate | Threshold |
|---|---|
| **v4.0 ship gate** (Tier-1) | 30/30 N=3 on Claude AND 30/30 N=3 on zeroclaw master |
| **v4.0 publish gate** (Tier-2) | ≥ 27/30 N=3 each on openclaw, hermes |
| **v4.0 advisory** (Tier-3) | reserved for future agents that can't fully speak MCP |
| **Compat test harness gate** | byte-diff v2.6.3 ↔ v4.0 for cutover |

Hermes likely jumps significantly in v4.0 vs the 6/30 today — the HER-1
architectural caveat ("skills are doc-hints, not first-class tools") gets
neutralized when there's no skill bundle to inject as a doc-hint; the
LLM sees an MCP server with first-class tool calls.

## 15. Migration path

| Track | What it is | Lifecycle |
|---|---|---|
| **2.x** | skill-bundle install path | v2.6.3 is final ship. 2.x branch frozen. Security backports only. Marketplace submission stays in review; lands or is rejected on its own. |
| **3.x** | Phase 3A enterprise tier on v2.x architecture (audit ledger, party hierarchies, RBAC, EMIR/MiFID exports) | Continues independently for compliance customers who can't containerize. mnemos-claude / user co-own. |
| **4.x** | Application service architecture | This RFC. Greenfield. Ships when ship gate met. |

Existing v2.x users:
- Can stay on v2.6.3 indefinitely (it's a final ship, not deprecated as
  unsupported).
- Can migrate to v4.0 at their pace once the container service is
  available — zero functional regressions per the compat-test harness.
- Cannot run v2.x and v4.0 simultaneously on the same agent (the agent's
  MCP config either points at the local skill bundle or the v4.0 service
  — pick one).

## 16. Open questions (filled as codex orientation lands)

The codex agent `afb4a5aef499ad7b9` (sub-task `br8e7gdf8`) is currently
running a read-only orientation pass on:
1. mnemos-rs current state (skeleton vs partial vs working; transports;
   sqlite layer; public API)
2. mnemosctl scope (where it lives; command surface)
3. mnemos-production v4.2.0a1 + `feat/persistence-sqlite` +
   `feat/single-binary-build` branches
4. zeroclaw master `[mcp]` config schema + DockerSandbox interface
5. ic-engine LLM-in-parse-path audit (resolved separately at
   `project_ic_engine_v4_0_audit_2026_04_30.md` — clean, no
   refactor needed)

The findings from items 1-4 will fill in:
- mnemos-rs Rust types for the public Python API mirror — concrete trait
  definitions, sqlite schema details
- The exact `[mcp]` config block format on zeroclaw master (so the
  dashboard's "Connect zeroclaw" wizard generates the right TOML)
- Whether `zeroclaw services install` is greenfield or builds on existing
  patterns (affects upstream PR scope)
- Whether mnemos-rs needs an MCP-HTTP transport layer added or already
  has one

Once the orientation lands, this section gets removed and the
implementation specifics get filled into sections 6, 7, and 9.

## 17. Risks

- **MCP spec evolves and breaks our wire compatibility.** Mitigation:
  pin to a stable MCP version, track Anthropic announcements, ship
  compat-test harness checks in CI.
- **Anthropic publishes a competing service-discovery / install
  spec.** Our convention is light enough (just compose `x-*` keys) to
  layer alongside or migrate cleanly.
- **Container resource overhead deters Pi / edge users.** The two-image
  size (~300-450 MB combined) is acceptable for laptop / homelab; bigpi
  has 16 GB and runs three agents already — ic-engine + mnemos-rs is
  small comparison. Pi Zero / 2 GB Pi: out of scope for v4.0; v2.x
  remains.
- **First-run UX failure modes** — Docker not installed, port conflicts,
  permission issues, stale image pulls. Compat-test harness covers
  the happy path; KNOWN_ISSUES.md collects the operator-facing
  caveats.

## 18. Prior art / references

- Helm charts (Apache 2.0) for Kubernetes (Apache 2.0) — same MIT/Apache
  pattern, except Helm itself is Apache.
- Docker Compose as a deploy spec — used at `compose.yml` level.
- MCP specification — Anthropic-stewarded, transport-agnostic.
- mnemos v4.2.0a1 — the substrate this builds on.
- v2.5.0 fleet baseline (2026-04-28) — the empirical numbers v4.0
  must match or exceed.
- v2.6.3 final ship (2026-04-30, this conversation) — the architecture
  v4.0 supersedes.

---

## Appendix A — Open task family mapping

This RFC maps to tasks #41, #42, #43, #44, #45, #46, #47, #48, #49 in
the session task list. See `MEMORY.md` for the full v4.0 task family.
