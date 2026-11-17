# AI-DFE — Process Overview

> Loaded by `core-engine.md`. High-level map of the data-fabric engine. The authoritative behavior is in the core engine; this is the navigational overview.

## Phase Map

```
CONFIGURE (discover-once)        OPERATE (continuous)              GOVERN
┌─────────────────────┐         ┌─────────────────────┐          ┌──────────────────┐
│ 1.1 family-discovery│         │ 2.1 gather  (Layer 1)│          │ 3.1 validation   │
│ 1.2 package-disc.   │  ─────► │ 2.2 shape   (Layer 2)│  ──────► │ 3.2 freshness    │
│ 1.3 demand-disc.    │         │ 2.3 distribute       │          │ 3.3 history      │
└─────────────────────┘         │ 2.4 monitor          │          │ 3.4 cleanup      │
        │ caches to              │ 2.5 cross-project    │          └──────────────────┘
        ▼ dfe-state.md           │ 2.6 cross-family     │
                                 └─────────────────────┘
```

## The Two Layers

| Layer | Input | Output | Stage |
|-------|-------|--------|-------|
| Layer 1 — Gather | declared raw sources | `{pkg}-data.json` (one per package) | 2.1 |
| Layer 2 — Shape | per-package JSON | `{consumer-output}.json` (one per DEMAND) | 2.2 |

Layer 2 is ALWAYS assembled from Layer 1, never from raw sources again.

## Interaction Model

| Mode | Trigger | Writes? |
|------|---------|---------|
| Operation | `DAT__ all`, `DAT__ {family}`, `DAT__ {family}/{pkg}`, `DAT__ aggregate`, `DAT__ discover`, `DAT__ cleanup`, `DAT__ master` | yes |
| Report | `DAT__ status`, `DAT__ validate`, `DFA__ …` | no |
| Continuous | FLO signal or timestamp pass | refreshes stale only |

## Commands

| Command | Phase | What |
|---------|-------|------|
| `DAT__ all` | all | full pass |
| `DAT__ {family}` / `DAT__ {family}/{pkg}` | 2 | scoped refresh |
| `DAT__ aggregate` | 2.2 | re-shape demands from existing per-package data |
| `DAT__ status` | 3.2 | staleness report |
| `DAT__ discover` | 1 | force re-discovery |
| `DAT__ validate` | 3.1 | dry-run schema validation |
| `DAT__ cleanup --before {ms}` | 3.4 | prune history |
| `DAT__ master` / `--set {family}` | 2.6 | master-mode control |
| `DFA__ [schema\|registry\|manifest\|freshness\|territory]` | 3 | integrity agent (report-only, 18 checks / 5 categories) |

## Graceful Degradation

A package that hasn't run, or a missing source file, never errors. The corresponding fields become `null`; the data file is still written and still valid. `DAT__ status` and `DFA__ freshness` surface what's missing.
