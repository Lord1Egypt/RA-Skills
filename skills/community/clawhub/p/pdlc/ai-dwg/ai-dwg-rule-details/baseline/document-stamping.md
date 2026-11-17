<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Document Stamping & Obsolescence Protocol

## Purpose

Defines two DWG behaviors that keep every file in the generated workspace traceable to a baseline version:
1. **Per-document baseline stamp** (Approach C) — every file DWG carries into the workspace gets a version mark showing when it was last substantively changed AND the latest baseline that confirmed it.
2. **Obsolescence protocol** — when a re-baseline removes a file from the governed surface, DWG soft-deletes it (moves to a local `obsolete/`) with an AI-blocking marker, never hard-deletes.

**Condition:** Stamping — every generated file, always. Obsolescence — only on re-baseline when a peer-input drops a file.

**Grounding:** Implements `MIDFLIGHT_DRIFT_GOVERNANCE_DESIGN.md` §4.3.1 (stamp) + §4.3.2 (obsolescence) + layout design Part 3C.

---

## MANDATORY: Stage Sub-Role — Audit Specialist

Audit Specialist mindset (traceability, provenance, reversibility). ADDS a dimension — does NOT replace the primary role.

### Anti-Patterns
- Do NOT hard-delete a file that leaves the governed surface — soft-delete only
- Do NOT rewrite a file's whole content just to bump the confirmed version — one-line stamp edit
- Do NOT let any AI read an obsoleted file — the marker must block it

---

## Part 1 — Per-Document Baseline Stamp (Approach C)

**Rule: Every file DWG places or updates in the workspace carries a baseline stamp as its first line.**

The stamp shows TWO versions:
- `v{N}` — the baseline version that last **substantively changed** this file's content
- `(confirmed v{M})` — the latest baseline version that reviewed and kept this file unchanged

On creation/modification, both equal the current version: `v3 (confirmed v3)`. On a later re-baseline that doesn't touch the file, only the confirmed bumps: `v3 (confirmed v5)`.

### Format per file type

| File Type | Stamp Format |
|-----------|-------------|
| Markdown (`.md`) | `<!-- DWG-BASELINE: v{N} (confirmed v{M}) \| {projectId} \| {timestamp} -->` |
| YAML (`.yml`, `.yaml`) | `# DWG-BASELINE: v{N} (confirmed v{M}) \| {projectId} \| {timestamp}` |
| JSON (`.json`) | No inline stamp — JSON has no comments. Tracked via manifest only. |
| TS/JS (`.ts`, `.tsx`, `.js`) | `// DWG-BASELINE: v{N} (confirmed v{M}) \| {projectId} \| {timestamp}` |
| Python (`.py`) | `# DWG-BASELINE: v{N} (confirmed v{M}) \| {projectId} \| {timestamp}` |
| Dotfiles (`.gitignore`, `.env.example`) | `# DWG-BASELINE: v{N} (confirmed v{M}) \| {projectId} \| {timestamp}` |
| Docker (`Dockerfile`) | `# DWG-BASELINE: v{N} (confirmed v{M}) \| {projectId} \| {timestamp}` |

**JSON rule:** files like `package.json`, `tsconfig.json` have no comment syntax — tracked ONLY via the manifest, no inline stamp. GCE uses the manifest for these.

### Stamping rules

- On initial generation: both values = `v1`.
- On re-baseline that **modifies** the file: both values → new version.
- On re-baseline that **does NOT modify** the file: only `confirmed` bumps (single-line diff).
- Machine-parseable: GCE reads provenance (substantive-change version) AND currency (confirmed version).
- Complements the manifest (per-file traceability vs. whole-surface truth) — does not replace it.

### Queries the stamp answers

- **"What changed at vN?"** → filter files where the primary version = vN.
- **"Is this file current?"** → confirmed version matches the latest baseline.

### Tradeoff (acknowledged)

Approach C touches the first line of every governed file on every re-baseline (to bump `confirmed`). For a 100+ file workspace that's 100 single-line diffs in one "DWG re-baseline v{N}" commit. Accepted: diffs are trivial, git handles them, the alternative (silent staleness) is worse, and reviewers learn to skip the re-baseline commit.

---

## Part 2 — Obsolescence Protocol (Soft-Delete + AI Block)

**Rule: When a re-baseline removes a file from the governed surface, DWG MUST NOT hard-delete it. It moves the file to an `obsolete/` subfolder within the SAME directory the file is nested in.**

### Mechanics

1. Move to a sibling `obsolete/` under the file's current parent (NOT a single root-level folder):
   - `backlog/epics/EPIC-003_stories/US-012.md` → `backlog/epics/EPIC-003_stories/obsolete/US-012.md`
   - `ux/wireframes/WF-05_Dashboard.md` → `ux/wireframes/obsolete/WF-05_Dashboard.md`
   - `backlog/DEFINITION_OF_READY.md` → `backlog/obsolete/DEFINITION_OF_READY.md`
   - `.governance/*` NEVER obsoleted this way (runtime state)

2. Prepend an AI-blocking marker as the first line (above the frozen baseline stamp):

```markdown
<!-- DWG-OBSOLETE: Retired in v{N} on {date}. Reason: {reason}. Do NOT reference, include, or act on this content. -->
<!-- DWG-BASELINE: v{N-1} (confirmed v{N-1}) | {projectId} | {original-timestamp} -->
# [OBSOLETE] {original title}
```

3. Record a `retire` entry in the baseline disposition ledger:

```yaml
dispositionLedger:
  - driftId: RET-001
    disposition: retire
    fromVersion: v3
    toVersion: v4
    element: PROD-005
    rationale: "Epic removed from scope; stories no longer applicable"
    retiredFiles: [backlog/epics/EPIC-003_stories/US-012.md, …]
    resolvedBy: AI-POLC
    timestamp: {ISO}
```

4. Emit the AI-blocking rule into workspace steering: *"Never read or act on files under any `obsolete/` subfolder or files containing the `DWG-OBSOLETE` marker."*

### `retire` is a baseline-maintenance action, NOT a drift disposition

`retire` does NOT go through the drift pipeline (detect→route→digest). It is triggered by **upstream peer-input delta** — POLC removes an epic → DWG detects the file is no longer sourced → retires it. Recorded in the ledger for audit completeness; distinct lifecycle (no GCE detection, no FLO routing).

### Obsolescence Trigger Path

1. Upstream package removes content (POLC drops an epic, ADLC drops a constraint, UXD drops a wireframe)
2. DWG detects the delta on re-baseline (peer-input no longer sources the file)
3. DWG moves the unsourced file to its local `obsolete/`
4. DWG records the `retire` ledger entry
5. DWG updates `WORKSPACE_CONTEXT_MAP.md` (removes the pointer)

**Who triggers:** Only DWG (sole baseline writer). A human wanting a file retired requests it via the upstream package; DWG picks up the delta.

**Edge case — user manually deletes a governed file:** GCE detects this as HARD drift (baseline expects it, reality lacks it). This is NOT obsolescence — it's drift. Restore (Conform) or change the design upstream (Amend → re-baseline → retire).

### Why local `obsolete/` (not root-level) and why soft-delete

- Local: preserves directory context; avoids a flat cross-domain dump; easy selective restore
- Soft-delete: audit trail, reversibility, safety (work built on the baseline isn't lost), transparency
- GCE excludes all `obsolete/` paths from drift scans — a retired file cannot drift

---

## Interaction with Other Files

| Related | Relationship |
|---------|--------------|
| `baseline/baseline-generation.md` | Stamps carry the version; ledger records retirements |
| `baseline/workspace-manifest-generation.md` | Manifest is whole-surface version; stamp is per-file |
| `reconciliation/re-baseline.md` | Drives the confirmed-bump + obsolescence on delta |
| (AI-GCE) | Reads stamps for provenance; excludes `obsolete/` from scans |

---

## Output Validation

- [ ] Every generated `.md`/`.yaml`/`.ts`/`.py`/dotfile carries an Approach C stamp as first line
- [ ] JSON files tracked via manifest only (no inline stamp)
- [ ] On re-baseline: modified files bump both versions; unchanged files bump only `confirmed`
- [ ] Retired files moved to local `obsolete/` (not root), never hard-deleted
- [ ] `DWG-OBSOLETE` marker prepended; original stamp frozen
- [ ] `retire` ledger entry recorded
- [ ] AI-blocking rule present in workspace steering
- [ ] Context map pointer removed for retired files
