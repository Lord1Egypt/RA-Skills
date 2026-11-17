# Compatibility matrix — 2026-11-11

Capability-detected refresh for the P0 Nov 2026 maintenance pass. This is not a
live-memory dry run and does not replace [dogfood-2026-09-18](dogfood-2026-09-18.md).

## Verified host

| Component | Observed |
| --- | --- |
| Operator OpenClaw CLI | `2026.9.2` (`3928bad`) |
| Node.js | `v24.20.0` |
| Migrator under test | `0.1.0-rc.3` workspace |
| Official LanceDB package on npm | `@openclaw/memory-lancedb@2026.11.3` |
| Pro npm `latest` | `memory-lancedb-pro@1.0.32` |
| Pro npm `beta` tag | `1.1.0-beta.9` |
| Pro GitHub release | `v1.1.0-beta.10` (2026-03-23); repo still active as of 2026-11-07 |

## Capability checks

| Source | Capability | Result |
| --- | --- | --- |
| memory-core (bundled) | `openclaw memory status|search|index` | Present on `2026.9.2` |
| Official memory-lancedb | `openclaw ltm *` | **Not present** until the plugin is installed; docs still document `ltm list/search/stats/query` |
| memory-lancedb-pro | `export` / `list` | Still per-scope; export path still uses a large fixed list budget (1,000) in `v1.1.0-beta.10` source |
| OpenClaw migrate CLI | `openclaw migrate` | Present for agent-system providers (for example Hermes); not a memory-backend cutover substitute |

## Adapter status after refresh

| Adapter | Status | Notes |
| --- | --- | --- |
| `lancedb-pro` | stable | Keep capability detection; no `--all-scopes` verified |
| `lancedb-official-list-beta` | beta | Still list-capture + versioned manifest; install `@openclaw/memory-lancedb` before expecting `ltm` |
| `markdown` / `qmd` | stable | Markdown-authoritative only |
| `canonical-v1` | stable | Preferred audit input after normalize |

## Product implications

1. Document that `ltm` is plugin-gated, not core-bundled.
2. Keep Pro multi-scope and 1,000-row export limits as operator chores until v0.2.0 orchestration.
3. Treat reverse migration marketing (core→Pro) as adjacent demand, not a reason to abandon the proof-first return path.
4. Re-run a live export dry-run before claiming a new Pro beta as verified.
