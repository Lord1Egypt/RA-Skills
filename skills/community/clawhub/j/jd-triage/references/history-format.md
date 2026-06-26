# History format

## File location

`~/.openclaw/workspace/jd_history.md` — single append-only file. Create on first evaluation if missing.

## Language policy

Same rule as `jd_criteria.md`:

- **Structural labels are always English** (`Evaluated`, `Verdict`, `Scores`, `Summary`, `Triggered red lines`, `Action taken`, `Criteria version`). This keeps the file grep-friendly and stable across user-language switches.
- **Free-text content follows the user's language at write time** (company name, JD title, summary one-liner, red-line citations, action notes).
- **Verdict tier names are English in storage** (`Strong Apply` / `Apply` / `Caution` / `Skip` / `OUT`), translated only when shown to the user.
- **Never retroactively translate.** If a Chinese user wrote a summary 6 months ago and now interacts in English, the entry's summary stays Chinese. List/comparison output renders structural labels in the current user's language but shows stored content as-is.

## Entry format (standard detail)

Append a new entry to the bottom of the file after each evaluation:

```markdown
## [JD-YYYYMMDD-XXX] <company> — <title>

**Evaluated**: ISO-8601 date
**Criteria version**: <integer from criteria file at time of eval>
**Verdict**: <emoji + tier>

### Scores
- Title fit:    ★★★★☆
- Industry:     ★★★★★
- Company type: ★★★☆☆
- Company size: ★★★★☆
- Vibe:         ★★☆☆☆
- Salary:       ★★★★☆

### Summary
<one-line judgment>

### Triggered red lines
<list, or "none">

### Action taken
<empty by default — user can edit manually: "applied", "skipped", "interviewing", etc.>

---
```

For `minimal` detail, drop everything except the `## [JD-...]` line, `Evaluated`, `Verdict`, and `Summary`.

For `full` detail, append a `### Raw JD` block with the user-pasted text. **Warn the user** the first time `full` is used: "This will store the full JD text including any recruiter contact info or private comp data. Continue? (y/n)".

## ID generation

Format: `JD-YYYYMMDD-XXX`
- `YYYYMMDD` — today's date
- `XXX` — sequential number for that day (`001`, `002`, ...) found by grepping existing entries with the same date prefix

If today has no entries yet, start at `001`.

## OUT entries

Hard-gate failures still get logged with full ID + verdict (`❌ OUT`) but with a shorter body — no scores section, just `Triggered red lines` and `Summary`. Useful for tracking which patterns keep showing up in your inbox.

## History commands

### `/jd-triage history` (or "show my JD history" / "看下评估过的 JD")
Show the last 10 entries as a one-line-per-JD table:
```
JD-20260520-001  Anthropic        Agent PM            ✅ Strong Apply
JD-20260605-003  Moonshot         AI Product Manager  🎯 Apply
JD-20260612-001  StealthCo        AI PM (no JD body)  ❌ OUT (red line)
...
```

### `/jd-triage compare <id1> [<id2>]` (or "compare last two" / "和上次的对比")
Side-by-side comparison table. If only one ID given, compare with the most recent entry. If user says "last two" or similar, use the two most recent entries.

```
                JD-20260520-001       JD-20260605-003
                Anthropic Agent PM    Moonshot AI Product
                ─────────────────     ─────────────────
Verdict         ✅ Strong Apply       🎯 Apply
Criteria ver    3                     3                 (same)
Title fit       ★★★★★                 ★★★★☆
Industry        ★★★★★                 ★★★★★
Company type    ★★★★★ (foreign)       ★★★★☆ (model)
Vibe            ★★★★★                 ★★★★☆
Salary          ★★★★☆                 ★★★☆☆

Recommendation: <one-line which is stronger and why>
```

### Criteria version mismatch warning

When comparing two entries with different `Criteria version` values, prepend the comparison output with:

```
⚠️ Criteria has changed between these evaluations.
   JD-20260520-001 used criteria v3
   JD-20260605-003 used criteria v5
   Some axes may not be directly comparable.
```

## Interaction with criteria updates

- Criteria file `criteria_version` increments on every S1 / S2 / S5 flow that writes the file.
- S4 "no, nothing changed" answers do **not** bump `criteria_version` — only `last_updated`.
- History entries store the `criteria_version` at evaluation time; never rewritten retroactively.

## No auto-cleanup (v0.1)

History grows indefinitely in v0.1. Manual cleanup: user opens the file and deletes entries themselves. A future version may add `/jd-triage history clean` once the file gets long.
