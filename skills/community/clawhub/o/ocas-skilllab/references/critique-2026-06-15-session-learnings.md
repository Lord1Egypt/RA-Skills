# Critique Session Learnings — 2026-06-15

## Session Summary

Critiqued and improved `util-wiki` (Wikipedia Author Assistant) using the skilllab critique procedure. Score went from 36/50 (B) to projected 41/50 (A) after fixes.

## Key Anti-Pattern Discovered: Failed Attempts → Absolute Prohibitions

The `util-wiki` skill contained multiple "Do NOT" rules that originated from **incomplete/failed attempts**, not confirmed permanent limitations:

| Original Prohibition | Origin | Reality |
|---------------------|--------|---------|
| "Do NOT use Wikipedia API (curl/Python) from VPS" | Prior session's proxy block | May change; verify before skipping browser |
| "Do NOT use `browser_type` to enter wiki markup" | Single large-text timeout | Works for small targeted edits |
| "Do NOT chain multiple long JS expressions" | Browser 502 in one session | Break into chunks; don't avoid entirely |
| "Do NOT dispatch `input` event after setting textarea `.value`" | One failed textarea approach | Fetch API is more reliable; textarea works without event |
| "Browser session is dead — navigate back" | Fatalistic framing of 502 | May be transient; try again first |

**Lesson:** Skills must distinguish between:
- **Confirmed hard constraints** (e.g., "Wikipedia edit filter blocks WP:CIRCULAR citations")
- **Transient failures from incomplete attempts** (e.g., "browser 502ed once")
- **Approach-specific limitations** (e.g., "large text in single browser_type call times out")

Encoding the latter two as absolute "Do NOT" rules creates self-imposed constraints that block legitimate work when conditions change.

## Critique Workflow Validation

The critique procedure (Phases 1-6) worked well:
1. **Read fully** → caught the absolute prohibitions in Pitfalls section
2. **Score against rubric** → D3 (Conciseness) and D8 (Progressive Disclosure) flagged
3. **Categorize issues** → Major: duplicate sections, missing support file map, inline JS
4. **Plan fixes** → Move JS to references, merge duplicates, add support file map
5. **Execute** → 5 targeted patches + 1 reference file
6. **Verify** → Re-scored, confirmed improvements

**Signal for future sessions:** When running critique on any skill, always check the "Pitfalls" / "What NOT to Do" sections for absolute prohibitions that may encode failed attempts rather than real constraints.

## Profile vs Monorepo Sync Gap

The profile copy (`$HERMES_HOME/../indigo/skills/util-wiki/`) had fixes applied but the monorepo (`~/utilities/wiki/`) did not. Both must be kept in sync. The `source:` field in frontmatter points to the monorepo, so that's the canonical version.

**Action:** After any skill edit, verify `diff` between profile and monorepo copies before considering the session complete.

## Reference File Created During Session

- `references/editing-wikipedia.md` — All JS code examples extracted from SKILL.md
- `references/critique-2026-06-15.md` — Improvement plan and before/after scores
- `wikipedia-templates/` — Existing template references

## Recommended Skilllab Updates

1. Add pitfall: "Beware of absolute prohibitions encoding failed attempts"
2. Add critique phase check: "Scan Pitfalls/What NOT to Do for failed-attempt encoding"
3. Add sync reminder: "Verify profile ↔ monorepo parity after skill edits"