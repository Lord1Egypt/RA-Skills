# History

`~/.openclaw/workspace/jd_history.md` — a single append-only log. Create it on the first
evaluation.

**Every evaluation writes an entry, including OUT.** Rejections are the most
useful rows in the file: they are what `analyze` reads to tell the user which
pattern keeps landing in their inbox. An evaluation that produced no entry did
not finish — say so rather than letting it pass.

## Language

Structural labels are **always English** (`Evaluated`, `Action`, `Desirability`,
`Candidacy`, `Scores`, `Summary`, `Triggered`, `Outcome`, `Criteria version`) so
the file stays greppable when the user switches languages.

Free text — org name, title, summary, red-line citations, JD quotes — is stored
in the language it was written in and **never retroactively translated**. Listing
and comparison output renders labels in the current language and shows stored
text verbatim.

## ID

`JD-YYYYMMDD-NNN` — today's date, then a per-day sequence starting at `001`,
found by grepping existing entries with the same date prefix.

## Entry — standard detail

```markdown
## [JD-20260725-001] <org> — <title>

**Evaluated**: 2026-07-25
**Criteria version**: 4
**Action**: ✅ Apply
**Desirability**: Good (3.6/5)
**Candidacy**: Plausible (70%)

### Scores
- Role fit:  ★★★★☆
- Domain:    ★★★★★
- Org:       — (info insufficient)
- Vibe:      ★★★☆☆
- Comp:      ★★★★☆

### Candidacy
Meets 3.5/5 stated must-haves. Gaps: team management, Kubernetes (learning).

### Summary
<one line>

### Triggered
<red lines or failed gates with location, or "none">

### Outcome
<blank — the user fills this in later: applied / rejected / interviewing / offer / passed>
```

`minimal` — the heading, `Evaluated`, `Action`, `Summary`.

`full` — adds a `### Raw JD` block. **Warn once before the first `full` write:**
"This stores the complete posting, which may include recruiter contact details or
comp not published elsewhere. Continue? (y/n)". Do not re-ask on later writes.

## OUT entries

Shorter body: no `Scores` or `Candidacy` sections — scoring stopped at the gate.
Keep `Triggered` and `Summary`, and record the "Matched anyway" points under
`Summary` so the signal is not lost.

## The Outcome field

Left blank by the skill. If the user mentions an outcome in conversation
("I applied to the Figma one", "they rejected me"), offer to fill it in — never
write it silently. Outcomes are what let `analyze` compare *predicted* fit with
*actual* results; a file with none is still useful, just blind to that.

## `/jd-triage history`

Last 10 entries, one line each, newest last:

```
JD-20260712-001  Basecamp     Senior PM        ✅ Apply        Good/Plausible    applied
JD-20260718-002  Northvolt    Product Lead     🗄️ Backup       Weak/Likely       —
JD-20260725-001  Figma        PM, Dev Tools    🔥 Apply now    Strong/Plausible  —
```

Support a filter argument: `/jd-triage history apply` shows only Apply-tier
actions; `/jd-triage history out` only OUT.

## `/jd-triage compare <id1> [<id2>]`

Two IDs, or one ID against the most recent, or "the last two".

```
                  JD-20260718-002        JD-20260725-001
                  Northvolt              Figma
                  Product Lead           PM, Dev Tools
                  ──────────────         ──────────────
Action            🗄️ Backup              🔥 Apply now
Desirability      Weak (2.8)             Strong (4.2)
Candidacy         Likely (85%)           Plausible (60%)
Criteria version  4                      4
Role fit          ★★★☆☆                  ★★★★★
Domain            ★★☆☆☆                  ★★★★★
Org               ★★★★☆                  — (insufficient)
Vibe              ★★★☆☆                  ★★★★☆
Comp              ★★★★☆                  ★★★★☆

<one line: which is stronger, and the trade the user is actually making>
```

The closing line must name the trade-off rather than declare a winner — these two
differ on *both* dimensions in opposite directions, which is the entire point of
keeping them apart.

**Criteria drift warning.** If the two entries used different `Criteria version`
values, prepend:

```
⚠️ Your criteria changed between these evaluations (v4 → v6).
   Axes touched by the change are not directly comparable.
```

Name which axes moved if the current file makes that determinable.

## Growth

The file grows without bound by design — `analyze` gets better with more rows.
If it passes roughly 100 entries and the user asks, offer to archive entries
older than a year to `jd_history_<year>.md` rather than deleting them. Never
delete history unprompted.
