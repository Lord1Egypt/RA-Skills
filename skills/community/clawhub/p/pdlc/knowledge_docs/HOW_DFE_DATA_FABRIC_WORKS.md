# How AI-DFE Data Fabric Works

**Purpose:** Explains how AI-DFE turns the scattered markdown outputs every AI-* package produces into a single, governed, machine-readable data surface — gathering sources, shaping them per consumer need, and distributing clean JSON to one read-point — so dashboards, extensions, and reports get trustworthy data without ever knowing where the raw files live.

---

## What AI-DFE Does

AI-DFE is the data layer of the AI-* Family. Every package in the family writes human-readable markdown — a Project Initiation Package here, an Architecture Package there, a portfolio register somewhere else. That output is scattered across many folders in many shapes. Anything that wants to *consume* that information (a dashboard, a report, a VS Code extension) would otherwise have to know where every file lives and how to parse it.

AI-DFE removes that coupling. It reads each package's declared output, projects it into structured JSON, reshapes it into exactly what each consumer asked for, and serves it all from one folder: `{family}-ws/data/`. AI-DFE is the **sole owner and sole writer** of that folder — which is precisely what makes the surface trustworthy.

It answers: "Where is the clean, current, validated version of everything the family has produced — in a form a tool can read?"

```
   PACKAGE OUTPUTS (scattered markdown, many folders)
   AI-PILC · AI-POLC · AI-UXD · AI-ADLC · AI-DWG · AI-PPM · …
        │
        ▼
┌──────────────────────────────────────────────────────────────────┐
│  AI-DFE — DATA FABRIC ENGINE                                       │
│                                                                    │
│  CONFIGURE → OPERATE → GOVERN   (3 phases)                        │
│                                                                    │
│  discover sources · gather (Layer 1) · shape (Layer 2) ·           │
│  distribute · validate · snapshot · monitor freshness              │
└──────────────────────────────────────────────────────────────────┘
        │
        ▼
   {family}-ws/data/   ← one governed read-point
        │
        ▼
   CONSUMERS (dashboards, extensions, reports) — read via REGISTRY.json
```

**Hard boundary:** AI-DFE gathers and shapes; it never decides structure and never places files for other packages. It navigates to where each package *says* its output lives, reads it, and writes only its own data surface. It is not a link in the chain — like the flow router, it runs *alongside* the whole family as a continuous engine.

---

## The Two-Layer Pipeline

The heart of AI-DFE is a two-layer projection. This separation is what keeps the surface both faithful and flexible.

| Layer | What it is | Built from |
|-------|-----------|------------|
| **Layer 1 — per-package JSON** | One `{pkg}-data.json` per package: a faithful, structured projection of that package's raw output | The package's declared source files |
| **Layer 2 — consumer outputs** | One `{consumer-output}.json` per registered consumer, shaped exactly to that consumer's declared demand | **Layer 1 JSON only — never raw sources** |

**The two-layer rule:** consumer outputs are always assembled from per-package JSON, never re-extracted from raw markdown. Layer 1 is the single faithful reading of each package; Layer 2 is any number of consumer-tailored views built on top of it. Read each raw source once, reshape it many ways.

---

## The Three Phases

### Phase 1 — Configure (discover the workspace, once)

AI-DFE learns the workspace on first encounter, then caches what it learned. It does not re-read package internals on every pass.

| Stage | What happens |
|-------|--------------|
| **Family discovery** | Reads the family manifest and installed package set to learn family identity and anchors; enumerates the known projects |
| **Package discovery** | For each installed package, reads that package's self-describing source map and data schema — caching which files to read and what shape the output takes |
| **Demander discovery** | Reads the consumer registry to resolve each registered consumer's data demand; also self-heals by scanning for unregistered consumers and auto-registering them |

**Discover-once rule:** full discovery re-runs only on first encounter, on an explicit re-discover command, when a package's source map or schema changes, or on a schema-version mismatch. Otherwise AI-DFE skips straight to monitoring. This is what keeps routine passes fast.

A package is discovered by its **declared data interface** (a self-describing marker), not by guessing paths. Placement is never invented — each package tells AI-DFE where its sources live.

### Phase 2 — Operate (gather → shape → distribute → monitor)

| Stage | What happens | Output |
|-------|--------------|--------|
| **Gather (Layer 1)** | Read each package's declared sources, extract the mapped fields, build one validated `{pkg}-data.json` | per-package JSON |
| **Shape (Layer 2)** | For each demand, assemble a consumer output from the per-package JSON | validated consumer JSON |
| **Distribute** | Write all outputs to the data folder; rebuild `REGISTRY.json`; snapshot to history | data surface + registry |
| **Monitor** | Compare cached source timestamps against the last generation time; refresh only what changed | refreshed deltas |
| **Cross-project** | Roll per-project data up into portfolio-level views | aggregated JSON |

### Phase 3 — Govern (validate → freshness → history → cleanup)

| Stage | What happens |
|-------|--------------|
| **Validation** | Every file is validated against its schema **before** it is written. A failure blocks that one file (the prior version stays) and reports — the rest of the pass continues |
| **Freshness** | Assesses staleness and lag across packages and demands — the basis of the status report |
| **History** | Every written file is snapshotted into `history/` with a millisecond timestamp |
| **Cleanup** | Prunes old snapshots per retention policy, on request |

---

## REGISTRY.json: How Consumers Find Data

The registry is the linchpin of consumer decoupling. Every consumer reads **one fixed path** — `REGISTRY.json` — to discover where all of its data lives. It never hardcodes a path into the data folder and never reaches into a source file.

```
Consumer startup:
  1. Read REGISTRY.json (one known path)
  2. Look up the entry for the data it needs
  3. Fetch the file at the path the registry gives
```

Because producers and consumers are joined only through the registry, either side can move or change without breaking the other. The registry is **re-derived on every write** — rebuilt from what was actually written, never blindly appended to — so it can never drift out of sync with the real files.

### The consumer contract

A consumer is *served* only when it holds up its end of a small contract:

1. It ships a **data demand** declaration (`data-demand/{name}.demand.md`) stating exactly what shape it wants.
2. It registers itself in the **consumer registry**.
3. It resolves its data through `REGISTRY.json` → path → data.

Consumers are **discovered, not assumed** — AI-DFE finds them by their demand declaration, the mirror image of how it discovers producers by their source map. Hardcoding a data path instead of reading the registry is a contract violation.

---

## Graceful Degradation: Incomplete Is Fine, Broken Is Not

A missing or not-yet-run package never causes an error. It becomes a `null`-filled `{pkg}-data.json` marked `status: not-run`, and the pass continues. This means AI-DFE produces a valid, useful surface even in a half-built workspace — you get data for the nine packages that ran, with clean nulls for the one that didn't, rather than a failed run.

The installer bootstraps an **empty but valid** data folder. It fills on the first data operation.

---

## Operating It: Commands and Modes

AI-DFE runs in three interaction modes, activated by the explicit key `_DFE_` or by data-fabric requests:

- **Operation mode** — does work and may write the data folder (gather, shape, distribute, discover, aggregate, cleanup).
- **Report mode** — reads and reports, never writes (status/freshness and the integrity agent).
- **Continuous mode** — when signalled that a package finished, or on a timestamp pass, refreshes only what changed.

| Command | Mode | What it does |
|---------|------|--------------|
| `DAT__ all` | writes | Full pass: gather → shape → distribute (each write validated + snapshotted), plus cross-project rollups |
| `DAT__ full` | writes | Same pipeline, then asserts completeness and emits a readiness report naming any package still absent or not-run |
| `DAT__ {family}/{pkg}` | writes | Re-gather one package and reshape only the outputs that depend on it |
| `DAT__ discover` | state only | Re-run full discovery; rewrite the registries; write no data files |
| `DAT__ status` | report | Staleness and lag across packages and demands |
| `DAT__ validate` | report | Dry-run schema check over existing files without regenerating |
| `DAT__ cleanup --before {ts}` | history only | Prune old snapshots |

Two report-only agents support the engine: a **health check** (`DHC__`) that answers "can the fabric run in this workspace?" (run it first in a new workspace), and an **integrity agent** (`DFA__`) that runs a deep, multi-category assessment of the surface. Rule of thumb: `DAT__` changes things; `DHC__` and `DFA__` only look.

---

## Why It Works This Way

| Principle | Why it matters |
|-----------|----------------|
| **Single-writer** | Only AI-DFE writes the data folder. One writer means one source of truth — no races, no conflicting versions, a surface consumers can trust. |
| **Schema-first** | No file is written without passing its schema. Consumers can rely on the shape without defensive parsing. |
| **Two-layer** | Reading raw sources once (Layer 1) and reshaping many times (Layer 2) keeps the faithful projection separate from consumer-specific views. |
| **Discover-once** | Learning interfaces once and then watching timestamps keeps routine passes cheap. |
| **Registry-mediated** | Producers and consumers never bind directly — either can change without breaking the other. |
| **Graceful degradation** | A partial family still yields a valid surface; missing becomes `null`, never a crash. |
| **Generated, not hand-edited** | Everything in the data folder is tool-produced, so a re-run always reproduces it — nothing precious is lost. |

---

## Related Documents

| Document | Location |
|----------|----------|
| How to Use the Dashboard | `knowledge_docs/HOW_TO_USE_THE_DASHBOARD.md` |
| How the Communication Fabric Works | `knowledge_docs/HOW_COMMUNICATION_FABRIC_WORKS.md` |
| How State Files Work | `knowledge_docs/HOW_STATE_FILES_WORK.md` |
| How Chain Handoff Works | `knowledge_docs/HOW_CHAIN_HANDOFF_WORKS.md` |
| Pattern: Marker File Detection | `knowledge_docs/PATTERN_MARKER_FILE_DETECTION.md` |
| Pattern: Graceful Standalone | `knowledge_docs/PATTERN_GRACEFUL_STANDALONE.md` |

---

*Knowledge Document | Created: 2026-07-05 | Updated: 2026-07-05 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
