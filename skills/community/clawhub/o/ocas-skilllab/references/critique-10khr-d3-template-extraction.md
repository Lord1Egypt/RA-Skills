# D3 Conciseness: Template Extraction Pattern

When D3 scores 4/5 because SKILL.md exceeds the line-count threshold (heuristic
penalizes >450 lines; manual rubric flags >500), the highest-value extraction
target is any inline template or example that duplicates content already in
`templates/` or `references/`.

## Detection

Run the heuristic scorer and check `line_count` and `code_ratio`:

```python
from critique_10khr_runner import score_skill
r = score_skill(name, path)
print(r['line_count'], r['code_ratio'])
```

If `line_count > 450` or `code_ratio > 20%`, D3 needs a fix.

## Scan Order (most savings, least risk)

1. **Inline JSON/template blocks that duplicate `templates/` files** — Search
   the SKILL.md for `\`\`\`json` blocks. Check if the same structure is already
   documented in `templates/<name>.json`. If yes, delete the inline block and
   replace with: "Use `templates/<name>.json` as the canonical template — required
   fields: [list]." Typical savings: 15-30 lines per template.

2. **Redundant support-file-map descriptions** — The "When to read" column in
   support file maps often repeats the file's own first line. Strip bold markup
   and merge compound descriptions into single phrases. Typical savings: 2-8
   lines.

3. **Repeated sections** — Check for the same warning/rule stated in two
   different sections (e.g., a "Hard rule" section and a "NEVER DO X" section
   saying the same thing). Keep the more prominent one, delete the other.

4. **Support File Map restructure** — When a Support File Map has 20+ entries with verbose "When to read" descriptions (each >1 line), extract the full map to a new `references/<skill>-support-file-map.md` file. Replace the inline map with a compact version: filename + 2-3 word trigger phrase, plus a header line pointing to the full map. Typical savings: 20-40 lines. Preserves information while removing context-load cost.

5. **Verbose how-to blocks** — Multi-step code walkthroughs that belong in
   `references/` rather than the always-loaded SKILL.md. Move to a reference
   file with a one-line pointer.

## Extraction Criteria

An inline block should be extracted when ALL of these are true:
- It appears only once in the SKILL.md (not referenced by multiple sections)
- The same content exists in `templates/` or can be moved to `references/`
- Removing it does not break any "See the example above/below" cross-reference
- It is longer than 10 lines

## Verification

After extraction:
1. Re-run the scorer — confirm `line_count` dropped below threshold
2. `grep -n '^## '` to verify no sections were eaten by patch drift
3. Confirm the canonical template still exists in `templates/`
4. Read the SKILL.md top-to-bottom to check flow is intact

## Real Example (2026-06-28)

`ocas-dispatch` SKILL.md was 460 lines. The "Dispatch Wave Journal Format"
section contained a 25-line inline JSON template that duplicated
`templates/dispatch-wave-journal.json`. Fix: replaced the inline block with a
3-line pointer to the template file + required field list. Also condensed the
Support File Map by removing bold redundancy. Result: 436 lines, D3 4→5/5.