# Phase 6: Migration Completeness Audit (Gap Report)

**This phase is NOT sequential — it can be invoked at ANY point during migration.**

Invoke with: "生成迁移完整性报告" / "gap report" / "还差什么" / "show migration status"

**Goal**: Produce a structured, multi-dimensional gap report that answers:
1. Which source files have no corresponding target file?
2. Which functions are marked DONE but have no `target_lines`?
3. Which source directories have no equivalent in the target?
4. Which non-code assets (fixtures, docs, configs) are missing from target?
5. What was intentionally skipped vs accidentally missed?
6. What is the true 1:1 replication percentage?

Output: `migration_workspace/gap-report.md` (human-readable) 
        + `migration_workspace/gap-report.yaml` (machine-readable)

---

## Execution Protocol

### Step 1: Run the Gap Report Script

In full_mode (bash/PowerShell available):
```bash
python migration_workspace/../.agents/skills/lang-migration/scripts/gap_report.py \
  --workspace migration_workspace/ \
  --source <source_dir> \
  --target <target_dir>
```

In editor_mode: manually execute the five analysis dimensions below.

### Step 2: Output the Report

The report must appear in the AI's response AND be written to `gap-report.md`.
Do not silently write to file only — the human must see the summary.

---

## Five Analysis Dimensions

### Dimension 1: File Coverage (Source → Target)

For every entry in `asset-inventory.yaml`:

| Strategy | Expected | Check |
|---|---|---|
| `translate` | `target_path` file exists on disk | File present AND non-empty? |
| `adapt` | `target_path` file exists on disk | File present AND non-empty? |
| `direct_use` | file copied to target | Exists in target tree? |
| `reference_only` | no target file (correct) | Documented skip — OK |
| `preserve` | file in target root | Exists? |
| `generated` | auto-created by toolchain | Skip check |

Report format:
```
DIMENSION 1 — File Coverage:
  translate_total:       <N>
  translate_present:     <N>   ← files that exist on disk
  translate_missing:     <N>   ← files that should exist but don't
  adapt_total:           <N>
  adapt_present:         <N>
  adapt_missing:         <N>
  direct_use_total:      <N>
  direct_use_present:    <N>
  direct_use_missing:    <N>
  
  MISSING FILES (translate/adapt):
    - source: <path>  target_expected: <path>  reason: not_created
    ...
  
  MISSING DIRECT_USE:
    - source: <path>  target_expected: <path>
    ...
```

### Dimension 2: Function Translation Coverage

Scan `ipo-registry.yaml`:

```
DIMENSION 2 — Function Coverage:
  functions_total:              <N>
  translation_status_DONE:      <N>
  translation_status_TODO:      <N>    ← not yet started
  translation_status_BLOCKED:   <N>    ← blocked; needs resolution
  DONE_with_target_lines:       <N>    ← genuinely complete
  DONE_without_target_lines:    <N>    ← ⚠️ suspicious — DONE claimed but no evidence

  SUSPICIOUS ENTRIES (DONE but no target_lines):
    - id: <fn_id>  target_impl_file: <file>
    ...

  TRUE_COMPLETION_RATE: <DONE_with_target_lines> / <functions_total> = <X>%
```

### Dimension 3: Directory Structure Gap

Walk source directory tree. For each source directory, check if a corresponding
directory exists in the target tree (either same name or mapped path from asset-inventory).

```
DIMENSION 3 — Directory Coverage:
  source_dirs_total:         <N>
  source_dirs_with_target:   <N>
  source_dirs_without_target:<N>
  
  UNMAPPED SOURCE DIRECTORIES:
    - genericagent/plugins/         → no equivalent in go-GenericAgent/
    - genericagent/memory/L4_raw_sessions/ → no equivalent (reference_only — OK?)
    ...

  UNEXPECTED TARGET DIRECTORIES (not derived from source):
    - go-GenericAgent/internal/bbs/bbs_files/ → runtime-generated temp dir? OK to ignore?
    ...
```

### Dimension 4: Non-Code Asset Coverage

Check that every `direct_use` file (test fixtures, binary assets, static data)
actually exists in the target project tree.

Also check: every `reference_only` file marked `p3_required: true` — was it
actually referenced during P3 IPO analysis? (Check for mentions in translation_notes
or ipo entry process.reference fields.)

```
DIMENSION 4 — Non-Code Assets:
  test_fixtures_total:        <N>
  test_fixtures_in_target:    <N>
  test_fixtures_missing:      <N>
  
  p3_required_files_total:    <N>
  p3_required_referenced:     <N>    ← appears in any IPO entry's process.reference
  p3_required_unreferenced:   <N>    ← ⚠️ marked p3_required but never cited

  MISSING TEST FIXTURES:
    - <source_path> → expected at <target_path>
    ...
  
  UNREFERENCED P3-REQUIRED DOCS:
    - <doc_path> — was this read during IPO analysis?
    ...
```

### Dimension 5: Intentional Skips vs Accidental Gaps

Cross-reference:
- Files in `decisions_log` with "skipped" rationale → intentional
- Files with `status: DONE` in asset-inventory but no target file → accidental gap
- Files explicitly noted in `operator_notes` or migration-state comments as skipped

```
DIMENSION 5 — Skip Classification:
  intentional_skips_documented: <N>    ← in decisions_log with rationale
  accidental_gaps:              <N>    ← DONE in inventory but target missing
  skipped_platform_specific:    <N>    ← e.g., Streamlit, PyQt5 (documented)
  
  INTENTIONAL SKIPS (documented):
    - <file>: <rationale from decisions_log>
    ...
  
  ACCIDENTAL GAPS (needs attention):
    - <file>: status=DONE in inventory but target_path not found on disk
    ...
  
  PLATFORM-SPECIFIC SKIPS (Python-only, no Go equivalent):
    - <file>: <framework> — <brief reason>
    ...
```

---

## Summary Report Format

The final output that appears in the AI response:

```
═══════════════════════════════════════════════════════════════
MIGRATION COMPLETENESS AUDIT — <project_name>
Generated: <timestamp>
Source: <source_dir> (<N> files)   Target: <target_dir>
═══════════════════════════════════════════════════════════════

FILE COVERAGE
  translate files:    <done>/<total> (<X>%) — <N missing> missing
  adapt files:        <done>/<total> (<X>%) — <N missing> missing  
  direct_use files:   <done>/<total> (<X>%) — <N missing> missing

FUNCTION COVERAGE
  genuinely DONE:     <N>/<total> (<X>%)
  ⚠️  DONE no evidence: <N>  ← requires re-verification
  TODO/BLOCKED:       <N>

DIRECTORY COVERAGE
  source dirs mapped: <N>/<total> (<X>%)
  unmapped source:    <N dirs> (see detail)

NON-CODE ASSETS
  fixtures in target: <N>/<total>
  p3 docs referenced: <N>/<total>

SKIP CLASSIFICATION
  intentional skips:  <N> (documented)
  accidental gaps:    <N> (⚠️ needs attention)

───────────────────────────────────────────────────────────────
TRUE 1:1 COMPLETION: <X>%
  (= files_complete + functions_with_evidence + assets_complete) / total_expected
───────────────────────────────────────────────────────────────

PRIORITY ACTION ITEMS:
  🔴 CRITICAL (blocks correctness):
    1. <item>
  🟡 IMPORTANT (completeness gap):
    2. <item>
  🟢 MINOR (documentation/cleanup):
    3. <item>
```

---

## Invoking at Session Start

If the human's first message in a session is a status question ("还差什么", "进度怎样",
"gap report"), run the Gap Report BEFORE resuming any other task.

Always show the Summary Report in the response. Write full details to `gap-report.md`.
