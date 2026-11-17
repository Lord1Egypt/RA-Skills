# AI-* Family — Naming & Ownership Convention

**Version:** 1.1.0 (RATIFIED — hybrid approach approved; multi-project project-folder convention added 2026-06-17)
**Date:** 2026-06-17
**Author:** Maheri
**Status:** 🟢 Ratified — the §5 A-dominant hybrid is approved. Propagation per §7 complete. v1.1.0 (2026-06-17) adds the multi-project project-folder convention (§5.5).

---

## 1. Purpose

Define **one** convention, across the whole AI-* family, that makes two things unambiguous for any file that ends up in a user's workspace:

1. **Provenance** — which package produced this file?
2. **Ownership** — is it tool-owned (regenerated, hands-off) or the team's to edit?

Today these answers are invisible or inconsistent. This document fixes that.

---

## 2. The Problem (Why This Doc Exists)

The family names things differently at each layer. Layer 1 is clean; layers 2–4 are not.

| Layer | What it covers | Current state | Verdict |
|-------|----------------|---------------|---------|
| **1. Engine files** | The package's own machinery installed into a workspace | Namespaced folders: `ai-{pkg}-rules/`, `ai-{pkg}-rule-details/` | ✅ Consistent |
| **2. Generated artifacts** | Files a package writes onto the user's project | AI-DWG: generic flat (`tech-stack.md`); AI-GCE steering: semi-prefixed (`compliance-*.md`); AI-GCE hooks: generic flat (`naming-check.json`) | ❌ Three styles, no provenance |
| **3. Hooks** | Automation files in `.kiro/hooks/` | Builder uses `*.kiro.hook`; GCE templates use `*.json` | ❌ Two conventions, no producer marker |
| **4. Builder steering** | This repo's own `.kiro/steering/` | Package-role rules, personas, and user files sit flat together; `ai-{pkg}-rules.md` collides conceptually with the install folder `ai-{pkg}-rules/` | ❌ No ownership grouping |

**Symptoms a user hits:**
- `workspace-rules.md` — written by AI-DWG, or hand-authored? No way to tell.
- `tech-stack.md` — safe to edit, or overwritten on next re-derivation? Unknown.
- A hook fires — which package owns it, and where do I report a bug? Unclear.

---

## 3. Root Cause

There is a real design reason layer 2 went generic: **DWG-generated steering files are meant to become the team's own living documents** (developers edit `tech-stack.md`, `coding-standards.md` daily). Prefixing them `ai-dwg-tech-stack.md` would make them feel like borrowed vendor files nobody owns.

The mistake was not the generic names — it was **never defining a provenance mechanism to replace the prefix.** Ownership became invisible. DWG rule 3 already half-solves this (it requires a provenance comment); the family just never standardized or universalized it.

---

## 4. Two Approaches (Decision Input)

The **Hybrid picks** column shows which approach the §5 hybrid adopts for that dimension — and for which artifact class when it differs.

| Dimension | Approach A — Provenance metadata (generic names + front-matter) | Approach B — Filename prefixes (`ai-dwg-tech-stack.md`) | **Hybrid picks** |
|---|---|---|---|
| Ownership visible in file tree | No (open the file) | Yes (from the name) | **B for tool-owned** (dedicated folders: `.governance/`, `.kiro/hooks/`); A for living |
| Ownership visible inside file | Yes (explicit fields) | No | **A** (all artifacts carry metadata) |
| Provenance richness | High (source doc, version, date, ownership state) | Low (producing package only) | **A** (rich metadata everywhere) |
| Feels like the project's own files | Yes | No (looks tool-owned) | **A for living** (team adopts them); B-folder for tool-owned (kept apart) |
| Natural for developers to edit | Yes | Awkward (prefix implies "don't touch") | **A for living**; tool-owned intentionally hands-off (B-folder) |
| Re-derivation overwrite safety | Tool reads `ownership` field | Tool keys off prefix; user edits ambiguous | **A** (`ownership` field) reinforced by **B-folder** boundary |
| Collision with user files | Possible (resolved by metadata) | Eliminated | **B-folder for tool-owned** (no collision); A-metadata resolves living |
| Cross-tool portability | Most tools ignore unknown front-matter | Filename works everywhere | **A** (front-matter), folders also portable |
| Kiro fileMatch impact | None (names unchanged) | Must rewrite every `fileMatchPattern` | **A** (names unchanged — no fileMatch churn) |
| Conflicts with  marker files | No | **Yes** — would rename `workspace-rules.md` etc. that downstream detection depends on | **A** (marker filenames preserved) |
| "Show me all DWG output" | Grep metadata | Trivial (`ls ai-dwg-*`) | **A** (grep `generated-by`); B-folder makes tool-owned obvious |
| Blast radius to adopt | Lower (additive header) | Higher (renames ripple into docs, patterns, scripts) | **A** (additive — folders already exist) |
| Reversibility | Easy (strip header) | Hard (names baked everywhere) | **A** (strip header to revert) |
| Best fit | Living artifacts the team adopts | Tool-owned artifacts kept hands-off | **A → living artifacts; B-folder → tool-owned artifacts** |

**Reading the Hybrid column:** the hybrid is **A-dominant** — it uses Approach A (metadata) as the universal ownership mechanism, and borrows from B only as a **folder boundary** (`.governance/`, `.kiro/hooks/`) for tool-owned files, never as a filename prefix. This keeps  marker files intact while still giving tool-owned files visible separation in the tree.

**Critical constraint:** Approach B applied to marker files (`workspace-rules.md`, `adlc-state.md`, `pilc-state.md`) **breaks chain detection**. So pure-B is not viable for those files regardless of preference — which is why the hybrid uses B only at the folder level, never on marker filenames.

---

## 5. Recommended Convention (Hybrid) — ✅ APPROVED

The two approaches are not mutually exclusive. Use each where it fits:

> **A (metadata)** for *living* artifacts the team adopts and edits.
> **B-style separation (dedicated folder, not filename prefix)** for *tool-owned* artifacts that should stay hands-off.

### 5.1 Rule by artifact type

| Artifact type | Producer(s) | Naming rule | Ownership mechanism |
|---|---|---|---|
| **Engine files** (`ai-{pkg}-rules/`, `ai-{pkg}-rule-details/`) | all | Namespaced folder (unchanged) | Folder name = producer; not user-edited |
| **Living steering** (`tech-stack.md`, `coding-standards.md`, `workspace-rules.md`, …) | AI-DWG | Generic name (unchanged — also protects  markers) | **Provenance front-matter (Approach A)** |
| **Project config** (`.editorconfig`, `docker-compose.yml`, `CODEOWNERS`, operational docs) | AI-DWG | Generic name (ecosystem-standard) | Provenance front-matter where the format allows comments |
| **Compliance rules** (`.governance/rules/*.md`) | AI-GCE | Generic name **inside the `.governance/` folder** | Folder = tool-owned boundary (Approach B by folder); front-matter for source trace |
| **Hooks** (`.kiro/hooks/*`) | AI-GCE | Standard `.json` extension (Kiro IDE requirement); provenance via `generatedBy` field inside the JSON | `generatedBy` field inside the JSON |
| **GCE steering enrichments** (`compliance-*.md`) | AI-GCE | Keep `compliance-` prefix (already a meaningful namespace) | Provenance front-matter |

### 5.2 Provenance front-matter schema (for `.md` artifacts)

```yaml
---
generatedBy: AI-DWG           # producing package
generatedVersion: 1.0.0       # package version at generation time
source: architecture/08_API_Architecture.md   # upstream doc(s) that justified this file
generatedOn: 2026-06-09
ownership: generated          # generated | hybrid | user
---
```

- `ownership: generated` — fully tool-managed; re-derivation may overwrite.
- `ownership: hybrid` — tool-seeded, team-edited; re-derivation must preserve content between `<!-- custom -->` markers (aligns with DWG rule 6 / GCE rule 8).
- `ownership: user` — promoted to team ownership; tool treats as read-only.

> **Key names LOCKED (2026-06-10, Plan Phase 0.4):** `generatedBy`, `generatedVersion`, `source`, `generatedOn`, `ownership`. **camelCase** is used across both `.md` front-matter and hook JSON for consistency with Kiro's existing front-matter keys (`fileMatchPattern`, `inclusion`). These names are final for propagation.

> **Traceability keys LOCKED (2026-06-13, OI-030 Phase A):** `id`, `originType`, `derivedFrom`, `mergedFrom`, `projectId`, `provenanceVersion`, `aliasOf`. These extend the provenance front-matter for identity-transformation traceability. Defined in `contracts/TRACEABILITY_CONTRACT.md`. Same camelCase convention applies.

### 5.3 Hook provenance (for `*.kiro.hook` JSON)

```json
{
  "name": "Security Gate Check",
  "generatedBy": "AI-GCE",
  "generatedVersion": "1.0.0",
  "source": ".governance/rules/security-compliance.md",
  "enabled": true,
  "when":  { "...": "..." },
  "then":  { "...": "..." }
}
```

> **Key names LOCKED (2026-06-10, Plan Phase 0.4):** hooks use the same provenance keys as `.md` artifacts — `generatedBy`, `generatedVersion`, `source` (renamed from the earlier `sourceRule` for one consistent key across artifact types). The `source` value holds the upstream rule path for hooks, the upstream doc path for steering.

### 5.4 Builder workspace `.kiro/steering/` ownership classes

This repo (the builder) should make its three ownership classes scannable and document the install-folder collision:

| Class | Pattern | Example | Owner |
|---|---|---|---|
| Persona | `persona-*.md` | `persona-cto-architect.md` | Builder-internal |
| Package role rule | `ai-{pkg}-rules.md` | `ai-pilc-rules.md` | Builder-internal |
| User / workspace | descriptive, no `ai-`/`persona-` prefix | `workspace-rules.md`, `model-disclosure.md` | Human-authored |

> **Naming clash to document, not rename:** the builder file `ai-{pkg}-rules.md` (a steering role file in *this* repo) is a different thing from the install folder `ai-{pkg}-rules/` (the package machinery copied into a *user* workspace). Same stem, different artifact. The convention records this so future sessions don't conflate them.

### 5.5 Non-negotiable constraints (carried from prior lessons learned)

- **Marker files keep their names** — `pilc-state.md`, `adlc-state.md`, `workspace-rules.md`, and the `.kiro/hooks/` folder are detection anchors. Never rename or prefix them.
- **Each package owns its governance registers under its own output folder** — provenance metadata does not change folder placement. In multi-project mode the per-project spine consolidates this at the project root (see the project-folder note below + `MANAGEMENT_FRAMEWORK_CONTRACT.md` §8).
- **Templates stay 100% generic** — provenance fields are filled at generation time with `{placeholder}` in the package templates themselves.

### Project-folder convention (multi-project mode, 2026-06-17; family-ws prefix 2026-06-22)

- **Project folders use a stable domain key, not a package prefix.** In a multi-project workspace, each project's output nests under `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/`. The `PRJ-{ABBREV}` handle is a **stable domain key** (the project's identity), which is the explicit exception  allows — the same class as the `{NNN}-{slug}/` idea folders. It is **not** an ownership-by-path marker; classification still lives in metadata (`projectId`, etc.).
- **"Project root" = `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/`** in multi-project mode (it was the workspace root in the legacy single-project layout). All sibling contracts read "project root" through this definition.
- **Canonical key stays in metadata.** The folder uses the readable short handle; the full `PRJ-{ABBREV}-{YYYY}-{NNN}` remains the canonical `projectId` correlation key (see `TRACEABILITY_CONTRACT.md`). The generated dev workspace folder is slug-based (`{slug}-workspace/`) for clean IDE logging.
- **Source of truth:** the `projects/` layout, registry, and active-pointer conventions are defined in `OUTPUT_AND_STATE_CONTRACT.md`; this section only records the naming/ownership stance on the project folder.

---

## 6. Decision — ✅ RESOLVED

**Decision:** The **§5 A-dominant hybrid** is approved (2026-06-09).

- ✅ **Selected: Hybrid** — metadata (Approach A) as the universal ownership mechanism, with Approach B used only as a **folder boundary** (`.governance/`, `.kiro/hooks/`) for tool-owned files, never as a filename prefix. Marker files keep their names.
- ❌ Pure A — rejected (no visible separation for tool-owned files).
- ❌ Pure B — rejected (breaks  marker-file detection).

Propagation proceeds per §7.

---

## 7. Rollout (Authorized — In Progress)

| # | Step | Status |
|---|------|--------|
| 1 | Lock the front-matter schema (§5.2) and key names | ✅ Done — schema ratified (2026-06-09); **key names locked camelCase 2026-06-10, Plan Phase 0.4** (`generatedBy/generatedVersion/source/generatedOn/ownership`; `sourceRule→source`) |
| 2 | Add a "Naming & Ownership" pointer section to `FAMILY_STRUCTURE.md` and annotate PART 2 output trees with `ownership:` markers | ✅ Done (pointer section + ownership map added) |
| 3 | Add the provenance requirement to each package's rules/README (all 10 packages) | ✅ Done (2026-06-10, Plan 2.2) — original rollout to 6: PILC, ADLC, DWG, GCE, ILC, TGE. **Extended 2026-06-15c (OI-054):** the 4 later packages (POLC, PPM, UXD, FLO) were born-compliant with the convention; all 10 now carry provenance. |
| 4 | Update DWG + GCE templates to emit the front-matter / `generatedBy` field | ✅ Done (2026-06-10, Plan 2.2) — 77 files: 40 DWG templates + 23 GCE templates + 14 hook JSONs |
| 5 | Unify GCE hook templates on `*.kiro.hook` + `generatedBy`; update INSTALL and uninstall scripts | ✅ Done (2026-06-10, Plan 2.2) — **extension rename SKIPPED** (Kiro requires `.json`; §5.1 updated); provenance achieved via `generatedBy` JSON field (Step 4E) |
| 6 | Register any new tables/files per `FAMILY_TABLE_MAP.md` rules | ✅ Done (2026-06-10) — verified: no template files carry the family table; no new registrations needed |

---

## 8. Change Log

| Version | Date | Change |
|---------|------|--------|
| 0.1.0 | 2026-06-09 | Initial draft — problem analysis, two-approach comparison, hybrid recommendation, schema. Pending §6 decision. |
| 1.0.0 | 2026-06-09 | Hybrid approach approved and ratified. §6 resolved, §7 rollout authorized. Added Hybrid-picks column to §4. |
| 1.0.1 | 2026-06-10 | Front-matter key names locked (Plan Phase 0.4): camelCase across `.md` + hook JSON; `sourceRule` renamed to `source`. §5.2/§5.3 finalized, §7 step 1 closed. |
| 1.1.0 | 2026-06-17 | Added the multi-project **project-folder convention** to §5.5: `projects/PRJ-{ABBREV}-{slug}/` as a Lesson-40 stable-domain-key exception; "project root" redefined for multi-project mode; canonical `projectId` stays in metadata. Source of truth = `OUTPUT_AND_STATE_CONTRACT.md`. |
| 1.1.1 | 2026-06-22 | **Family-workspace prefix** (install-lock design): §5.5 "project root" now nests under the family workspace → `pdlc-ws/projects/PRJ-{ABBREV}-{slug}/`. Convention unchanged; path gains the `pdlc-ws/` prefix. |
