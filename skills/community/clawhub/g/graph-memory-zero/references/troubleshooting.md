# Troubleshooting matrix

## 1) Command failed during patch flow

### Symptoms
- `Error: Command failed` from PowerShell or helper script

### Checks
1. Validate path first with `Test-Path`.
2. Confirm script exists and execution policy allows run.
3. Retry with minimal command (avoid long chained commands).

### Recovery
- If path issue: fix path, then rerun.
- If permission issue: use proper shell/permissions.

---

## 2) Schema lookup path not found

### Symptoms
- `gateway.config.schema.lookup` returns missing/invalid path

### Checks
1. Re-check plugin id (`graph-memory`) spelling.
2. Query parent path first:
   - `plugins.entries`
   - `plugins.entries.graph-memory`
3. Confirm plugin is installed/enabled.

### Recovery
- Use discovered exact path; do not guess field names.

---

## 3) Patch applied but behavior unchanged

### Symptoms
- Config appears updated, recall behavior unchanged

### Checks
1. Verify restart completed.
2. Re-read live config (`gateway.config.get`) to ensure persisted values.
3. Confirm threshold/minScore conflict isn’t overriding expected value.
4. Confirm `memoryType` filter is not too restrictive.

### Recovery
- Reapply minimal patch with fresh `baseHash`.
- Re-run verification playbook.

---

## 4) Recall too noisy (false positives up)

### Quick fix order
1. Raise threshold (e.g., +0.04)
2. Keep `infer=true` (usually useful)
3. Narrow `memoryType` (`all -> fact`)
4. Tighten lexicon keywords

---

## 5) Recall too strict (misses relevant memory)

### Quick fix order
1. Lower threshold (e.g., -0.04)
2. Keep `memoryType=all`
3. Expand lexicon keywords (especially bilingual terms)
4. Re-run query set to confirm improvement

---

## 6) Version mismatch warning

### Symptoms
- Extension folder version != runtime installed version

### Handling
- Mark as metadata mismatch item.
- Continue config-level optimization if runtime behavior is healthy.
- Include mismatch in release/ops report.

---

## 7) Rollback trigger conditions

Rollback immediately when one of the following occurs:
- Query relevance drops materially after patch
- Off-topic hits spike significantly
- Observability/debug fields disappear
- Critical preference queries fail consistently

Rollback method:
- restore previous `recallPolicy` snapshot via minimal patch
- verify with same query set
