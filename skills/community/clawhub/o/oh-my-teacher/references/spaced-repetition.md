# Spaced Repetition

Use this file for `/review-due`, SRS file handling, due-date calculation, and automatic SRS updates after `/quiz`, `/mock`, `/oral`, `/grade`, `/fix`, `/socratic`, or `/feynman`. For host fallbacks, see `references/environment-adaptation.md`.

For explicit user-requested daily/weekly reminders or knowledge digests, use
`references/opt-in-reminders.md`; do not turn SRS due items into proactive
messages unless the user opted in.

In agent shells, prefer `scripts/srs.py` for deterministic `init`, `update`, `due`, `list`, `rename`, `remove`, and `set-active` operations instead of hand-editing Markdown tables.

The workspace root defaults to `$OMT_WORKSPACE`, then the current directory. In agent shells where the cwd may be an unrelated repository, set `OMT_WORKSPACE` (or pass `--workspace`) to a stable path so learning state is not scattered across project folders.

In ima-native environments, prefer the SRS table in the course homepage or a dedicated ima-note. Use `search source=note` to find it, `fetch type=note_id` to read the full note when needed, and `use_skill name=ima-note` to update it. Use `memory_recall` only as a fallback or to find the active course context.

## Slug Consistency

The SRS slug and the snapshot slug **must** be the same for a given course. `scripts/snapshot.py` exposes a `slugify()` helper that derives slugs from course names (Unicode-aware, see `course-profiles.md` → Slug Convention). `scripts/srs.py` does **not** derive slugs itself — it accepts them via `--slug` or `--active`. When initializing a new SRS file, derive the slug with `snapshot.py slug "Course Name"` first, then pass it to `srs.py`:

```bash
# Bash
SLUG=$(python scripts/snapshot.py slug "Course Name")
python scripts/snapshot.py set-active --course "Course Name"
python scripts/srs.py init --slug "$SLUG" --active
python scripts/srs.py set-active "$SLUG" --require-exists
```

```powershell
# PowerShell
$SLUG = python scripts/snapshot.py slug "Course Name"
python scripts/snapshot.py set-active --course "Course Name"
python scripts/srs.py init --slug "$SLUG" --active
python scripts/srs.py set-active "$SLUG" --require-exists
```

If the slugs diverge, the active SRS and active snapshot may point to different courses, causing incorrect review scheduling.

## Topic Naming and Deduplication

The **Topic** field is the primary key. Inconsistent names (`极限` today, `limits-epsilon-delta` tomorrow) silently fragment one concept into several rows and wreck scheduling. To prevent this:

- Reuse the exact topic label from the Current Course Snapshot's Weak points / Completed lists, or from prior SRS rows. Do not paraphrase a topic that already exists.
- `scripts/srs.py update` normalizes surrounding whitespace and warns on stderr when a new topic is fuzzy-similar to an existing one (`'limits-epsilon-delt' is similar to existing topic 'limits-epsilon-delta'`). Heed the warning: reuse the existing name, or merge with `srs.py rename "old" "new"`.
- `srs.py rename` merges into the target row when it already exists (keeps the stronger streak, the sooner next-review, the lower ease, and the summed lapses). `srs.py remove` deletes a topic that is no longer relevant.

## SRS State Files

In agent shell:

- Single-course mode: `.oh-my-teacher/srs-state.md`.
- Multi-course mode: `.oh-my-teacher/srs/<course-slug>.md` plus `.oh-my-teacher/srs/_active`.

Use this table shape:

```markdown
| Topic | Last Review | Score | Streak | Next Review | Difficulty | Ease | Lapses |
|-------|-------------|-------|--------|-------------|------------|------|--------|
| limits-epsilon-delta | 2026-06-01 | 4 | 2 | 2026-06-04 | medium (中等) | 2.50 | 0 |
| rolle-theorem | 2026-06-05 | 2 | 0 | 2026-06-06 | hard (困难) | 2.10 | 3 |
```

Older 5-column (no Difficulty) and 6-column tables still parse — missing columns backfill to `medium`, ease `2.50`, lapses `0` — but always write the full 8-column shape going forward.

Fields:

- **Topic**: short label, consistent across sessions (see Topic Naming above).
- **Last Review**: ISO date of last practice on this topic.
- **Score**: 1-5.
- **Streak**: consecutive reviews with score >= 3; resets to 0 on score <= 2.
- **Next Review**: ISO date for next review.
- **Difficulty**: easy / medium / hard. A coarse, model/user-owned knob that scales the base interval.
- **Ease**: per-topic SM-2-style factor in `[1.3, 2.7]`, default `2.50`. Drifts automatically with recall quality and finely scales the interval. Owned by the script, not the model.
- **Lapses**: total count of score <= 2 reviews. Drives leech detection.

## Date Source

All scheduling depends on today's date.

- Agent shell: obtain the current date from the environment before computing intervals or filtering due topics. Use the available platform command, not a hardcoded shell.
- RAG notebook, notes app, or plain chat: if today's date is not already known from the conversation, ask once before computing absolute dates.
- If the date cannot be determined, store intervals relative to "last review + N days" and do not invent overdue counts.

## Interval Algorithm

The schedule combines a coarse Leitner ladder (structure) with a per-topic ease factor (fine adaptivity). `scripts/srs.py` is the source of truth; this prose describes what it does.

When a topic is reviewed with score `S`:

1. Update the **ease** factor by recall quality, clamped to `[1.3, 2.7]`:
   - `S = 5`: +0.10 · `S = 4`: +0.00 · `S = 3`: −0.14 · `S <= 2`: −0.20
2. If `S <= 2`: set streak to 0, increment **lapses**, set next review to tomorrow.
3. If `S >= 3`: increment streak and compute the base ladder interval:

| Streak | Base Interval |
|--------|---------------|
| 1 | 1 day |
| 2 | 3 days |
| 3 | 7 days |
| 4 | 14 days |
| 5+ | 30 days |

4. Scale the base interval by the difficulty multiplier and the normalized ease:

| Difficulty | Multiplier | Effect |
|------------|-----------|--------|
| easy | 1.4 | Review less often |
| medium | 1.0 | Default |
| hard | 0.6 | Review more often |

`final_interval = max(1, int(base_interval * difficulty_multiplier * (ease / 2.5)))`

So a topic the student keeps acing drifts toward longer gaps (ease → 2.7, ~1.08x), while a shaky one is pulled in (ease → 1.3, ~0.52x) even at the same streak.

## Leech Detection

A topic whose **lapses** reach `4` is a *leech*: repeated rescheduling is not working. `srs.py update` prints a `Leech:` warning to stderr, and `due` / `list` print a leech summary. When a topic is flagged, do **not** just reschedule it — break it into prerequisites, switch teaching strategy (e.g. `/socratic` or `/feynman` instead of drill), or drop its difficulty. Surface the leech to the student rather than silently looping.

## Difficulty Ownership

Difficulty and ease have different owners, and they must not be confused:

- **Ease** is owned by the script and evolves automatically; never hand-edit it.
- **Difficulty** is owned by the model/user. `srs.py update` *suggests* a change on stderr (`Suggestion: consider --difficulty easy`) based on the just-updated row, but only applies a change when `--difficulty` is passed. When `--difficulty` is omitted, the topic's existing difficulty is preserved.

Suggestion heuristics the script surfaces:

- Score ≥ 4 with streak ≥ 3 → suggest bumping difficulty to `easy`.
- Lapses ≥ 2 → suggest dropping difficulty to `hard`.

The model may also apply the multi-session rule "scored ≤ 2 twice in a row → drop to hard"; that judgement is the model's, since the single-row script cannot see the full history. The user can always override via `--difficulty`.

## `/review-due`

When the user runs `/review-due`:

1. Agent shell:
   - If `.oh-my-teacher/srs/` and `.oh-my-teacher/srs/_active` exist, read the active multi-course SRS file.
   - Otherwise read `.oh-my-teacher/srs-state.md` if it exists.
   - Preferred helper: `python scripts/srs.py due` or `python scripts/srs.py due --today YYYY-MM-DD` (the `--today` flag defaults to the system date when omitted).
2. ima-native:
   - Use `search source=note` for the active course homepage, SRS Table, and recent wrong-question notes.
   - Use `fetch type=note_id` when a candidate note is found.
   - If multiple courses match, use `ask_user` once to confirm the active course.
   - Update the note via `ima-note` or output a copyable Markdown fallback.
3. RAG notebook, notes app, or plain chat: parse the last copyable SRS block or note table.
4. Determine today's date before filtering.
5. Filter rows where `Next Review <= today`.
6. Sort by overdue days descending, then lowest score first.
7. Present the due list and offer to start `/quiz` on the highest-priority topic.

## Automatic Updates

After each `/grade`, `/quiz`, `/mock`, `/oral`, or `/fix` answer:

- Extract the topic from the question.
- Use the score to update or create the topic row.
- Mention the update briefly with the next review date.
- Preferred helper: `python scripts/srs.py update "topic" --score 4` (omit `--today` to use the system date).

In RAG notebook, notes app, or plain chat, output the SRS table as a copyable Markdown block after each update. For notes apps, optional tags such as `#复习计划` and backlinks such as `[[极限]]` are useful when they do not clutter the table.
