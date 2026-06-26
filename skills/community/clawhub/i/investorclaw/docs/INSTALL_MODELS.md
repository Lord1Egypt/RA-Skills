# InstallModels — why two install patterns

> Status: design rationale, supersedes ad-hoc explanations in `README.md`
> and `RFC-v0.1.md`. Intended as the canonical answer to "why is the install
> story different for Claude Code than for OpenClaw / ZeroClaw / Hermes?"

## TL;DR

InvestorClaw v4.x ships under **one engine source** (`argonautsystems/ic-engine`)
that supports **two install models** at the agent boundary:

| Model | Used by (today) | Used by (eventual) | Where the engine runs |
|---|---|---|---|
| **Dockerized-skill** | OpenClaw, ZeroClaw, Hermes, Claude Code | OpenClaw, ZeroClaw, Hermes | A separate container; agents connect via MCP-HTTP |
| **Native-workspace SKILL.md** | (none yet) | Claude Code (post Anthropic marketplace approval) | In-process inside the agent's workspace via uv-managed venv |

Both paths consume the same `ic-engine` source, the same FINOS-CDM
data model, and produce identical envelope shapes. The split exists because
the four agent runtimes have fundamentally different process and security
models, and forcing them into a single install convention costs more than it
buys.

This document explains why.

---

## 1. The four agent runtimes are not the same shape

| Runtime | Architecture | Workspace concept | Native skill format |
|---|---|---|---|
| **Claude Code** | CLI per workspace, runs in user's shell | Yes — `~/.claude/agents/`, project `./skills/`, `~/.claude/skills/` | `SKILL.md` (AgentSkills spec, in-process) |
| **OpenClaw** | Long-running gateway daemon, multi-channel router | No — gateway-scoped plugin manifest | `openclaw.plugin.json` + TS code |
| **ZeroClaw** | Container-friendly chat gateway | No — config.toml driven | TOML config snippet |
| **Hermes** | Python agent runtime, model router | No — yaml config driven | YAML config snippet |

The asymmetry: **Claude Code is the only one that natively reads a SKILL.md
from a user-owned workspace and treats it as installable in-process.** The
other three are gateway-style daemons. They don't have a "workspace" concept
that maps to AgentSkills folder layouts. They have plugin/extension systems
with their own conventions.

If you wanted to ship the InvestorClaw engine as an in-process plugin to all
four runtimes, you'd need:

- A TypeScript plugin shim for OpenClaw (its plugin SDK is TS/Node)
- A TOML/Python install path for ZeroClaw
- A YAML/Python install path for Hermes
- A SKILL.md path for Claude Code

That's roughly the v2.6.x architecture. Each path was independently broken
by upstream runtime releases roughly every two weeks. The 2026-04-30 fleet
barrage on TYPHON-Windows-WSL caught **6/30** for OpenClaw, **6/30** for
Hermes, **21/30** for ZeroClaw, against a Linux baseline of 26/30 / 23/30 /
30/30. **Every failure was install friction, not analytical capability.**

The v4.x decision: stop building four different install paths to the same
engine. Build one engine, expose it over a universal contract, let each
runtime choose how to talk to it.

That contract is **MCP-HTTP**.

---

## 2. The dockerized-skill convention (works for all four today)

**Architecture:**

```
   ┌─────────────────────────────────────────┐
   │  ic-engine container                    │
   │  ────────────────                       │
   │  ghcr.io/argonautsystems/ic-engine:4.7.7-cpu  │
   │                                         │
   │  - Python 3.12 venv (uv-managed)        │
   │  - Engine source (ic-engine HEAD)       │
   │  - Bridge: FastMCP HTTP server          │
   │  - Dashboard: dash + plotly             │
   │                                         │
   │  Listens on:                            │
   │    18090/mcp     (MCP-HTTP, agents)     │
   │    18092/        (dashboard, browser)   │
   └────────────────┬────────────────────────┘
                    │
                    │  MCP over HTTP (streamable-http transport)
                    │
        ┌───────────┴────────────┬─────────────────────┬─────────────────────┐
        │                        │                     │                     │
   ┌────▼─────┐            ┌────▼─────┐         ┌─────▼────┐         ┌──────▼───┐
   │ OpenClaw │            │ ZeroClaw │         │  Hermes  │         │  Claude  │
   │ gateway  │            │  daemon  │         │  router  │         │   Code   │
   └──────────┘            └──────────┘         └──────────┘         └──────────┘
   "mcpServers" config     [mcp] config         tools.config          .mcp.json
   each agent points at http://localhost:18090/mcp
```

**What this buys:**

- One source of truth for the engine. Engine bugs get fixed once. Image
  releases ship via `docker compose pull`, no per-runtime npm/pypi/whatever.
- **The engine never embeds runtime-specific code.** No TS shim, no per-
  runtime config patcher, no install.sh. The engine doesn't know or care
  which agent is calling it.
- **The runtime never embeds engine-specific code.** OpenClaw's plugin
  catalog isn't polluted with TypeScript that wraps a Python skill. ZeroClaw's
  config doesn't carry a Python venv path. Hermes doesn't pip-install
  anything outside its own dependency tree.
- Trust boundary becomes the docker socket + the MCP HTTP endpoint. Both are
  well-defined, both are auditable.

**What this costs:**

- Users have to run Docker (or Podman, or any OCI runtime). For the runtimes
  that already require Docker (OpenClaw production, Hermes when paired with
  vLLM, etc.), this is no cost. For Claude Code users on a fresh laptop, this
  is one extra prerequisite — which is the exact thing the native-workspace
  install model below removes for them specifically.
- Two processes (agent + engine) instead of one. They communicate over HTTP
  on localhost, ~5ms overhead per call. Well within budget for a portfolio
  analyzer that takes 30-180s per refresh.

**Per-runtime SKILL.md files** (`agent-skills/{openclaw,zeroclaw,hermes,
claude-code,claude-desktop}/`) are *hint files for the user* — they say
"copy this snippet into your runtime's MCP config." They are not the install
itself. The install is `docker compose up`.

This is the entirety of v4.x today. All cobol regression validation runs
through this path: **245-249/250 (98-99%)** on baked images.

---

## 3. The native-workspace SKILL.md model (Claude Code, eventually)

Claude Code is unique in that it **already** supports SKILL.md as a first-class,
in-process install via the AgentSkills spec. Drop a `SKILL.md` with frontmatter
+ instructions into `~/.claude/agents/<name>/`, restart, and Claude Code reads
it natively. The skill author can specify a uv-managed venv, scripts to run,
and tools the agent should expose.

Today InvestorClaw's Claude Code / Claude Desktop plugin uses the dockerized-skill
path because it's the only path that's fleet-aligned. Claude Code installs
the engine via the same MCP-HTTP contract as the other three runtimes.

**Eventually** — once Anthropic approves InvestorClaw for the Claude Code
marketplace and the marketplace exposes a path that auto-installs both the
SKILL.md AND the supporting Python venv — Claude Code gets a second native
install model:

```
   ┌─────────────────────────────────────────────────┐
   │  Claude Code workspace                          │
   │  ─────────────────────                          │
   │  ~/.claude/agents/investorclaw/                 │
   │    SKILL.md          (AgentSkills frontmatter)  │
   │    pyproject.toml    (declares ic-engine dep)   │
   │    .venv/            (uv-managed, in workspace) │
   │                                                 │
   │  Engine runs in-process, no container needed.   │
   │  Tool calls dispatched via Claude Code's        │
   │  native skill-tool bridge.                      │
   └─────────────────────────────────────────────────┘
```

**What that buys (Claude Code users specifically):**

- No Docker prerequisite. uv handles Python; Claude Code handles the agent.
  One install command, one process tree.
- Faster boot. Engine starts when the skill is first invoked, no docker
  daemon warmup, no compose start latency.
- Tighter integration. Slash commands like `/investorclaw:refresh` map
  directly to ic-engine entrypoints with no MCP-HTTP marshaling.
- Workspace-scoped state. Per-project portfolio data lives in the workspace,
  not in a global docker volume.

**Why this isn't a regression to v2.6.x's "four install paths":**

- The engine source stays in `argonautsystems/ic-engine`. Single source of
  truth.
- The Claude-Code-native install path is built **on top of** the same engine,
  not as a fork. It depends on `ic-engine` as a published Python package
  (post-marketplace), not as an in-repo Python tree.
- The other three runtimes never gain a native-workspace install. They stay
  on dockerized-skill, which is the right model for daemon-style runtimes.
- The SKILL.md in this runtime repo (the one ClawHub publishes) and the
  SKILL.md in the future Claude Code marketplace skill are different files
  serving different runtimes — but both reference the same engine and produce
  the same envelopes. Cobol regression validates both.

The native-workspace path is **not** in scope today. It's blocked on:

1. Anthropic marketplace approval for InvestorClaw
2. `ic-engine` published as a versioned wheel (currently git-installed)
3. A separate workspace skill that wraps the wheel

Tracking as task #50 in the project queue (post-stable).

---

## 4. The single contract: MCP-HTTP + ic-engine envelopes

Whichever install model the runtime uses, the contract between agent and
engine is the same:

- **Tool calls** go over MCP. (HTTP for dockerized-skill; in-process via
  Claude Code's tool bridge for native-workspace.)
- **Tool responses** carry a JSON envelope with: `sections.{performance,
  bonds, news, holdings, ...}`, `ic_result.{hmac, run_id, command,
  engine_version}`, narrative text from a no-fabrication validator.
- **Mode classifier** (portfolio-strict / concept / market / setup) lives
  in the engine, not the runtime. Routes the same way regardless of caller.
- **Tightened cobol verdict** validates both paths against the same 250-NLQ
  regression set.

This means an InvestorClaw skill author writes one analyzer that runs in
either install model. A user who switches from OpenClaw + dockerized-skill
to Claude Code + native-workspace gets the same answers, the same precision,
the same audit trail. The transport changes; the math doesn't.

---

## 5. Why this matters operationally

**v2.6.x lifecycle of a bug fix (per-runtime install paths):**

1. Fix the bug in `InvestorClaw` Python.
2. Bump version in `pyproject.toml`.
3. Bump version in `openclaw.plugin.json`, `package.json`, `SKILL.toml`,
   `package-lock.json`, `investorclaw.py` shim.
4. Rebuild TS plugin (`npm run build`).
5. Push to `npm` for OpenClaw consumers.
6. Update each per-runtime `install.sh` to point at the new version.
7. Each runtime user runs the install procedure for THEIR runtime.
8. Six install paths drift; one quietly breaks under a runtime upgrade.

**v4.x lifecycle of a bug fix (dockerized-skill):**

1. Fix the bug in `argonautsystems/ic-engine`.
2. Build + push `ghcr.io/argonautsystems/ic-engine:X.Y.Z-cpu`.
3. Bump `compose.yml` image tag in `mnemos-os/mnemos-ic-runtime`.
4. Each runtime user runs `docker compose pull && docker compose up -d`.
5. All four runtimes get the fix on the same image SHA.

The first lifecycle takes hours and is fragile. The second takes minutes and
is atomic. The dockerized-skill convention exists primarily to enforce the
second one for runtimes that don't support a native workspace install path.
For runtimes that DO (Claude Code, eventually), the workspace install will
be a strictly faster path layered on top — not an exception to it.

---

## 6. References

- `RFC-v0.1.md` — full v4.0 architecture specification (this doc is the
  why-not-how complement)
- `SKILL.md` — the runtime SKILL.md ClawHub publishes
- `agent-skills/*/SKILL.md` — per-runtime install hint files (MIT-0)
- `argonautsystems/ic-engine` — engine source of truth (https://github.com/argonautsystems/ic-engine,
  build mirror at https://gitlab.com/argonautsystems/ic-engine)
- AgentSkills spec — https://agentskills.io
- ClawHub — https://clawhub.ai (skill registry, Apache 2.0 + MIT-0)
- MCP spec — https://modelcontextprotocol.io
