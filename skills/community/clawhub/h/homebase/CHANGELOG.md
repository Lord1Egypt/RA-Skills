# Changelog

Dated entries for what changed and when. Live operating rules belong in
`SKILL.md`; this file is where the "it used to work differently" narrative goes
so `SKILL.md` can stay an instruction manual instead of a history.

## 0.6.0 — 2026-09-20

**Breaking: the calendar tool surface is gone.** Google access moved to the
`gog` CLI, and with it every calendar wrapper.

### Removed
- All eight calendar tools: `get_events_for_date`, `get_events_for_range`,
  `get_next_event`, `get_tomorrow_events`, `check_calendar_for_date`,
  `add_calendar_event`, `update_calendar_event`, `delete_calendar_event`.
  Read and write the calendar with `gog` directly; get the calendar id from
  `get_message_targets`, never gog's default (the account's *primary*).
  `confirm_pending_school_events` is the one calendar write homebase still makes.
- `core/keychain_secrets.py`, `core/reauth_google.py`, `migrate_to_keychain.py`
  and the `.env` they read. The skill now holds no credentials at all: `gog`
  owns the OAuth refresh token and mints an access token per invocation.
- Dependencies `google-api-python-client`, `google-auth`, `google-auth-httplib2`,
  `google-auth-oauthlib`, `keyring` and `python-dotenv`. Only `requests` and
  `pypdf` remain.
- `com.openclaw.daemon.plist` — a second gateway contending for the same port
  and session. OpenClaw installs and owns its own gateway agent.
- `get_cron_health_digest`, which read OpenClaw's own SQLite state. Nothing in
  this skill reads OpenClaw internals any more.
- The 5:50 AM briefing pre-flight check, deleted with the cron job it guarded.

### Added
- `core/gcal.py` and `core/gmail.py` — the only two modules that reach Google,
  both by exec'ing `gog`. `GOG_BIN` overrides the binary; the test suite points
  it at a path that cannot exist so a missing mock fails loudly.
- `HOMEBASE_CONFIG` environment override in `core/config_loader.py`. The test
  suite sets it, so tests run against their own fixture instead of whatever
  `config.json` is on the machine.
- `bin/homebase.sh` as the real shim. `bin/homebase` forwards to it and stays
  for existing callers. The `.sh` extension matters: ClawHub publishes only
  known text extensions, so the extensionless script was being silently dropped
  from the published package.
- `tools.py list` — prints all 48 tool names; unknown names get a
  `Did you mean:` suggestion.
- `LICENSE` (MIT), declared in `pyproject.toml` since the start but never shipped.
- `CHANGELOG.md` (this file).

### Fixed
- **Privacy: real family data removed from every publishable file.** Children's
  and adults' first names, two teachers' email addresses, the school name and
  its email domain were hardcoded across `references/agent.md`, three source
  modules and eleven test files — roughly 250 occurrences. All are now neutral
  placeholders. The same values were present in the published package and in
  git history; see "Known gaps" below.
- **`pyproject.toml` declared no dependencies.** `classifiers` and
  `dependencies` sat below `[project.urls]`, which TOML reads as
  `project.urls.classifiers` / `project.urls.dependencies`. `pip install -e .`
  failed outright on the former; had it not, it would have installed nothing.
  Both now sit above `[project.urls]`, with a comment pinning the order.
- `migrate_to_keychain` removed from `[tool.setuptools] py-modules`, where it
  referenced a deleted file and broke the build.
- 49 tests only passed against the maintainer's private `config.json`. They now
  run against the conftest fixture.
- `bin/homebase.sh` reports a missing venv on **stdout**, not stderr — callers
  capture stdout and match a leading `❌`, so the old message was invisible.
- Dead `.env` load removed from `features/calendar/calendar_aggregator.py`, and
  `setup_check.py` now checks the dependencies that actually exist.
- `.gitignore`: added `config.json.*`, `*.bak`, `*.bak.*`, `*.bak-*`, `*.orig`,
  `.ruff_cache/`, `.coverage`, `htmlcov/`. The literal `config.json` rule
  matched only that exact name, leaving a full copy of the config — phone
  numbers, WhatsApp jids, calendar id, home address — untracked *and*
  unignored, one `git add -A` from being committed.

### Documentation
- `SKILL.md` rewritten as an operating manual. It now documents **all 48 tools**
  (it named 13), and the dated incident narrative moved here. Frontmatter
  `description` cut from 446 to 175 characters — it is injected every session.

### Known gaps (not fixed in this release)
- Git history still contains the real names in every prior commit. Scrubbing the
  working tree does not rewrite history.
- An all-day event titled `Field trip` matches the `X trip` travel pattern and
  reads as the household being away. `SKILL.md` warns; the matcher is unchanged.
- A failed Gmail search in the bills watcher returns `[]`, which the caller
  cannot distinguish from a quiet day, so a broken token stays silent.
- `confirm_pending_school_events` clears the pending queue even when every
  calendar write failed.
- Weight-based dose checking is skipped entirely for a child with no recorded
  weight.

## 0.5.1 — 2026-07-18

Last release published before the `gog` migration. Withdrawn from ClawHub on
2026-09-20: it contained real children's names, their school, and their
teachers' email addresses.

## Earlier

- **2026-08-17** — All recurring work left OpenClaw cron. Nothing in this skill
  schedules anything; the weekly meal-plan cadence and the receipt/media
  directory scanner became on-demand only.
- **2026-08-16** — `meal_suggestions` dropped from the morning briefing. The
  field is still populated: these tools deliberately return more than any one
  caller uses, so don't assume every field belongs in the message.
