# How to Run the Data Fabric

**Purpose:** Practical guide for using AI-DFE to turn your packages' scattered outputs into clean, validated, machine-readable data that a dashboard, report, or extension can consume — covering first-run setup, routine refreshes, checking freshness, and connecting a new consumer.

---

## Who This Is For

You've run one or more AI-* packages on your project and now something needs to *read* that output as data — a dashboard wants progress numbers, a report wants the portfolio register, an extension wants the current backlog. Rather than teaching each of those tools where every markdown file lives and how to parse it, you run AI-DFE once and it serves everything from a single place.

You do not need to understand the internals to use it. If you want the mechanics (the two-layer pipeline, the registry, graceful degradation), see `HOW_DFE_DATA_FABRIC_WORKS.md`.

---

## Before You Start

- AI-DFE is installed in your workspace (its rules and detail folders are in place).
- At least one AI-* package has produced output. AI-DFE works with a partial family — anything not yet run simply comes back as `null`, never an error.
- You activate AI-DFE with the explicit key `_DFE_`, or just by asking for a data operation.

---

## Step 1 — Check the Workspace Is Ready (first run only)

In a brand-new workspace, run the health check first:

```
DHC__
```

This answers one question: *can the data fabric run here?* It's read-only — it verifies the data folder scaffolding exists and reports anything missing. If it flags missing empty scaffolding, `DHC__ fix` creates it (and only that — it never writes data).

## Step 2 — Do a Full Pass

Run the main data operation:

```
DAT__ all
```

This gathers data from every installed package, shapes it into the outputs each registered consumer asked for, validates every file against its schema, writes it all to `{family}-ws/data/`, and rebuilds `REGISTRY.json`. You'll get a status line back, for example:

```
Gathered 9/10 packages. ai-tge: not run (null). 12 files written. Registry updated.
```

If you have the complete family installed and want AI-DFE to assert completeness — naming any package or dashboard pane still absent — use the fuller variant:

```
DAT__ full
```

This runs the same pipeline and then emits a readiness report. It never fabricates data; a package that hasn't run stays `null` and is named in the report.

## Step 3 — Point Your Consumer at the Data

A consumer (dashboard, report, extension) reads its data through the registry — never by reaching into a source file:

1. Read `{family}-ws/data/REGISTRY.json` (one fixed path).
2. Look up the entry for the data it needs (e.g. `dashboard-data.json`).
3. Open the file at the path the registry gives, and read its `data` payload.

If you're wiring up the dashboard specifically, `HOW_TO_USE_THE_DASHBOARD.md` walks through it end to end.

---

## Routine Use

Once the surface exists, you don't re-run everything every time. Match the command to what changed:

| Situation | Command | What it does |
|-----------|---------|--------------|
| A package's output changed | `DAT__ {family}/{pkg}` | Re-gathers that one package and reshapes only the outputs that depend on it |
| You just want the consumer views rebuilt | `DAT__ aggregate` | Reshapes and redistributes demand outputs from already-fresh per-package data (no gather) |
| Everything may have moved | `DAT__ all` | Full gather → shape → distribute pass |
| "Is anything stale?" | `DAT__ status` | Read-only staleness/lag report across packages and demands |
| "Is the existing data valid?" | `DAT__ validate` | Read-only schema dry-run over existing files — no regeneration |

**Tip:** AI-DFE discovers each package's data interface once and then just watches timestamps, so routine passes are cheap. It only re-learns the workspace on first run, when you run `DAT__ discover`, or when a package's interface changes.

---

## Connecting a New Consumer

Consumers are *discovered, not assumed*. To have AI-DFE serve a new dashboard, report, or extension, that consumer must hold up its end of the contract:

1. **Declare a demand** — ship a `data-demand/{name}.demand.md` file describing exactly the shape it wants.
2. **Register** — add an entry to `{family}-ws/data/CONSUMER_REGISTRY.md` (AI-DFE also self-heals: it scans for unregistered consumers under `tools/extensions/*/data-demand/` and auto-registers them).
3. **Read via the registry** — resolve data through `REGISTRY.json` → path → data. Never hardcode a data path.

Then run `DAT__ discover` (to pick up the new demand) followed by `DAT__ all`, and the consumer's output will be produced and registered.

---

## Checking Quality

For a deeper, standalone assessment of the whole surface — schema conformance, registry integrity, manifest correctness, freshness, and territory ownership — run the integrity agent:

```
DFA__
```

It performs a multi-category integrity assessment and returns a findings report, each finding naming the `DAT__` command that fixes it. It is strictly read-only — it never mutates the data. Rule of thumb: **`DAT__` changes things; `DHC__` and `DFA__` only look.**

---

## Common Situations

| Situation | What's happening | What to do |
|-----------|------------------|------------|
| A package shows `null` / `not-run` | That package hasn't produced output yet — graceful degradation, not an error | Run the package, then `DAT__ {family}/{pkg}` |
| Consumer shows stale data | The consumer's mirrored copy drifted, or the surface wasn't refreshed | Re-run `DAT__ all`; confirm the consumer reads via `REGISTRY.json`, not a cached path |
| A write was blocked | A file failed schema validation; the prior version was kept and the rest of the pass continued | Read the reported field mismatch, fix the source, re-run |
| New consumer isn't served | It hasn't been discovered | Ensure it ships a demand + registry entry, run `DAT__ discover` then `DAT__ all` |

---

## Related Documents

| Document | Location |
|----------|----------|
| How AI-DFE Data Fabric Works | `knowledge_docs/HOW_DFE_DATA_FABRIC_WORKS.md` |
| How to Use the Dashboard | `knowledge_docs/HOW_TO_USE_THE_DASHBOARD.md` |
| How State Files Work | `knowledge_docs/HOW_STATE_FILES_WORK.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |
| Pattern: Graceful Standalone | `knowledge_docs/PATTERN_GRACEFUL_STANDALONE.md` |

---

*Knowledge Document | Created: 2026-07-05 | Updated: 2026-07-05 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
