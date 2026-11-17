<p align="center">
  <img src="docs/assets/hero-governance-console.png" alt="MemoryGuard governance console showing organized shared memory, a supersede chain, and a rollback history" width="960" />
</p>

<h1 align="center">MemoryGuard</h1>

<p align="center">
  <strong>Shared memory for coding agents, without shared-memory chaos.</strong><br />
  A local-first MCP memory layer that organizes writes automatically and keeps every governance decision reversible.
</p>

<p align="center">
  <a href="https://pypi.org/project/agent-memguard/"><img src="https://img.shields.io/pypi/v/agent-memguard.svg?label=PyPI" alt="PyPI version" /></a>
  <a href="https://github.com/irisxc4/memoryguard/blob/main/pyproject.toml"><img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python 3.10 or newer" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-2ea44f" alt="MIT license" /></a>
  <a href="README.zh-CN.md">中文文档</a>
</p>

> Your agents can write freely. MemoryGuard classifies, deduplicates, supersedes, quarantines, and compresses shared memory on every write - then lets you inspect, correct, or roll back the result afterward.
>
> **No account. No server. No telemetry. Your memory stays local.**

<p align="center">
  <a href="#install-in-60-seconds">Install in 60 seconds</a> ·
  <a href="#see-the-governance-loop">See the governance loop</a> ·
  <a href="#what-memoryguard-is-and-isnt">What it is and isn't</a>
</p>

## Why MemoryGuard

Persistent memory solves only half the problem. When several coding agents write into the same context, memory can become duplicated, stale, contradictory, or unsafe to reuse.

MemoryGuard is the local control layer between your coding agents and their shared memory:

| Instead of | MemoryGuard gives you |
|---|---|
| A growing pile of unreviewed notes | Write-time classification, deduplication, superseding, conflict detection, quarantine, derivation, and compression |
| Approving every agent write by hand | Automatic writes; human review only when you need it |
| Treating an overwrite as permanent | History, evidence, supersede chains, and rollback |
| Sending project context to another service | A local MCP stdio server with local SQLite storage |

## See the governance loop

<p align="center">
  <img src="docs/assets/write-organize-rollback.png" alt="A MemoryGuard demo: an agent writes a duplicate memory, MemoryGuard supersedes the stale version, then the operator restores a previous version" width="900" />
</p>

```text
Agent writes memory
  -> MemoryGuard MCP write
  -> auto-organize
      classify · deduplicate · supersede · detect conflict · quarantine · compress
  -> active shared memory
  -> governance console
      inspect · correct · merge · lock · restore · roll back
```

The console is **not an approval queue**. Agents keep moving; you govern the outcome with evidence when it matters.

## Install in 60 seconds

```bash
pip install agent-memguard
```

Choose the coding agent you use. Each command adds MemoryGuard as an MCP server and writes its instruction file.

```bash
# Claude Code
memoryguard source add . && python -m memoryguard.provider_adapters install claude

# Codex
memoryguard source add . && python -m memoryguard.provider_adapters install codex

# Cursor
memoryguard source add . && python -m memoryguard.provider_adapters install cursor
```

Then restart your agent and verify the environment:

```bash
memoryguard doctor
memoryguard mcp-status
```

Need a desktop window for the governance console?

```bash
pip install "agent-memguard[gui]"
```

For explicit configuration and provider-specific behavior, see the [Claude Code](docs/install-claude-code.md), [Codex](docs/install-codex.md), and [Cursor](docs/install-cursor.md) guides.

## What you can govern

<p align="center">
  <img src="docs/assets/governance-evidence.png" alt="MemoryGuard evidence views for a conflict, a quarantined secret, a supersede chain, and version history" width="900" />
</p>

| Signal | What you can do |
|---|---|
| Duplicate or stale memory | See the supersede chain and restore the prior version if needed |
| Conflicting memories | Surface the conflict and resolve it deliberately |
| Secrets, tokens, or credentials | Quarantine them instead of leaving them in active shared memory |
| A wrong governance decision | Inspect its history and roll the shared memory back to a version snapshot |
| Multiple coding agents | Bind agents to a governed shared-memory group |

## What MemoryGuard is - and isn't

MemoryGuard is a **local MCP memory backend and governance console** for coding agents. It provides a shared source of truth and organizes writes as they arrive.

It is not a cloud service, an account system, or a human gate that blocks every memory write. It also does not pretend every agent's native memory can be disabled: provider support is reported as redirected, observed, or unsupported where appropriate.

## Architecture

| Layer | Responsibility |
|---|---|
| **Evidence layer** | Agent-native memory, files, documents, and external MCP descriptors; raw inputs, not governance truth |
| **Memory layer** | MemoryGuard's local MCP shared-memory backend; the governed shared source of truth |
| **Governance layer** | GUI and CLI for observation, evidence, corrections, and reversible changes |

## Core surfaces

| Surface | Use it for |
|---|---|
| MCP memory backend | Read, search, write, update, delete, and inspect shared-memory status |
| Auto-organizer | Classify, deduplicate, supersede, detect conflicts, quarantine, derive, and compress on write |
| Governance console | Review raw writes, conflicts, quarantine, supersede chains, and versions |
| Provider adapters | Set up Claude Code, Codex, or Cursor from one command |
| CLI | Audit local sources, manage authorized inputs, inspect reports, and manage memory builds/releases |

The complete MCP tool reference and CLI command reference are below for evaluation and integration work.

<details>
<summary><strong>CLI commands</strong></summary>

| Command | Description |
|---|---|
| `audit [path]` | Read-only scan; generate a report |
| `open [path]` | Open the latest report in a window |
| `explain <finding_id>` | Explain a finding's evidence and risk |
| `plan <finding_ids...>` | Generate a minimal fix plan without writing |
| `apply <plan_id>` | Apply a plan: backup, patch, and rescan |
| `verify` | Rescan and compare before/after |
| `undo <change_id>` | Restore from backup and re-verify |
| `source <action>` | Manage authorized sources |
| `scan` | Read-only scan and coverage ledger |
| `import <action> <bundle>` | Preview or create an offline import bundle |
| `memory <action>` | Memory build, verify, and release rollback workflows |
| `doctor` | Diagnose installation and environment |
| `mcp-status` | Inspect MCP shared-memory status |

</details>

<details>
<summary><strong>MCP tools</strong></summary>

| Group | Tools |
|---|---|
| Memory backend | `memoryguard_memory_read`, `memoryguard_memory_search`, `memoryguard_memory_write`, `memoryguard_memory_update`, `memoryguard_memory_delete`, `memoryguard_memory_status` |
| Audit and scan | `memoryguard_audit`, `memoryguard_explain`, `memoryguard_list_sources`, `memoryguard_scan_summary`, `memoryguard_neuron_graph`, `memoryguard_import_preview`, `memoryguard_build_plan` |
| Agent binding | `memoryguard_binding_create`, `memoryguard_binding_list` |
| External MCP | `memoryguard_external_mcp_list`, `memoryguard_external_mcp_import` |
| Document extraction | `memoryguard_extract_memories`, `memoryguard_accept_candidates` |
| Semantic and provider | `memoryguard_semantic_check`, `memoryguard_provider_install` |

</details>

## Privacy and safety boundaries

- MemoryGuard runs as a local MCP stdio server; it requires no account, remote server, or telemetry.
- Shared memory is stored locally in SQLite under `.memoryguard/`.
- Source scanning is read-only by default. Changes use explicit plans, backups, rescans, and undo paths.
- A quarantined memory is deliberately kept out of active shared memory until you decide what to do with it.

## Roadmap

- **Now:** local MCP backend, auto-organization, governance console, provider adapters, and rollback.
- **Later:** enhanced governance signals such as decay, derivation, and governance reports. No committed date.
- **Later:** team and enterprise capabilities after proven demand. No committed date.

## Contributing

Issues and pull requests are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md); by submitting a pull request, you agree to the [CLA](CLA.md).

## License

[MIT](LICENSE)
