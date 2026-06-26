# Quality Self-Check and Error Detection

After each phase, perform checks before proceeding. Fix errors immediately.

## Phase 1 (SCAN) Checks

| Check | How | Common Error | Fix |
|-------|-----|-------------|-----|
| macOS resource forks excluded | No `._*` in scan_result.json | Double-counted files | Add `._` filter |
| Priority classification accuracy | Sample 10 P7 files | System-named Excel files misclassified | Promote to P2 manually |
| Extension coverage | Check by_extension stats | .xls missed (case) | `.lower()` on comparison |
| File count sanity | Compare against `find . -type f` | Path encoding on Windows CJK | Use `pathlib.Path` |

## Phase 2 (EXTRACT) Checks

| Check | How | Common Error | Fix |
|-------|-----|-------------|-----|
| Column role accuracy | Print 5 sample tables' column_roles | "字段描述" → field_name instead of field_name_cn | Longest-match-wins strategy |
| Table name extraction | Count `table_name: null` | Name in merged first row | Check merged rows |
| Schema detection rate | schema_tables / total_tables | Below 30% | Tighten `is_schema_header()` |
| Large file handling | Check `truncated: true` flags | Data lost | Re-extract with higher limits |
| .doc conversion | Check for FAILED entries | COM failure | Skip, try LibreOffice fallback |

### Column Role Detection Pitfalls

```
"字段描述" matches both "字段" (field_name) and "描述" (description)
→ Use longest-keyword-match-wins

"数据类型" matches "数据" and "类型"
→ Add "数据类型" as specific keyword for field_type

"是否主键" matches "是否" (nullable) and "主键"
→ Add compound keyword to primary_key
```

Always spot-check 5 random tables after extraction.

## Phase 3 (MERGE) Checks

| Check | How | Common Error | Fix |
|-------|-----|-------------|-----|
| Entity count plausibility | Compare against schema tables | Too few = aggressive exclusion | Review EXCLUDE decisions |
| Cross-system duplicates | Search similar Chinese names | Same concept counted separately | Create merge review_flag |
| Relationship completeness | Each entity has ≥1 relationship | Orphan entities | Check for missed FKs |
| Property deduplication | Same property twice in one entity | Multi-source extraction | Keep stronger evidence_grade |
| JSON validity | `python -c "import json; json.load(...)"` | Syntax errors | Validate before claiming done |

## Error Correction Workflow

```
1. IDENTIFY: What exactly is wrong? (specific example)
2. DIAGNOSE: Why? (root cause in script or analysis)
3. FIX: Modify script/approach
4. VERIFY: Re-run and confirm
5. PROPAGATE: Same error type elsewhere?
6. DOCUMENT: Note in review.md "Data Quality Notes"
```

Do NOT silently work around errors or wait until the end.

## Common Error Patterns

| Error | Root Cause | Fix |
|-------|-----------|-----|
| Column role mismatch | Ambiguous keywords | Longest-match + compound keywords |
| macOS resource forks | `._*` not filtered | Add prefix filter |
| Excel data dict misclassified | Filename is system name | Promote P7 Excel manually |
| Console encoding crash (Win) | GBK codec | `sys.stdout = TextIOWrapper(buffer, encoding='utf-8')` |
| .doc conversion timeout | Large/corrupted file | Set timeout, skip, log |
| Merged cell table names | Title in merged row | Check identical-cell rows |
