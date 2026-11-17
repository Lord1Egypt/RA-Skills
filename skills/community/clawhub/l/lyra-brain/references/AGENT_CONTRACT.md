# LYRA 3-Brain — agent contract (v2.1.0)

## Must

1. **Explicit consent** — only write/grow when the user clearly asks for **disk** memory (log snip, grow graph, 3-brain file).  
2. **Pass `--i-consent`** on all write CLIs.  
3. **Additive only** — no destructive overwrite of vault/graph without explicit user consent.  
4. **P0/Oath** — grow is validated in LYRA_CORE; no secrets.  
5. **Snip discipline** — DONE facts only (ids, urls, paths, merkle).  
6. **Real data** — only log URLs/IDs that exist.  

## Must not

1. Treat vague “remember that” / “log this” (app logs) as disk-memory consent.  
2. Auto-publish GitHub/HF/ClawHub/social.  
3. Put secrets in memory or grow text.  
4. Claim ALIGNED without stack verify when stating lattice health.  
5. Run write scripts without `LYRA_CORE_ROOT` set by the operator.  

## When to load this skill

| Load | Do not load |
|------|-------------|
| “Write a lyra-brain snip…” | Casual chat “remember for this reply” |
| “Grow into 3-brain graph…” | “Remember” meaning short-term context only |
| “Recall from LYRA memory…” | Unrelated “log” / debugging |
| End of multi-step ops **and** user asked to persist | Compaction without user ask |

## Recall modes

- `balanced` (default), `library`, `outer`, `working` — see MEMORY_LAYOUT.md
