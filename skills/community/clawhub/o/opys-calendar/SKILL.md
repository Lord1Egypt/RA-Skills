---
name: opys-calendar-skill
description: A local markdown-backed calendar with CLI and optional two-way Google Calendar sync.
env:
  - GOOGLE_CLIENT_ID
  - GOOGLE_CLIENT_SECRET
  - GOOGLE_REDIRECT_URI
  - APP_BASE_URL
  - CALENDAR_AGENT_SNAPSHOT
  - CALENDAR_AGENT_DAYS
---
# Calendar Markdown + Google Sync Skill

Use this skill to query/update the local markdown-backed calendar safely and sync it with Google Calendar.

## Source of Truth

- File: `calendar.md`
- Authoritative section: `## Event Records` (fenced `event` YAML blocks)
- Human summary section: `## Event Checklist`

## Event Identity Rules

- `id`: local identifier
- `externalId`: stable cross-system identifier used for dedupe
- `googleEventIds`: per-calendar Google event mapping
- `updatedAt`: event-level timestamp for conflict resolution

Do not remove `externalId` from existing records.

## Preferred Interface

Use CLI from repo root:

```bash
npm run cli -- <command>
```

## Safe Query Flow

1. Run `npm run cli -- summary`.
2. If raw markdown is needed, run `npm run cli -- export`.

## Safe Update Flow

1. Add (preferred for new events):
   `npm run cli -- add --title "..." --start "<ISO>" --end "<ISO>" --category <id> [--shift-to-next|--allow-overlap]`
2. Update:
   `npm run cli -- update --id <event_id> [fields...]`
   If changing `--start` or `--end`, include `--shift-to-next` or `--allow-overlap` in non-interactive runs.
3. Check/uncheck:
   `npm run cli -- check --id <event_id>` or `--undone`
4. Delete:
   `npm run cli -- delete --id <event_id>`
5. Add category:
   `npm run cli -- category-add --id <id> --label "Label" --color "#9ca3af" --description "..."`
6. Remove category:
   `npm run cli -- category-remove --id <id> --reassign <id>`

Conflict handling:

- `add` and time-changing `update` detect overlaps with existing events.
- Interactive runs can choose accept overlap, shift to next available slot, or provide a custom time.
- Non-interactive runs:
- `--shift-to-next` to auto-resolve to the next open window.
- `--allow-overlap` to keep the requested overlapping time.

Agent snapshot output:

- Every mutating CLI command writes a rolling markdown snapshot.
- Default path: `./agent-snapshot.md`
- Override with `CALENDAR_AGENT_SNAPSHOT`.
- Recent window defaults to 14 days and is configurable with `CALENDAR_AGENT_DAYS`.
- Snapshot also includes upcoming 7 days when events exist.

## UI Constraints

- UI does not provide add-event form/button.
- Events are created via CLI agents only.
- UI still supports drag/drop, resize, and check-off.

## Google Sync Flow

1. In UI, sign in with Google.
2. Select target calendar via calendar selector controls.
3. Click **Sync Now** for two-way merge.

Sync state file:

- `.calendar-google-sync-state.json`

## Import/Export

- Export: `npm run cli -- export --out backup-calendar.md`
- Import: `npm run cli -- import --in backup-calendar.md`

## Notes for Agents

- Keep datetimes in ISO format.
- Prefer CLI operations over manual markdown edits.
- If categories are changed manually in frontmatter, keep `id`, `label`, and `color` fields valid.

## Environment Variables

This skill uses the following environment variables (defined in `.env`):

- **Google Calendar Sync (Optional)**
  - `GOOGLE_CLIENT_ID`: Google OAuth Client ID
  - `GOOGLE_CLIENT_SECRET`: Google OAuth Client Secret
  - `GOOGLE_REDIRECT_URI`: Should be `http://localhost:<PORT>/api/google/auth/callback`

- **Agent Configuration (Optional)**
  - `CALENDAR_AGENT_SNAPSHOT`: Custom absolute or relative path to write the Markdown snapshot. Defaults to `./agent-snapshot.md`.
  - `CALENDAR_AGENT_DAYS`: Number of historical days to include in the snapshot (defaults to 14).
  - `PORT`: API server port (defaults to 8787).
  - `APP_BASE_URL`: Base URL for the frontend UI.
