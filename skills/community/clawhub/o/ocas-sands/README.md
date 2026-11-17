# ⚙️ Sands

  <img src="./assets/readme/hero.jpg" width="100%" alt="Sands">

Calendar management. Use for viewing, querying, creating, modifying, deleting, or analyzing calendar events. Handles natural-language scheduling, conflict detection with flexibility classification, free slot finding, automatic travel time event insertion between consecutive appointments, recurring event management, and daily schedule briefings for Vesper. Do not use for reminders without calendar context, task management, or general time/timezone questions.

**Skill name:** `ocas-sands`
**Version:** 2.2.0
**Type:** 
**Layer:** productivity
**Author:** <agent-name>

---

## 📖 Overview

Calendar management. Use for viewing, querying, creating, modifying, deleting, or analyzing calendar events. Handles natural-language scheduling, conflict detection with flexibility classification, free slot finding, automatic travel time event insertion between consecutive appointments, recurring event management, and daily schedule briefings for Vesper. Do not use for reminders without calendar context, task management, or general time/timezone questions.

---

## 🔧 Capabilities

- `sands.calendar.query` — pull events for a time window; merged view with work busy overlay
- `sands.event.create` — create event from natural language with conflict pre-check and smart duration defaults
- `sands.event.modify` — update event with recurring scope control and post-modify conflict re-check
- `sands.event.delete` — cancel event with travel block cleanup and recurring scope control
- `sands.event.undo` — revert most recent calendar action (within 24 hours)
- `sands.schedule.free` — find available time slots for a given duration with constraints
- `sands.schedule.conflicts` — analyze time window for conflicts with flexibility classification. See `references/conflict-report-format.md` for output template.
- `sands.logistics.travel` — insert travel time block between events via Google Places API
- `sands.briefing.generate` — generate structured schedule summary for Vesper emission
- `sands.status` — skill health, configured calendars, API connectivity, current timezone
- `sands.journal` — write journal for the current run; called at end of every run
- `sands.update` — pull latest from GitHub source; preserves journals and data
- `sands.chronicle.sync` — push travel, medical, and personal calendar events into Chronicle as persistent facts
- **`400 Bad Request` from oauth2.googleapis.com = dead credentials** — Besides `invalid_grant`, expired/revoked refresh tokens can return HTTP `400` from the token endpoint. Surfaces as `"400 Client Error: Bad Request for url: https://oauth2.googleapis.com/token"` from `get_service()`. Treat identically to `invalid_grant`: log, move to next account. Do NOT interpret `400` as a bug in your code.
- **`config.json` `auth_status` can be stale after fallback** — When the primary account's token is dead but the fallback account succeeds, `auth_status` may still say `MCP_ONLY` or `STALE_OAUTH`. After a successful direct-Python fallback, update `auth_status` to `OK` so the next run doesn't pre-emptively assume degradation. The field reflects the *system's* ability to reach the calendar, not any single account's token state.
- `templates/sands_briefing_morning.py` — Reusable cron-compatible morning briefing script with multi-account fallback, dedup, conflict detection, and prep-signal checking.

---

## 📊 Outputs

See `SKILL.md` for outputs, journals, and persistence rules.

---

## 📄 Files

| File | Purpose |
|---|---|
| `SKILL.md` | Skill definition |
| `references/` | Supporting documentation |
| `scripts/` | Helper scripts |


## Changelog

- [2.1.4] - 2026-04-12
- Added
- [2026-04-04] Spec Compliance Update
- Changes
- Validation
- [2.1.1] - 2026-04-08
- Storage Architecture Update
- [2.1.0] - 2026-04-08

---

## 📚 Documentation

Read `SKILL.md` for operational details, schemas, and validation rules.

Read `references/` for detailed specifications and examples.


---

## 📄 License

MIT License — see `LICENSE` for details.
