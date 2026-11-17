<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mode 3 — Brownfield Overlay Flow

## Purpose

The step-by-step orchestration for **Mode 3: Brownfield Overlay** — layering governance and steering onto an existing codebase WITHOUT disturbing existing code, configs, or team conventions. The core (`core-generator.md`) carries the Mode 3 intent + index; this file carries the detailed flow, the Mode-1-vs-Mode-3 overrides, the additive config-merge logic, and the output summary. Load it when Mode 3 is detected (after the pre-mode gate passes).

> Conditional steering content lives in `mapping/brownfield-to-steering.md` + `templates/steering/brownfield-patterns.md`. Mode-3 pipeline summary + key differences live in `common/process-overview.md`.

---

## When to Use

Mode 3 is for existing codebases that were built WITHOUT AI-DWG governance. The codebase has code, possibly its own conventions, but no `rules/` files (or only partial ones). The goal: layer governance and steering onto an existing project WITHOUT disturbing existing code, configs, or team conventions.

**Typical scenarios:**
- Team has a running project and wants to adopt AI-DWG governance retroactively
- Project was started without architecture steering and needs structure
- AI-ADLC was run against an existing system (Mode D: Brownfield) and now AI-DWG needs to overlay

## Interaction Model

1. **User invokes:** "Add governance to this workspace" / "Overlay steering" / "Retrofit AI-DWG"
2. **AI detects** existing workspace state (code, configs, conventions)
3. **AI asks** 3-5 configuration questions (see below)
4. **AI generates** steering files + non-conflicting operational docs
5. **AI merges** configs (additive only —.gitignore, CODEOWNERS)
6. **AI presents** summary with what was added vs. what was skipped (to respect existing)
7. **User reviews** — done

## Configuration Questions (Mode 3 Specific)

| # | Question | Purpose | Default |
|---|----------|---------|---------|
| 1 | Where is the Architecture Package? | AP path for deriving steering content | Ask user (no default) |
| 2 | Do you have existing conventions I should respect? | Identify README, CONTRIBUTING, etc. that should NOT be overwritten | Auto-detect existing files |
| 3 | Should I generate folder structure? | Brownfield = code already exists; usually NO | No (skip source folders) |
| 4 | Any existing `rules/` files to preserve? | Partial overlay scenario | Auto-detect and preserve |
| 5 | Merge or skip config files (.gitignore, CODEOWNERS)? | Respect vs. enhance existing configs | Merge (additive) |

---

## Brownfield Overlay Flow

```
STEP 1: DETECT EXISTING — Scan Workspace State
───────────────────────────────────────────────
Scan the target workspace and catalog what exists:
• Source code folders (DO NOT modify)
• Existing rules/ files (preserve; fill gaps only)
• Existing config files (.gitignore,.editorconfig, CODEOWNERS, docker-compose.yml)
• Existing operational docs (README.md, CONTRIBUTING.md, etc.)
• Existing conventions (detect from code: naming patterns, folder structure, test locations)

Build inventory: EXISTING vs. MISSING

STEP 2: READ — Load Architecture Package
─────────────────────────────────────────
Same as Mode 1 STEP 1 — load all AP artifacts.
Additionally check `adlc-state.md` for:
• `Input Mode: Brownfield` → triggers brownfield-patterns.md conditional steering
• Extension awareness (same as Mode 1)

Load: common/ap-reading-guide.md

STEP 3: MAP — Generate Steering Content
────────────────────────────────────────
Same mapping rules as Mode 1, with these OVERRIDES:

| Category | Mode 1 Behavior | Mode 3 Override |
|----------|----------------|-----------------|
| Steering files (rules/) | Generate all | Generate ALL (steering doesn't conflict with code) |
| Source folders | Create from C4 L3 | SKIP — code already exists |
|.gitignore | Generate fresh | MERGE — add missing entries, preserve existing |
|.editorconfig | Generate fresh | SKIP if exists; generate if missing |
| docker-compose.yml | Generate fresh | MERGE — add missing services, preserve existing |
| CODEOWNERS | Generate fresh | MERGE — add missing entries, preserve existing |
| README.md | Generate fresh | SKIP if exists (team's README is sacrosanct) |
| PROJECT_INSTRUCTIONS.md | Generate fresh | Generate (new file — won't conflict) |
| CONTRIBUTING.md | Generate fresh | SKIP if exists; generate if missing |
| CICD_GUIDE.md | Generate fresh | Generate (new file — won't conflict) |
| DEFINITION_OF_DONE.md | Generate fresh | Generate if missing; skip if exists |
| TEAM_AGREEMENTS.md | Generate fresh | SKIP if exists; generate if missing |
| ONBOARDING.md | Generate fresh | SKIP if exists; generate if missing |
| PR template | Generate fresh | SKIP if exists; generate if missing |
| Planning templates | Generate fresh | Generate (new directory — won't conflict) |
| management_framework/ | Generate fresh | **Spine-aware:** detect marker (`MANAGEMENT_FRAMEWORK.md`). If spine exists → append `DWG-*` entries. If missing → generate. If non-conforming (no marker) → add marker + Phase columns non-destructively. |

**Key rule:** Steering files are ALWAYS generated (they live in rules/ which is unlikely to have existing content in a non-AI-DWG workspace). Everything else respects existing files.

Also load: mapping/brownfield-to-steering.md (for brownfield-specific conditional steering)

STEP 4: MERGE CONFIGS — Additive Only
──────────────────────────────────────
For each config file that exists AND AI-DWG wants to modify:

###.gitignore Merge
- Read existing.gitignore
- Identify entries AI-DWG would add (from tech stack)
- Add ONLY entries not already present
- Add under a comment: `# AI-DWG additions ({date})`
- NEVER remove existing entries

### CODEOWNERS Merge
- Read existing CODEOWNERS
- Identify module ownership from C4 L3
- Add ONLY paths not already covered
- Add under a comment: `# AI-DWG additions ({date})`
- NEVER modify existing ownership rules

### docker-compose.yml Merge
- Read existing docker-compose.yml
- Identify services AI-DWG would define (from infra)
- Add ONLY services not already defined
- NEVER modify existing service configurations
- Add under a comment: `# AI-DWG additions`
- If ALL services already exist → skip entirely

STEP 5: GENERATE BROWNFIELD-SPECIFIC CONDITIONAL
─────────────────────────────────────────────────
IF `adlc-state.md` shows `Input Mode: Brownfield`:
• Generate `rules/brownfield-patterns.md` (conditional steering file)
• Content: characterization test rules, strangler-fig boundaries, legacy API compatibility, data migration guardrails
• Derived from: AP Integration Architecture (legacy patterns) + Brownfield Strategy ADR

Load: mapping/brownfield-to-steering.md

STEP 6: VALIDATE — Cross-Check
───────────────────────────────
Same as Mode 1 STEP 4, plus:
• Verify no existing files were overwritten
• Verify merge additions are non-contradictory with existing configs
• Verify steering file content doesn't assume folder structure that doesn't exist

STEP 7: OUTPUT — Present Summary
─────────────────────────────────
Present overlay results:

"✅ AI-DWG BROWNFIELD OVERLAY COMPLETE

📦 Governance layered onto: {system_name}
📁 Location: {workspace_root}

📊 Summary:
   • Steering files generated: {n} (of which {m} conditional)
   • Operational documents generated: {n} (of {total} — {skipped} skipped: already exist)
   • Config files merged: {n} (additive entries only)
   • Config files skipped: {n} (already exist, no additions needed)
   • Source folders: NOT MODIFIED (existing code preserved)

📋 Files SKIPPED (already exist):
   • {file}: exists at {path} — preserved as-is
   •...

📋 Config MERGES (additive only):
   •.gitignore: +{n} entries added
   • CODEOWNERS: +{n} ownership rules added
   •...

📋 Brownfield-specific:
   • brownfield-patterns.md: {generated / skipped (not brownfield mode)}

🔗 Next steps:
   1. Review generated steering files — adjust rules that conflict with your existing conventions
   2. Review config merges — remove any AI-DWG additions that don't fit
   3. Run AI-GCE to derive compliance enforcement
   4. Consider: should existing code be gradually brought into compliance? (AI-GCE incremental adoption)

🔀 **Chain Navigation (what's next in the AI-* Family):**
   • Sequential next: **AI-GCE** (`_GCE_`) — Governance & Compliance Engine
   • Alongside: **AI-TGE** (`_TGE_`) — Test Governance (runs parallel with GCE)
   • Or ask AI-FLO: type `_FLO_` for routing guidance based on your project state
   • Dashboard data: type `DAT__ pdlc/dwg` to update the family dashboard

⚠️ **IMPORTANT: Start the next package (AI-GCE) in a NEW session.**
   Each AI-* package loads a full workflow into context;
   a fresh session keeps it fast and focused.

The workspace now has governance steering. Existing code and conventions are untouched."
```

---

## Brownfield Overlay Rules

| Rule | Description |
|------|-------------|
| **Never modify source code** | Mode 3 ONLY touches.kiro/, configs, and docs — never source files |
| **Never overwrite existing docs** | If README.md, CONTRIBUTING.md, etc. exist, respect them |
| **Steering files always generated** | rules/ is AI-DWG's domain — always create (won't conflict with code) |
| **Config merges are additive** | Only ADD entries; never remove or modify existing config content |
| **Respect existing conventions** | If the team has patterns (naming, folder structure), steering should acknowledge not contradict them |
| **Ask before generating structure** | Source folders are NEVER created in Mode 3 (code already exists) |
| **Brownfield conditional is separate** | `brownfield-patterns.md` only generated when ADLC was in brownfield mode |
| **Signal downstream** | After overlay, signal AI-GCE (same as other modes — see `reconciliation/downstream-signaling.md`) |

---

*Mode 3 flow — loaded by `core-generator.md` when Brownfield Overlay is detected.*
