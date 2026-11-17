# 🧠 Memoria

**Local, multi-agent memory for AI assistants.** Your agents (Claude Code, Codex, OpenClaw, …) each get their own private, persistent memory — sharing only what you decide. 100% local, zero cloud, open source.

> *Human-machine memory is our memory. Local, ours, and it never starts from zero.*

**Status: public beta** — V3 in active development on the `memoria-v1` branch, a ground-up rebuild of the former OpenClaw plugin (now archived in [`legacy/`](legacy/)). See [`docs/v3/STATUS.md`](docs/v3/STATUS.md) for live progress.

## Install (macOS)

One command in the Terminal — requires [Node.js 22 LTS](https://nodejs.org):

```sh
curl -fsSL https://raw.githubusercontent.com/Primo-Studio/openclaw-memoria/memoria-v1/scripts/install-memoria.sh | sh
```

The script checks prerequisites, installs Memoria, starts the local service (auto-start at login) and opens the web UI. From there the onboarding guides you: pick your intelligence engine (Ollama recommended — free and 100% local — or LM Studio, or an OpenAI/OpenRouter/Anthropic API key), detect the agents on your machine, connect them in one click and optionally import their existing memories. Reopen the UI anytime with `memoria ui`, update with `memoria update`.

🌐 **Website:** [primo-studio.fr/app/memoria](https://primo-studio.fr/app/memoria) · 🐛 [Report a bug](https://github.com/Primo-Studio/openclaw-memoria/issues)

---

## Why V3

The previous Memoria was an OpenClaw plugin, coupled to its host's hooks — and an OpenClaw update broke it. V3 fixes that at the root:

- **`@memoria/core`** — the engine. No host hooks, no network. Governed schema (users, organizations, clients, projects, scopes, policies), FTS5 recall with hard client-isolation, hard-delete, neutral audit log.
- **`@memoria/daemon`** — a single local process owns the databases. Serialized writes, HTTP on `127.0.0.1` with token auth, singleton lock.
- **`@memoria/mcp`** — one MCP server per agent, relaying to the daemon. Connect any MCP-capable agent with one pasted command.
- **`@memoria/cli`** — `memoria init | doctor | pair | forget | …`
- **`@memoria/web`** — local web UI (no terminal needed): connect agents, browse memory, share, pause.
- **`packages/adapters`** — hosts become thin adapters (OpenClaw is just one of them).

### Principles

1. **Local-first, absolutely.** Nothing leaves your machine without explicit action.
2. **One memory per agent.** Each assistant instance is a digital person with private memory; sharing is opt-in, by subject.
3. **Memoria governs, agents propose.** Schema, dedup, redaction, audit and deletion belong to Memoria.
4. **Secrets never enter memory.** Hard redaction gate before storage; values live in the OS keychain (or an AES-256-GCM vault), memory only keeps references.
5. **Client isolation is non-negotiable.** The recall benchmark enforces a **0% cross-client leak rate** in CI.
6. **Free for users and for us.** No hosted infra, no telemetry, Apache-2.0.

## Development

```bash
npm install
npm run build     # tsc strict — 0 errors tolerated
npm test          # vitest — includes the recall-quality benchmark
node scripts/boot-test.mjs
```

Node ≥ 20. Native deps: `better-sqlite3`, `sqlite-vec`.

- Build & contribution docs: [`docs/v3/`](docs/v3/) (status, decisions log, handoff TODO, legacy port map)
- The frozen build spec lives in the project's dev dossier (`PLAN-Memoria-v3-2026-06-03.md`).

## License

Apache-2.0 © Primo-Studio
