# YAML Frontmatter Parsing Pitfalls

## The `body_start` Offset Bug (discovered 2026-05-09)

**Symptom:** YAML validator reports `STRAY_FM_CLOSE: body contains '---'` on a clean file, or body content is shifted/includes the closing `---` delimiter.

**Root cause:** Using `.lstrip('\n')` on `raw[3:]` changes the offset, then `close_idx = rest.find('\n---')` returns an index relative to the stripped string, but `body_start = close_idx + 5` tries to use it on the original `raw` string. The lstrip shifts everything.

**Bad pattern (DO NOT USE):**
```python
rest = raw[3:].lstrip('\n')          # offset shifted by stripping
end_idx = rest.find('\n---')          # index relative to stripped string
yaml_block = rest[:end_idx].strip()   # OK for parsing YAML
body_start = end_idx + 5              # WRONG: end_idx is in stripped space, not raw
body_raw = raw[body_start:]           # WRONG: starts too early or in wrong place
```

**Correct pattern:**
```python
close_idx = raw.find('\n---', 3)      # always search in raw, skip first 3 chars (---)
if close_idx == -1:
    return errors
yaml_block = raw[3:close_idx].strip() # YAML content
body_raw = raw[close_idx + 5:]        # +5 skips \n---\n, correct because close_idx is in raw
```

**Key insight:** Always search for the closing `---` delimiter in the original `raw` string, not in a `lstrip()`-ed copy. The `\n---` sequence is deterministic (it's `\n` + `---` + `\n`), so `close_idx + 5` is correct when operating on the original string.

## Common `tag:` vs `tags:` Typo

Several notes in the vault use `tag:` (singular, missing 's') instead of `tags:`. The yaml-validator now detects this with `TAG_VS_TAGS` error.

**Detection logic:**
```python
if 'tag' in fields and 'tags' not in fields:
    errors.append("TAG_VS_TAGS: frontmatter has 'tag:' — did you mean 'tags:'?")
```

## Agent Memory Frontmatter Rules

Agent memory fragments (`agent memory/` directory) have special rules:
- No `type:` field (use `tags:` instead)
- No `[[links]]` in frontmatter
- No `related_fragments` field (use `project:` grouping)
- Must have `summary:` field with `importance:` rating

These are enforced by `yaml-validator.py` and should not be overridden.
