<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
<!--
  PARALLEL TEMPLATE — Claude Code variant of session-orchestrator.md.
  Claude Code has NO `inclusion:` directive and does NOT auto-load `CLAUDE*.md`
  by filename glob — only a real `CLAUDE.md` (which the installer wires to import
  this file via `@CLAUDE_PDLC_ORCHESTRATOR.md`). Routing uses on-demand `Read` of
  the cores in the uniform home `.aiflc/pdlc/` (OI-158) — identical targets to the
  generic orchestrator; only this file's loading header (import vs `inclusion:`)
  differs. Any change to the routing/trigger semantics here MUST be mirrored in
  session-orchestrator.md (and vice versa). Enforced by INV-L3-030.
-->
# AIFLC Session Orchestrator — AI-* PDLC Family (Claude Code)

> **This is the only always-loaded steering for the AI-* PDLC Family on Claude Code.** It is imported by your workspace `CLAUDE.md` (`@CLAUDE_PDLC_ORCHESTRATOR.md`). All package cores live in the uniform home `.aiflc/pdlc/` and are **not** auto-loaded — this orchestrator `Read`s the relevant core on demand. That keeps the context window free for actual work.

---

## Purpose

Prevent context overload. Instead of loading all package workflows into every session, this orchestrator:
1. Detects what the user wants to do
2. `Read`s ONLY the relevant package core from `.aiflc/pdlc/` (and its rule-details on demand)
3. Provides the activation keys as a routing table

---

## Activation Keys (Quick Reference)

> **Full trigger registry (all package keys + all agent shortcuts):** `Read` `.aiflc/pdlc/TRIGGER_KEYS_REFERENCE.md`

| Key | Package | When to Use |
|-----|---------|-------------|
| `_ILC_` | AI-ILC | New idea capture, evaluation, go/no-go |
| `_PILC_` | AI-PILC | Project initiation from requirements |
| `_PPM_` | AI-PPM | Portfolio management, cross-project governance |
| `_FLO_` | AI-FLO | Flow routing, entity position tracking |
| `_POLC_` | AI-POLC | Product backlog, product ownership |
| `_UXD_` | AI-UXD | UX design, personas, journeys, design system |
| `_ADLC_` | AI-ADLC | Architecture / system design |
| `_DWG_` | AI-DWG | Development workspace generation |
| `_GCE_` | AI-GCE | Compliance / enforcement governance |
| `_TGE_` | AI-TGE | Test governance, coverage analysis |
| `_DFE_` | AI-DFE | Data fabric (gather/shape/distribute) |
| `_ACTIVE_` | (read-only) | Report which package is currently active |
| `DAT__` | AI-DFE | Data operations (gather, status, discover) |
| `DFA__` | AI-DFE | Data fabric audit (read-only report) |
| `DHC__` | AI-DFE | Data fabric bootstrap readiness check |
| `FHC__` | AI-FLO | FLO health check — "is this workspace FLO-ready?" |
| `FIA__` | AI-FLO | FLO integrity audit — "is FLO's state correct?" |

---

## Path Map (uniform home `.aiflc/pdlc/`)

All package cores and rule-details live under the uniform home `.aiflc/pdlc/` — identical to every other platform. When you activate a package, `Read` its core file first, then its rule-details folder on demand:

| Package | Core file to `Read` | Rule-details folder (on demand) |
|---------|---------------------|---------------------------------|
| AI-ILC  | `.aiflc/pdlc/ai-ilc-rules/core-workflow.md`   | `.aiflc/pdlc/ai-ilc-rule-details/`  |
| AI-PILC | `.aiflc/pdlc/ai-pilc-rules/core-workflow.md`  | `.aiflc/pdlc/ai-pilc-rule-details/` |
| AI-PPM  | `.aiflc/pdlc/ai-ppm-rules/core-engine.md`     | `.aiflc/pdlc/ai-ppm-rule-details/`  |
| AI-FLO  | `.aiflc/pdlc/ai-flo-rules/core-engine.md`     | `.aiflc/pdlc/ai-flo-rule-details/`  |
| AI-POLC | `.aiflc/pdlc/ai-polc-rules/core-workflow.md`  | `.aiflc/pdlc/ai-polc-rule-details/` |
| AI-UXD  | `.aiflc/pdlc/ai-uxd-rules/core-workflow.md`   | `.aiflc/pdlc/ai-uxd-rule-details/`  |
| AI-ADLC | `.aiflc/pdlc/ai-adlc-rules/core-workflow.md`  | `.aiflc/pdlc/ai-adlc-rule-details/` |
| AI-DWG  | `.aiflc/pdlc/ai-dwg-rules/core-generator.md`  | `.aiflc/pdlc/ai-dwg-rule-details/`  |
| AI-GCE  | `.aiflc/pdlc/ai-gce-rules/core-generator.md`  | `.aiflc/pdlc/ai-gce-rule-details/`  |
| AI-TGE  | `.aiflc/pdlc/ai-tge-rules/core-engine.md`     | `.aiflc/pdlc/ai-tge-rule-details/`  |
| AI-DFE  | `.aiflc/pdlc/ai-dfe-rules/core-engine.md`     | `.aiflc/pdlc/ai-dfe-rule-details/`  |

> If a core file is not present under `.aiflc/pdlc/`, that package was not installed in this bundle — tell the user which packages are available and how to install the missing one.
>
> **Claude slash commands:** installed packages also expose `/pdlc:<key>` commands (e.g. `/pdlc:pilc`) generated under `.claude/commands/pdlc/` — each simply `Read`s the same core below.

---

## Session Detection Logic

When the user starts a session WITHOUT an explicit activation key, determine intent from their message, then `Read` the matching core file:

| User Intent Signal | Route To (`Read`) |
|-------------------|-------------------|
| "I have an idea" / "new idea" / "evaluate this" | `.aiflc/pdlc/ai-ilc-rules/core-workflow.md` |
| "initiate project" / "start project" / "PIP" | `.aiflc/pdlc/ai-pilc-rules/core-workflow.md` |
| "portfolio" / "cross-project" / "prioritize projects" | `.aiflc/pdlc/ai-ppm-rules/core-engine.md` |
| "route" / "flow" / "handoff" / "where is entity" | `.aiflc/pdlc/ai-flo-rules/core-engine.md` |
| "backlog" / "epics" / "product ownership" / "prioritize" | `.aiflc/pdlc/ai-polc-rules/core-workflow.md` |
| "UX" / "personas" / "journeys" / "design system" / "user experience" | `.aiflc/pdlc/ai-uxd-rules/core-workflow.md` |
| "architecture" / "system design" / "containers" / "C4" | `.aiflc/pdlc/ai-adlc-rules/core-workflow.md` |
| "workspace" / "generate workspace" / "steering files" | `.aiflc/pdlc/ai-dwg-rules/core-generator.md` |
| "compliance" / "hooks" / "enforcement" / "rules derivation" | `.aiflc/pdlc/ai-gce-rules/core-generator.md` |
| "test governance" / "test strategy" / "coverage" | `.aiflc/pdlc/ai-tge-rules/core-engine.md` |
| "data" / "gather" / "DAT__" / "DFA__" / "freshness" | `.aiflc/pdlc/ai-dfe-rules/core-engine.md` |
| "FHC__" / "FLO health" / "is workspace ready for FLO" | `.aiflc/pdlc/ai-flo-rules/core-engine.md` → run FLO Health Check agent |
| "FIA__" / "FLO integrity" / "routing state" | `.aiflc/pdlc/ai-flo-rules/core-engine.md` → run Flow Integrity agent |
| "resume" / "continue" / "where was I" | Check `*-state.md` files for in-progress package → `Read` that one's core from `.aiflc/pdlc/` |
| Ambiguous / general question | Ask: "Which AI-* package are you working with?" and list the keys |

---

## Resume Detection

When user says "resume" or "continue" without specifying a package:

1. Scan for any `*-state.md` with status ≠ "complete":
   - `{family}-ws/ideas/ilc-state.md` → check if an idea is in-progress
   - `{family}-ws/projects/*/pip/pilc-state.md` → check if PIP is in-progress
   - `{family}-ws/projects/*/backlog/polc-state.md` → check status field
   - `{family}-ws/projects/*/architecture/adlc-state.md` → check status
   - `{family}-ws/projects/*/ux/uxd-state.md` → check status
   - `{family}-ws/portfolio/ppm-state.md` → check status
2. If exactly ONE package is in-progress → `Read` that package's core from `.aiflc/pdlc/` and resume.
3. If MULTIPLE packages are in-progress → present the list, ask user which to resume.
4. If NONE in-progress → ask what they want to do.

---

## Multi-Package Isolation (Enforced)

- Only ONE package core is active at a time.
- A package switch NEVER happens without a direct user order or explicit confirmation.
- When switching, announce: "Active package: AI-{XXX}" as the first line.
- The `_ACTIVE_` key reports the current active package without switching.

---

## State Awareness (Lightweight)

> **PLACEHOLDER — populated per workspace.** A static source cannot know per-workspace package status. A future Workspace Initiator (or a manual update) fills this in from the actual `*-state.md` files. Leave as-is in the package source.

- **Active project:** {populated per workspace}
- **Packages complete:** {populated per workspace}
- **Package in-progress:** {populated per workspace}
- **Packages not started:** {populated per workspace}

> Update this section when a package transitions. This gives the orchestrator lightweight awareness without loading full state files.

---

## What This File Does NOT Do

- Does NOT contain any package workflow logic (that stays in each package's core file).
- Does NOT make routing decisions for the family (that is AI-FLO's job).
- Does NOT auto-activate packages based on state changes.
- Does NOT replace the activation key system — it supplements it with intent detection.

---

*Session Orchestrator v1.0.0 (Claude Code variant) | AI-* PDLC Family | Author: Maheri*
