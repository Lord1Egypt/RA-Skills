# Phase 0: Bootstrap

**Goal**: Initialize the migration workspace, detect the language pair, and prepare all five
YAML state files so that Phase 1 can begin immediately.

P0 is the only phase that requires direct human input. All subsequent phases are AI-autonomous
(with human gating only on explicit BLOCKED items).

---

## Entry Criteria

- User has provided: source directory path, target language, and any known constraints
- `migration_workspace/migration-state.yaml` does not yet exist

If `migration-state.yaml` already exists, P0 is already complete — do not re-run it.
Read the existing state and resume from `current_task`.

---

## Steps

### Step 1: Gather required information

Ask the user for exactly these four things (all required before proceeding):

```
1. Source language (e.g., python, rust, go)
2. Source project directory path (relative to workspace root)
3. Target language (e.g., go, rust, c, zig, typescript)
4. Any constraints or priorities (optional — can be empty)
```

Do not proceed until source language, source path, and target language are confirmed.

### Step 2: Resolve language pair module

Construct the language pair key: `<source>-<target>` (lowercase, hyphen-separated).

Check if `references/lang-pairs/<key>.md` exists:
- **YES** → load it; note any pre-mapped gaps and anti-patterns for use in P2 and P3
- **NO** → load `references/lang-pairs/TEMPLATE.md`; inform the user this pair has no
  pre-built module; offer to draft one before continuing (recommended for non-trivial pairs)

### Step 3: Initialize workspace

Create `migration_workspace/` directory at the project root.

Copy all five template files from `templates/` into `migration_workspace/`:

| Template | Destination | Initial Action |
|---|---|---|
| `migration-state.yaml` | `migration_workspace/migration-state.yaml` | Fill `meta` block (source/target lang, dirs, project name, lang_pair_module) |
| `asset-inventory.yaml` | `migration_workspace/asset-inventory.yaml` | Leave empty; ready for P1 |
| `ecosystem-map.yaml` | `migration_workspace/ecosystem-map.yaml` | Leave empty; ready for P2 |
| `ipo-registry.yaml` | `migration_workspace/ipo-registry.yaml` | Leave empty; ready for P3 |
| `retrospective-checklist.yaml` | `migration_workspace/retrospective-checklist.yaml` | Fill `meta.project` and `meta.lang_pair`; leave `entries: []` |

### Step 4: Fill migration-state.yaml meta block

```yaml
meta:
  source_lang: "<source>"          # e.g., python
  target_lang: "<target>"          # e.g., go
  source_dir: "<path>"             # relative path to source project root
  target_dir: "<path>"             # relative path to translated output (may not exist yet)
  lang_pair_module: "<key>"        # e.g., python-go
  project_name: "<name>"           # name of the source project
  source_version: "<commit/tag>"   # git describe or commit hash of source (run: git describe --tags)
  created_at: "<ISO timestamp>"
  last_updated: "<ISO timestamp>"
  operator_notes: "<any human notes>"
```

`source_version` is important for reproducibility — if the source changes mid-migration,
the version pinpoints what was analyzed.

### Step 5: Set initial phase status

```yaml
phases:
  P0_bootstrap:     DONE
  P1_asset_scan:    IN_PROGRESS
  P2_ecosystem_map: TODO
  P3_ipo_analysis:  TODO
  P4_translation:   TODO
  P5_verification:  TODO
```

### Step 6: Trigger PGR-0

Do not immediately proceed to P1. Load `references/phase-gate-review.md` and run **PGR-0**
to verify the bootstrap is complete and consistent. Only after PGR-0 passes with zero findings
should you set `phase_gates.PGR_0.status: PASSED` and proceed to P1.

---

## Exit Criteria

- All five workspace files exist in `migration_workspace/`
- `migration-state.yaml` meta block fully populated (no empty required fields)
- `phases.P0_bootstrap: DONE`
- `phase_gates.PGR_0.status: PASSED`

---

## Common Failure Modes

| Problem | Detection | Fix |
|---|---|---|
| `source_version` left empty | PGR-0 check | Run `git -C <source_dir> describe --tags --always` |
| `target_dir` path same as `source_dir` | PGR-0 check | Ask user to confirm target output directory |
| Lang pair module not loaded | PGR-0 check | Load `references/lang-pairs/<pair>.md` before marking P0 done |
| Missing `retrospective-checklist.yaml` | PGR-0 check | Copy from `templates/retrospective-checklist.yaml` |
