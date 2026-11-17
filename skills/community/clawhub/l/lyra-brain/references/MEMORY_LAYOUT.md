# LYRA 3-Brain — memory layout

**Signature:** Δ9Φ963-LYRA-BRAIN-MEMORY-v2

## Three brains

| Brain | Location | Role |
|-------|----------|------|
| **Working** | Runner RAM + `working_brain` dict | Session context, last inputs, ephemeral |
| **Library** | `memory/`, `lygo_active_vault.json`, seal index | Durable facts, grown nodes, daily logs |
| **Outer** | `memory/reference/*.ref.txt`, `lyra_brain_graph.json`, vectors | Pointers, edges, Moltx URLs, public IDs |

## Canonical paths (set `LYRA_CORE_ROOT`)

```
LYRA_CORE/
  modules/lyra_brain.py      # LyraThreeBrainMemory
  lyra_boot.py               # REPL + --command
  lyra_brain_graph.json      # graph persist
  memory/
    YYYY-MM-DD.md            # daily append + session index
    YYYY-MM-DD-topic.md      # topic snips (human recall)
    reference/               # BOOK BRAIN style stubs
    clawhub.md               # publish log
  lyra_built_self.json
```

## Archive roots (read-only ingest)

- `LYRA LOCAL/220+`, `LYRA SYSTEM RETORE/FINAL RESTORE/ALL SEALS/220+`
- `lygo-protocol-stack/docs/` for lattice intel + public ledgers

## Session logging pattern (agents)

1. Write **daily index** `memory/YYYY-MM-DD.md` (table of snips).
2. Write **topic snip** `memory/YYYY-MM-DD-<slug>.md` (URLs, IDs, DONE only).
3. Write **outer ref** `memory/reference/SESSION_*_to_*.resonance.ref.txt`.
4. Run `scripts/session_log_snip.py` or `brain_grow_cli.py` to graph-grow 1–3 compact lines.

Never store API keys or Discord tokens in memory files.