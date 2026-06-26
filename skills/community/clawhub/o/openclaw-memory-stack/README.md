# OpenClaw Memory Stack

Guided memory routing for OpenClaw — so your agent remembers what matters.

---

## The Problem

OpenClaw's default memory works fine for small projects. But when conversations grow long, codebases get large, and decisions pile up, you hit the memory wall. Important context gets lost, decisions get re-made, and your agent starts from scratch every session.

## The Solution

Memory Stack bundles 2 researched memory backends with a rule-based router. Each query gets routed to the right backend — code search goes to BM25, recent context goes to git-based recall. No magic, just guided routing with clear rules.

We did the research so you don't have to.

---

## What's Included — Free & Open Source

| Component | What it does |
|-----------|-------------|
| **Memory Router** | Rule-based query routing with sequential fallback across all installed backends |
| **Total Recall** | Git-based memory — stores memories as markdown on an orphan branch. Zero dependencies beyond git |
| **QMD** | BM25 + vector search engine — keyword search, semantic search, and hybrid mode for code and docs |
| **Plugin integration** | Installs as OpenClaw's memory provider automatically — just restart and go |
| Quickstart guide | Get running in under 5 minutes |

MIT licensed. No purchase required.

---

## Quick Start

```bash
# 1. Install
./install.sh

# 2. Restart OpenClaw
openclaw gateway restart

# 3. Done — memory is now active
#    Just have a conversation. Memory Stack works automatically
#    as OpenClaw's memory backend.
```

**Want per-project code search?** That's optional and takes one extra step:

```bash
cd /path/to/your/project
openclaw-memory init          # sets up BM25 search for this project
openclaw-memory embed         # optional: enables vector search too
```

See [docs/quickstart.md](docs/quickstart.md) for the full setup guide.

---

## How Routing Works

The router matches your query against a rule table — keyword patterns, not AI classification. First match wins, and if the result is poor, it falls back to the next backend in the chain.

| Query type | Primary backend | Fallback |
|-----------|----------------|----------|
| Exact symbol: `find function parseAuth` | QMD (BM25 search) | Total Recall |
| Concept: `how does error handling work` | QMD (vector search) | Total Recall |
| Recent context: `what did we just discuss` | Total Recall | QMD |
| File/path: `in src/models/*.ts` | QMD (BM25 search) | Total Recall |
| Ambiguous: single words, vague references | QMD (hybrid) | Total Recall |

---

## How It Compares

Most AI memory systems make you choose between control and convenience.

| | Hermes Agent | Google Always-On | Memory Stack |
|---|---|---|---|
| **Routing** | Agent decides (opaque) | Google decides (black box) | 13 deterministic rules — inspectable |
| **Fallback** | None | Uncontrollable | Sequential chain — poor result → next backend |
| **Storage** | Developer-managed DB | Google cloud | Local git + SQLite — nothing leaves your machine |
| **Token control** | None | None | 3 tiers: ~100 / ~800 / full |
| **Deduplication** | Manual | Unknown | 4-level auto-dedup |
| **Offline** | Depends | No | Yes |
| **Open source** | Varies | No | MIT |

Hermes gives control but no routing infrastructure. Google gives convenience but no privacy. Memory Stack gives you both — deterministic, local, and debuggable.

---

## Platform Support

| Platform | Status |
|----------|--------|
| macOS | Fully tested. |
| Linux | Documented. Not fully validated at launch. |
| Windows | Not supported natively. Use [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install) (recommended) or Git Bash. |

---

## Honest Disclaimers

- **Rule-based routing, not AI-powered selection.** The router uses keyword pattern matching to pick backends. It does not understand your query semantically.
- **QMD requires Bun runtime.** Total Recall works everywhere git does. QMD needs [Bun](https://bun.sh) installed — it's free and open source, but it's an extra dependency.
- **macOS first.** Linux installation docs are included but not fully validated. If you hit issues on Linux, report them and we'll fix them.

---

## License

Commercial license — see [LICENSE](LICENSE).

---

## Support

Community — GitHub Issues
