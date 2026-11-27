# Changelog

Dated entries for what changed and when. Live operating rules belong in
`SKILL.md`; this file is where the "it used to work differently" narrative goes
so `SKILL.md` can stay an instruction manual instead of a history.

## 0.7.3 — 2026-11-27

### Fixed
- **Attachments were left on disk.** gog writes every attachment to a file,
  even with `--inline`, and by default into its own gmail-attachments
  directory, which nothing cleaned. Every bill PDF and school attachment read
  through `gmail.get_attachment` stayed there. Each download now goes to a
  private temp directory that is deleted before the bytes are returned.
- `draft_meal_plan`'s description said it returned a weekly plan; it returns
  today's suggestions.

## 0.7.2 — 2026-11-27

Answers ClawHub's security scan (ClawScan + Skillspector + AIG).

### Changed
- **Meal plan:** nothing locks without a person approving. A change request
  past the 2-revision limit used to lock the plan as-is and drop the request;
  it now changes nothing and returns `MAX_REVISIONS_REACHED` so the agent asks
  the family. `cmd_auto_approve` (the old Sunday-night timeout lock, unscheduled
  since 2026-08-17) and the pending plan's `expires_at` are removed.
- **pypdf 6.x** (was capped below 6.0); `requests>=2.32.4`,
  `setuptools>=78.1.1`.

### Fixed
- **DOCX attachments:** `document.xml` is capped at 20 MB inflated, so a small
  compressed attachment can't exhaust memory and wedge the school queue.
- **School mail:** removed dead code that resolved `${ENV}` placeholders for
  Google client secrets from the environment. gog holds all credentials.
- **Docs that disagreed with the code:** Infants' Tylenol concentration (the
  code was right, 32 mg/mL), the health log's "append-only" claim, the meal
  history's 30-day pruning, the lunch-constraint fallback, the tool count (44)
  and the attachment cleanup side effect of `fetch_school_emails`.

### Documentation
- SKILL.md: a fuller description, a declared `allowed-tools` scope, what data
  is kept and where it goes (including what Open-Meteo receives), and why
  scanners see `subprocess`, `os.execv` and launchd mentions.
- Comments reworded so explanations of *not* touching credentials stop
  matching credential-access patterns. No behavior change.

## 0.7.1 — 2026-11-27

No code changes. ClawHub listing moved to the `homebase-family` slug with the
display name "Homebase"; the old `homebase` slug was retired because its early
versions carried personal data.

## 0.7.0 — 2026-11-26

Fixes from the 2026-10-22 code review, plus November's travel and health-log
work. The theme: "failed", "incomplete" and
"stale" were being reported as success or as nothing.

### Removed
- The pending school-event queue: `save_pending_school_events`,
  `get_pending_school_events`, `confirm_pending_school_events`,
  `reject_pending_school_events`. Never used on this install — the school
  runner creates events with `gog` itself. It was the last calendar write, so
  `features/calendar/calendar_manager.py` and `gcal`'s create/update/delete
  went with it. Homebase now only reads the calendar.

### Fixed
- **Bills:** a failed Gmail search returned `no_new_emails`, so the
  `auth_failed` the bills runner alarms on could never fire. It raises now.
- **Bills and school mail:** search read one fixed page of newest ids and
  filtered processed ones afterwards, so older unprocessed mail behind a page
  of handled mail was never returned. Both now read every page of their
  lookback (`gmail.search(all_pages=True)`).
- **School:** the routine filter searched the body for "check-in" and friends
  and marked matches processed for good. Now only a subject starting "Daily
  summary" — every routine email in 60 days of real mail.
- **School:** body text was cut at 2,000 chars (one email in five in
  Sept–Oct) and PDF + Word text shared 4,000. Both are 20,000 now, with
  `body_truncated` / `pdf_truncated`.
- **Health:** Infants' Tylenol was 100 mg/mL (the drops withdrawn in 2011)
  and Infants' Motrin fell through to Children's 20 mg/mL. Now 32 and 40.
  Offset/`Z`/fractional ISO timestamps no longer silently become "now", and an
  unreadable time is refused. "Next dose" counts from the newest dose and is
  withheld at the 24h maximum; the reminder no longer says "safe to give".
  Contradictory mg + mL, and non-positive or non-finite amounts, are refused.
- **Meals:** `get_meal_history` ignored `days`; a weekend draft approved on
  Monday was stored as the following week. The week is fixed at draft time
  (`week_of` in the pending file — older pending files still load).
- **Snacks:** a wrong `school_closed` could never be cleared. Explicit
  `false` with `force: true` clears it; plain `false` still doesn't, since the
  two photos needn't agree.
- **Messaging:** `get_message_targets` ignored the `whatsapp.groups[]` shape.
- **Weather:** a destination that would not geocode silently became home
  weather; trip weather fell back to home too. Both return none instead.
- **Calendar:** a cancelled event that began before the sync window (a trip
  under way) survived a successful sync. Sync now returns whether every
  calendar is fresh, and both briefings carry `calendar_stale`.

### Added
- `core/docx_attachments.py`: Word attachments on school mail are extracted
  alongside PDFs.
- School fetch reports `unreachable` (a transport failure) separately from
  `auth_failed`.
- **Travel:** an all-day rental stay ("🏡 Sonoma gBnB Stay") counts as a
  trip; a guest's "Nani's stay" does not. Leading emoji no longer defeat title
  matching, and a street address is reduced to "City, ST" before geocoding.
  A flight leaving before noon makes day 1 a destination day.
- **Health:** `log_medication` with no amount repeats a recent dose of the
  same strength (within 7 days) and marks it `dose_assumed`, or asks without
  suggesting a number. `correct_assumed` fixes that entry in place instead of
  logging a second dose. `get_health_summary` ends with "Dose timing now".
- `schedule_medication_reminder` returns `deliver_to`: the family group.

### Fixed (November)
- **Health:** a clock time later than now is read as yesterday's ("11:45 PM"
  reported at 12:23 AM), for doses, fevers and symptoms.
- **gog errors:** the quoted request URL is stripped from stderr before it is
  capped at 300 chars, so the actual reason survives.
- **SKILL.md:** `metadata.openclaw.requires.bin` → `bins`.

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
