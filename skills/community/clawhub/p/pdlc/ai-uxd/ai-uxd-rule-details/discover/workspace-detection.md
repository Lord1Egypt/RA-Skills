<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 1: Workspace Detection & Input Ingestion

## Purpose

Detect available inputs, determine the operating mode, assess project complexity, set depth level, and create the state file. This is the foundation stage — everything downstream depends on correct detection here.

---

## MANDATORY: Stage Sub-Role — Business Analyst

During this stage, layer the Business Analyst lens on top of the UX Designer primary:

**Behavioral Shifts:**
- Read input documents analytically — extract user types, business goals, constraints, and scope boundaries
- Identify ambiguity and gaps in the input that will need research in Stage 2
- Structure extracted information into categories (users, goals, constraints, unknowns)
- Ask clarifying questions about scope before making assumptions

**Anti-Patterns for This Stage:**
- DO NOT start designing or suggesting UI solutions — this stage is pure analysis
- DO NOT assume user types from job titles — look for behavioral descriptions
- DO NOT skip reading predecessor documents even if the user provides a verbal summary

**Quality Check:**
- [ ] All available predecessor documents have been read (not summarized by user)
- [ ] User types are extracted as behavioral descriptions, not just role labels
- [ ] Gaps and unknowns are explicitly flagged for Stage 2 research
- [ ] Mode and depth are confirmed with the user, not assumed

---

## Depth Adaptation

| Depth | Detection Behavior |
|-------|-------------------|
| **Minimal** | Quick scan; 2-3 questions; accept defaults readily |
| **Standard** | Full scan; balanced questions; confirm key decisions |
| **Comprehensive** | Deep scan; extended questions; probe for hidden complexity |

---

## Steps

### Step 1: Detect Input Mode

Based on welcome message selection OR automatic scanning. Scan the **default multi-project layout** first (`pdlc-ws/projects/*/`), then legacy locations:

| Mode | Detection Method |
|------|-----------------|
| A (PIP + PBP) | Scan for `pdlc-ws/projects/*/pip/pilc-state.md` AND `pdlc-ws/projects/*/backlog/polc-state.md` (same project) — the normal chain flow (PILC → POLC → UXD) |
| B (PIP only) | `pdlc-ws/projects/*/pip/pilc-state.md` without a `backlog/polc-state.md` sibling (POLC skipped or not yet run) |
| C (Standalone) | No markers found; user provides brief |
| D (Brownfield) | User indicates existing design system; scan for design artifacts |

**Detection strategy:** scan `pdlc-ws/projects/*/` → legacy paths (`./`, `./pip/`, `./architecture/`) → user-provided path → ask user.

**Peer marker scan (enrichment — architecture constraints):** alongside the mode markers, also scan for `pdlc-ws/projects/*/architecture/adlc-state.md` — if present (rare at UXD start since ADLC runs after UXD in the sequential chain), it feeds the Architecture→UX constraint loop in the re-entry section below. Absence is the normal case and never blocks.

**Active-project selection:** if more than one project is present, read `pdlc-ws/projects/PROJECTS.md` for the ★ active project and prompt the user to work on the active project or pick another (`OUTPUT_AND_STATE_CONTRACT.md` §8).

### Step 2: Read Predecessor Output

**Mode A (PIP + PBP):**
- Read PIP: project vision, stakeholders, user types, scope, success criteria, constraints
- Read PBP: product vision, value goals/OKRs, prioritized epics, strategic themes, target segments — these focus UX research on the users and problems that matter most to the product strategy
- Extract: user segments from both PIP + PBP; success metrics that inform design KPIs; scope boundaries that constrain UX ambition

**Mode B (PIP only):**
- Read PIP: same as Mode A (PIP part)
- Note: no product backlog context available — UX research scope comes from PIP alone. If POLC runs later and a `polc-state.md` appears, the peer-read below will pick it up adaptively.

**Mode C (Standalone):**
- Ask for product/brand brief (document or verbal description)
- Extract: product vision, target audience, brand identity, competitive landscape, known constraints

**Mode D (Brownfield):**
- Scan for existing design artifacts: style guides, component libraries, token files, brand guidelines
- Inventory what exists vs. what's missing
- Identify governance gaps (what exists but is ungoverned)

**Architecture constraint loop — AI-ADLC (adaptive, if `adlc-state.md` appears):**

AI-ADLC runs **after** AI-UXD in the sequential chain (POLC → UXD → ADLC). In rare cases (e.g., a team running packages in parallel, or a resumed project), an Architecture Package may already exist. If `adlc-state.md` is present at UXD start, read it for platform constraints (web/mobile/native, BFF presence, UI containers, frontend technology, performance requirements) and extract technical constraints that affect UX (platform, responsive needs, offline requirements). If absent (the normal case), UX proceeds freely — the constraint loop below handles late-arriving AP.

**Architecture-constraint re-entry (Architecture→UX loop, same-layer — OI-099):**

AI-ADLC constraints are consumed once at intake (Mode A). But ADLC runs concurrently and may finalize feasibility *after* UX flows already exist — a late latency/data/platform ceiling can force a simpler interaction. To make this a real loop (not a one-shot read):

1. **Track what was seen.** In `uxd-state.md`, record an `Upstream Signals` entry: `lastApStateSeen: {adlc-state.md last-updated timestamp or hash, or "none"}`.
2. **Detect change on start/resume.** When UXD starts or resumes, compare the current `adlc-state.md` (if present) against `lastApStateSeen`. If it newly appeared or changed after UX flows/screens were produced → trigger a re-entry review.
3. **Non-destructive review.** Surface which flows/screens are affected by the new/changed constraint (e.g., a real-time expectation now capped by a data-refresh limit) and **propose** targeted adjustments. Never auto-edit flows — the designer decides (mirrors the reconciliation pattern,).
4. **Re-record** `lastApStateSeen` after the review.

**Standalone-safe:** absent `adlc-state.md` → no constraint loop; UX proceeds as today.

### Step 3: Assess Complexity and Set Depth

| Signal | Points Toward |
|--------|--------------|
| ≤2 user types, single platform | Minimal |
| 3-5 user types, multi-platform OR data-rich | Standard |
| 6+ user types, enterprise, regulated, accessibility-critical | Comprehensive |

Present recommendation to user with rationale. Accept override.

### Step 4: Detect Conditional Feature Triggers

| Feature | Trigger Signal |
|---------|---------------|
| Multi-Brand Theming | Brief mentions >1 brand, white-label, partner branding, OR dark mode |
| i18n/RTL/Localization | Brief mentions >1 language, international users, RTL languages |
| Service Blueprints | Comprehensive + "service", "multi-channel", "backstage process" |
| Empathy Maps | Comprehensive depth automatically |

### Step 5: Create State File & Project Structure

**Adopt or mint the Project ID (correlation key):**
- **Adopt (Mode A/B — predecessor exists):** read `projectId`, `projectHandle`, `projectRoot` from the predecessor marker (`pilc-state.md` / `polc-state.md`) and use them unchanged — never re-mint. `{project_root}` = the predecessor's project root; UXD output → `{project_root}/ux/`.
- **Mint (Mode C/D — UXD originates, no predecessor):** UXD is originator-eligible (`OUTPUT_AND_STATE_CONTRACT.md` §7). Mint the **family correlation key** `PRJ-{ABBREV}-{YYYY}-{NNN}` (ask the user for name/abbreviation), create `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/`, and seed the `pdlc-ws/projects/PROJECTS.md` registry row (★ active). Output → `{project_root}/ux/`.
  > Note: UXD no longer mints a package-local `UXD-{YYYY}-{NNN}` ID — the family correlation key `PRJ-{ABBREV}-{YYYY}-{NNN}` is the single identity, so PPM/FLO can correlate UXD output with the rest of the project.

**Generate `ux/uxd-state.md`** (from `templates/uxd-state.md`) with:
- `projectId`, `projectHandle`, `projectRoot`, `outputRoot` (= `{project_root}/ux/`)
- Mode, depth, conditional features
- Current Phase: Discover, Current Stage: 1
- Progress table: Stage 1 = `🔄 Active`, all others = `⏳ Pending`; Downstream Signals: all Pending

**Contribute to the shared spine** at `{project_root}/management_framework/` (append-if-exists, create-if-absent) per `MANAGEMENT_FRAMEWORK_CONTRACT.md` v1.2.0 — project-qualified IDs `UXD-{ABBREV}-{TYPE}-{N}` (UX-design governance decisions, e.g. accessibility-baseline decisions). Update `pdlc-ws/projects/PROJECTS.md`: set this project's `UXD` column to `wip`.

> **Brownfield:** if UXD output already exists in an older flat layout (`./ux-design/`, `./uxd/`), do NOT force-relocate — offer a one-time non-destructive restructure into `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/ux/`, or operate in the standard location alongside the legacy output (never force-move existing files). This is distinct from Mode D (existing *design artifacts* to govern).

### Step 6: Confirm with User

Present summary:
```
Project Detection Summary
━━━━━━━━━━━━━━━━━━━━━━━━
Mode: {A/B/C/D} — {description}
Depth: {level} — {rationale}
Conditional features:
  • Multi-Brand Theming: {Yes/No} — {trigger}
  • i18n/RTL: {Yes/No} — {trigger}
  • Service Blueprints: {Yes/No} — {trigger}
  • Empathy Maps: {Yes/No} — {trigger}

Key inputs detected:
  • User types: {list}
  • Platform: {web/mobile/native/multi}
  • Constraints: {list}
  • Product value focus (AI-POLC): {value goals / OKRs / target outcomes — or "none (polc-state.md absent)"}
  • Unknowns: {list — these drive Stage 2 research}

Approve this configuration? [Y / Adjust]
```

---

## Gate

**Approval required before proceeding to Stage 2.**

User must confirm:
- Mode selection is correct
- Depth level is appropriate
- Conditional feature flags are accurate

If user adjusts any parameter → update state file → re-present summary.

---

## Log

Update `uxd-state.md`:
- Progress table: set Stage 1 Status to `✅ Done`, record date and artifact (`uxd-state.md`); set Stage 2 to `🔄 Active`
- Current Stage: 2

---

## Transition

After gate approval:
```
Stage 1 complete. Moving to Stage 2: Research Planning & Synthesis.

I'll now plan the research approach to fill the unknowns we identified
and build the evidence base for persona development.
```

Load `discover/research-planning.md`.
