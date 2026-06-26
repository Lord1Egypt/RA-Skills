# Changelog

All notable changes to this project will be documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),

## 0.3.0 (2026-05-10)

- Dashboard overhaul: every tracker defaults to a date-grid visualization
- New trackers auto-infer chart type: numeric fields → heatmap, text/bool → calendar_grid
- Mood: changed to calendar_grid for glance-friendly daily view
- MIT: changed to calendar_grid showing 90-day completion history
- Scaffold template includes `_presence` marker for text-only trackers
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2026-05-04

Initial public release.

### Added

- **Single CLI** (`glancely`) with subcommands for every component:
  `setup`, `doctor`, `diary`, `mood`, `reminder`, `mit`, `scaffold`,
  `dashboard`, `list`.
- **Component framework** (`glancely/core/`): per-component SQL
  migrations into a shared `~/.glancely/data.db`, filesystem-driven
  registry (no central registry file), Google OAuth (user brings own
  client), openclaw cron registration helpers.
- **Shipped components**:
  - `diary_logger` — time-tracked activities written to a user-owned
    Google Calendar; English + Chinese natural-language time parsing.
  - `mood` — hourly check-ins with raw reply storage.
  - `reminder` — add/done/list + markdown digest for cron prompts.
  - `mit` — nightly Most Important Task check-in.
  - `scaffold_component` — meta-skill that creates a new tracker
    end-to-end (folder + skill + migrations + cron + dashboard panel).
- **Read-only dashboard** (`glancely dashboard build`) — static HTML
  rendered from each component's `stats.py`.
- **Demo fixture** (`examples/demo-data/seed.py`) for reproducing the README
  screenshot without an OAuth client.
- **Tests** — 13 across migrations, scaffolder, and component round-trips.
- **CI** — pytest on Python 3.9 / 3.11 / 3.12 + dashboard build smoke check.

### Known limitations

- Diary path requires the user to bring their own Google OAuth client and
  manually create a Calendar named "Glance Diary" (or set
  `GLANCE_DIARY_CALENDAR_ID`). Verification dialog will say
  "unverified app" since each user uses their own client.
- Notifications are dispatched via openclaw cron only. There is no
  Windows/desktop fallback.
- Stats are computed on every dashboard build with no caching. Fine at ten
  components, will get slow beyond that.

[Unreleased]: https://github.com/JunjieYu95/glancely/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/JunjieYu95/glancely/releases/tag/v0.1.0
