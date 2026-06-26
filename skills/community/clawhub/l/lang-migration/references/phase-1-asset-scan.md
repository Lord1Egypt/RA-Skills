# Phase 1: Asset Scan

**Goal**: Produce a complete `asset-inventory.yaml` where every file in the source project
has an entry with a migration strategy. Zero files omitted.

---

## Entry Criteria

- `migration-state.yaml` exists
- `phases.P0_bootstrap: DONE`
- `phases.P1_asset_scan: IN_PROGRESS`

## Exit Criteria

- Every file in the source project has an entry in `asset-inventory.yaml`
- Every entry has `status: DONE` (or `BLOCKED` — which requires human resolution first)
- `migration-state.yaml` stats block is updated
- `phases.P1_asset_scan: DONE`, `phases.P2_ecosystem_map: IN_PROGRESS`

---

## Execution Steps

### Step 1: Generate File List

**In full_mode** (Claude Code / OpenCode with bash):
```bash
cd <source_dir>
find . -type f | sort > /tmp/source_file_list.txt
wc -l /tmp/source_file_list.txt
```

Also run the scan script if available:
```bash
python migration_workspace/../skills/lang-migration/scripts/scan_assets.py \
  --source <source_dir> \
  --output migration_workspace/asset-inventory.yaml
```

**In editor_mode** (Cursor / Copilot):
- Read the directory tree by exploring the file system
- Manually enumerate all files
- Do not guess — if you cannot see a directory, say so

### Step 2: Classify Each File

For each file, determine:
1. **type** — use the type table in `references/schemas.md`
2. **purpose** — read the file; write a one-line description of what it does
3. **migration_strategy** — apply the decision tree below
4. **p3_required** — true if this file contains algorithm descriptions, mathematical derivations, or explanations not present in the code

### Strategy Decision Tree

```
Is this a source code file (.py, .go, .c, etc.)?
  YES → translate

Is this a test code file (test_*, *_test.*, spec.*, etc.)?
  YES → translate (tests are first-class citizens; migrate them too)

Is this a test fixture / data file used by tests?
  YES → direct_use (copy as-is; test data must remain identical)

Is this a dependency manifest (requirements.txt, go.mod, Cargo.toml, package.json)?
  YES → adapt (recreate for target ecosystem using ecosystem-map)

Is this a build config (Makefile, CMakeLists, build.gradle, pyproject.toml)?
  YES → adapt (rebuild for target toolchain)

Is this a CI config (.github/workflows/, .gitlab-ci.yml, Jenkinsfile)?
  YES → adapt (update build commands, keep pipeline structure)

Is this a Dockerfile or docker-compose?
  YES → adapt (update base image and build commands)

Is this documentation or algorithm notes (README, docs/, *.md, *.rst, *.tex)?
  YES → preserve_and_reference; set p3_required: true if it contains algorithm detail
  
Is this a binary asset (image, .npy, .pb, .pkl, compiled output)?
  YES → direct_use if it's input data; generated if it's build output

Is this a configuration file (.env, .yaml, .json config, .ini)?
  YES → direct_use (format-compatible) or adapt (if syntax must change)

Cannot determine purpose?
  → preserve; write what you observe in notes; DO NOT skip
```

### Step 3: Record Dependencies

For each `translate` or `adapt` file, read the imports/includes and list them in `depends_on_ecosystem`. These feed directly into P2.

```yaml
# Example
- path: "src/core/entropy.py"
  depends_on_ecosystem:
    - numpy
    - scipy.stats
    - collections
    - typing
```

### Step 4: Set p3_required

Mark `p3_required: true` for:
- Files with algorithm descriptions (docs, comments files)
- Files with mathematical derivations
- Any file whose content is referenced in source code comments
- Project wiki exports, research notes, design documents

### Step 5: Update State

```yaml
# In migration-state.yaml
stats:
  assets_total: <count>
  assets_done: <count>   # all DONE (not counting BLOCKED)
  assets_blocked: <count>
phases:
  P1_asset_scan: DONE
  P2_ecosystem_map: IN_PROGRESS
```

---

## Blocking Rules

Block (do not skip) when:
- A file exists but cannot be read or accessed
- A file type is completely unrecognizable and the name gives no clues
- Two files appear to conflict in purpose (e.g., two different configs for the same tool)

Present the block using the standard blocking protocol from `SKILL.md`.

---

## Quality Checks Before Exiting P1

- [ ] File count in `asset-inventory.yaml` matches `find . -type f | wc -l`
- [ ] No file has `migration_strategy: ""` (empty)
- [ ] All test fixture files are `direct_use`
- [ ] All documentation files are `reference_only` or `preserve`
- [ ] `depends_on_ecosystem` is populated for all `translate` files

---

## Phase Exit: Trigger PGR-1

When you believe P1 is complete, do NOT mark it DONE yet.

Load `references/phase-gate-review.md` and run PGR-1 using the audit criteria defined there.
Only set `phases.P1_asset_scan: DONE` after PGR-1 passes with zero findings.

The PGR-1 loop will:
1. Verify every source file is in `asset-inventory.yaml` (including a fresh re-scan)
2. Verify every entry has a non-placeholder `purpose`
3. Verify every entry has a confirmed `migration_strategy`
4. Verify every entry has a valid `status`
5. Verify `by_strategy` counts match actual entry counts
6. Fix any findings autonomously and re-audit from scratch until zero findings remain

`phases.P1_asset_scan: DONE` is set by PGR-1 as its final action — never set it directly.
