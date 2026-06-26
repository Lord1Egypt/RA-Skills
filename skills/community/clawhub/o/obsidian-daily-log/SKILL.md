---
name: obsidian-daily-log
description: Update freznel's Obsidian daily note with timestamped activity entries, especially day recaps, travel logs, itineraries, movement updates, and "I did X at Y time" messages. Use when freznel reports what happened during a day, wants a running timeline added to the daily note, needs backfilled time-stamped logs for travel, commute, meetings, meals, or errands, or asks to save a day summary into the Obsidian vault.
---

# Obsidian Daily Log

Update freznel's Obsidian daily note in the superyas vault by appending timestamped entries to a `## Timeline` section. Prefer compact chronological logging that stays readable in Obsidian on mobile and desktop.

## Vault conventions

- Vault path: `C:\Users\frezn\iCloudDrive\iCloud~md~obsidian\superyas`
- Daily notes folder: `01 Daily`
- Daily note filename: `YYYY-MM-DD.md`
- Daily note template: `Templates\Daily Note.md`
- Default insertion section: `## Timeline` placed before `## Notes`

## Group-chat safety

Allow this skill in Telegram groups and other shared chats only when freznel clearly intends to log something to the vault.

Strong triggers:
- messages starting with `/dailylog`, `/travellog`, or `/timeline`
- direct prompts like `add this to my daily note`, `save this to Obsidian`, or `log this for today`
- clear first-person day recaps addressed to the assistant

Do not write to the vault from ordinary group banter, third-party messages, or ambiguous conversation fragments.
If intent is unclear in a group, ask one short confirmation question before saving.

## Workflow

1. Determine the target date.
   - If freznel says "today", use the current date.
   - If freznel gives a date, use that exact date.
   - If the date is ambiguous, ask one short clarifying question.
2. Prefer natural-language inference first.
   - Accept messy recaps, travel updates, partial timelines, and conversational summaries.
   - Infer sequence, approximate times, locations, and activity boundaries from context.
   - Convert the recap into clean chronological entries.
3. Extract each activity into structured fields:
   - `time` in `HH:MM` 24-hour form
   - `activity` as a short action phrase
   - optional `location`
   - optional `tags`
4. Choose output mode.
   - Prefer `bullets` for normal daily logging and travel updates.
   - Use `table` only when freznel explicitly asks for a table or when the day is highly structured and comparable across many entries.
5. Run `scripts/update_daily_log.py`.
6. Confirm what was saved and which note was updated.

## Obsidian Markdown conventions

Use native Obsidian Markdown where it improves readability, but keep daily logging lightweight.

- Prefer standard Markdown headings and bullet lists for timeline capture.
- Use callouts only for summaries, key travel notes, or notable incidents — not for every timeline line.
- Keep callouts compact, for example:

```markdown
> [!tip] Travel day
> Landed on time. Hotel check-in was smooth.
```

- Avoid large tables unless the entries are consistently structured.
- Preserve compatibility with normal Markdown rendering; do not depend on exotic plugin-only syntax for core timeline content.
- Use emoji sparingly inside timeline bullets when they add scanning value, such as `📍` for location.

## Format policy

### Default: bullets

Use bullets for most cases because they are easier to dictate, faster to scan on mobile, and more tolerant of messy real-life travel notes.

Example:

```markdown
## Timeline

- 06:45 — Left home for airport — 📍 Manila
- 08:10 — Checked in and cleared security — 📍 NAIA T3
- 11:35 — Landed — 📍 Singapore
- 13:00 — Reached hotel and checked in — 📍 Bugis
```

### Optional: table

Use a table when the user asks for one, when entries naturally fit consistent fields, or when location and tags matter enough to justify columns.

Example:

```markdown
## Timeline

| Time | Activity | Location | Tags |
|---|---|---|---|
| 06:45 | Left home for airport | Manila | #travel #airport |
| 08:10 | Checked in and cleared security | NAIA T3 | #travel |
| 11:35 | Landed | Singapore | #flight |
```

## Recommendation logic

- Recommend **bullets** by default.
- Recommend **table** for trip reports with many repeated attributes, such as `time / place / transport / status`.
- If freznel asks whether a table should be auto-generated, answer: **not by default**. Auto-generate only when the day has 6+ structured entries or freznel explicitly wants spreadsheet-like review.
- If a recap or takeaway would help, add a short Obsidian callout after the timeline instead of overloading each entry.

## Running the updater

Use this script:

- `scripts/update_daily_log.py`

Typical bullet example:

```powershell
python scripts/update_daily_log.py --date 2026-03-30 --mode bullets --time 06:45 --text "Left home for airport" --location "Manila" --tags "#travel" --time 08:10 --text "Checked in and cleared security" --location "NAIA T3" --tags "#airport #travel"
```

Typical table example:

```powershell
python scripts/update_daily_log.py --date 2026-03-30 --mode table --time 06:45 --text "Left home for airport" --location "Manila" --tags "#travel" --time 08:10 --text "Checked in and cleared security" --location "NAIA T3" --tags "#airport #travel"
```

## Notes for interpretation

- Normalize times like `7`, `7am`, `7:15 pm`, `19:15` into `HH:MM`.
- Keep activity text concise; do not write long narrative paragraphs inside the timeline.
- If freznel sends a narrative recap, convert it into separate timestamped entries when possible.
- Prefer inference over rigid parsing. freznel should not need to write machine-friendly input.
- Treat `/dailylog`, `/travellog`, and `/timeline` as strong save-to-note triggers, but accept plain-language prompts like `add this to today's note` too.
- Preserve chronology by sorting entries by time.
- Avoid duplicating identical lines if the same update is logged twice.
- If no exact time is available, ask whether to log an approximate time only when timing materially matters. Otherwise, use the best reasonable approximation and say so briefly.
