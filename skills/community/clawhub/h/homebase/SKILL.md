---
name: homebase
description: "Family household coordinator: calendar, briefings, kids' meals, school email, groceries, health log, receipts. Every tool goes through tools.py — read this before calling one."
metadata: {"openclaw": {"requires": {"bin": ["gog"]}}}
license: MIT
---

# Homebase

A household data layer for a family: the calendar, the morning and evening
briefings, the kids' meals, the grocery list, the school inbox, medication and
receipts — one place, configured per family in `config.json`, no code per
family.

**Python returns data. The caller composes and sends.** Nothing in this skill
formats a message, delivers one, calls an LLM, or schedules anything. That
division is the whole architecture: the agent (or a scheduler you write) reads
these tools and decides what to say.

## Calling a tool

```
python3 {baseDir}/tools.py <tool_name> '<json_args>'
```

- **Always give `tools.py` an absolute path, and never `cd` first.** This is
  the one shell habit that predicts failure: `cd`-then-relative-path calls fail
  at 20% against a 1.6% baseline, because the working directory the exec host
  hands you is not the one you assumed.
- **One tool per exec call.** Chaining with `&&`/`||` is a smaller but real
  risk (4.9% vs 1.6%): the second command runs against state you have not read,
  and a failure in the first is easy to miss.
- `~`, `$(...)` and pipes are fine — measured within noise of baseline. Don't
  contort a command to avoid them.
- Tools taking no arguments need no third argument; `'{}'` is equivalent.
- **A non-zero exit is a failure even when there is no `❌`** — the command
  broke before the tool ran. Say so; never treat it as "nothing to report".
  The reverse also holds: most `❌` returns exit 0, so judge by the output.

**If any value contains an apostrophe, use the stdin form.** A `'` inside the
single-quoted argument closes it and the shell dies before Python runs — you
get `unmatched "`, not a `❌`. Backslash-escaping does not work inside single
quotes. Pass `-` as the argument and heredoc the JSON:

```
python3 {baseDir}/tools.py log_restaurant_visit - <<'JSON'
{"restaurant":"Romy's","meal_type":"lunch","date":"2026-06-12","total":42.50}
JSON
```

Use the stdin form whenever a value holds `'`, emoji, newlines, or text you
extracted from an email, a photo or a message — anything you did not author.
The quoted `<<'JSON'` matters: it stops the shell expanding `$` and backticks.

**Non-agent callers use the shim:** `{baseDir}/bin/homebase.sh <tool> '<json>'`.
It pins the interpreter to homebase's venv. Prefer it in any script or
scheduler — `tools.py` can re-exec itself under the venv, but only when the
calling interpreter both lacks `pypdf` and resolves to a different binary than
`.venv/bin/python`, which is not true of a Homebrew `python3.12`.

## Finding a tool

`tools.py list` prints all 48 tool names. An unknown name returns a
`Did you mean:` suggestion rather than a silent failure. Use it instead of
guessing a name — invented names like `check_school_emails` are a known way to
burn a turn.

## Tool surface

All 48 tools. **W** marks a tool that writes state. Exact arguments for every
one are in `{baseDir}/references/agent.md`.

**Briefings, weather, travel**

| Tool | Does |
|---|---|
| `get_morning_briefing` **W** | The whole morning payload: date, weather, events, snack, travel, `warnings`. Syncs the calendar and updates the 60-day reliability tracker. |
| `get_evening_prep` **W** | Tomorrow's events and the kids' locked meals, for the "so do this tonight" message. Syncs the calendar. |
| `get_weather` | Today's raw forecast. |
| `get_weather_context` | Hourly forecast across a window (default 08–17) plus US AQI. |
| `get_travel_status` | Is the household away on a date, and where. `{"sync":true}` forces a calendar refresh first **(W)**. |
| `get_message_targets` | The configured owner, family group, alert webhook and **`calendar_id`** — use this id for any `gog` calendar call, never gog's default. |

**Kids' meals and the weekly plan**

| Tool | Does |
|---|---|
| `get_kids_meals` | The locked plan's breakfast/lunch/side per kid for a date. |
| `get_meal_suggestions` | Today's pre-picked suggestion per kid, when no plan is locked. |
| `log_kids_meal` **W** | Record one food, for one kid, in one slot. |
| `get_meal_history` | Recent meal log. |
| `get_weekly_meal_pool` | The per-day, per-kid, per-slot menu pool. |
| `get_morning_meal_checkin_text` | The canonical "what did the kids eat?" question. |
| `draft_meal_plan` | A starting-point draft. |
| `save_meal_plan` **W** | Validate and stage a plan. Rejects meals outside the catalog. |
| `get_pending_meal_plan` | The staged draft awaiting a reply. |
| `handle_meal_plan_response` **W** | Approve and lock, or revise. Max 2 revisions, then auto-locks. |
| `approve_meal_plan` **W** | Approve with no changes. |
| `get_pending_catalog_reviews` | Off-catalog meals awaiting approval. |
| `apply_catalog_review` **W** | Accept or reject them into the learned catalog. |

**School: snacks, email queue, proposed events**

| Tool | Does |
|---|---|
| `get_school_roster` | School name and the kids with their teachers. |
| `get_snack_schedule` | The stored snack schedule for the month. |
| `save_snack_schedule` **W** | Save a month of snack duty. Refuses a write that looks like the same photo read twice; `"force":true` overrides. |
| `fetch_school_emails` **W** | **A queue, not a mail reader** — see below. |
| `mark_email_synced` **W** | Advance the queue. Call *after* acting, never before. |
| `save_pending_school_events` **W** | Stage events extracted from an email for the family to approve. |
| `get_pending_school_events` **W** | The approval queue (purges entries older than 3 days on read). |
| `confirm_pending_school_events` **W** | Create the approved events on Google Calendar. The only calendar *write* homebase still makes. |
| `reject_pending_school_events` **W** | Drop them without creating anything. |

**Groceries and restaurants**

| Tool | Does |
|---|---|
| `get_grocery_list` | The list, optionally for one store. |
| `add_to_grocery_list` **W** | Add items to a store bucket. |
| `remove_from_grocery_list` **W** | Remove by name match. |
| `log_restaurant_visit` **W** | Record a visit. Merges on `(date, restaurant)`. |
| `rate_restaurant` **W** | Attach a rating and notes, per person. |
| `get_restaurant_recommendations` | Suggestions, optionally by meal type. |
| `get_top_restaurants` | Highest-rated places. |

**Health** — advisory, not a gate. Every dose is logged; warnings never block.

| Tool | Does |
|---|---|
| `log_medication` **W** | Log a dose. Warns on weight-based range, minimum interval and the 24h count. |
| `log_fever` **W** | Log a temperature, or a subjective fever. |
| `log_symptom` **W** | Log symptoms. |
| `get_health_summary` | A doctor-friendly summary over N days. |
| `update_child_weight` **W** | Update a weight. A child with no weight gets **no** dose-range checking at all. |
| `schedule_medication_reminder` **W** | Note a follow-up dose time. |

**Kid profiles and trips**

| Tool | Does |
|---|---|
| `log_kid_observation` **W** | Append an observation to a child's profile. |
| `get_kid_profile` | Weight, observations, preferences. |
| `get_trip_data` | Destination forecast, environment tags, per-kid prep notes. |
| `get_trip_prep` | Legacy text form of the same. |
| `mark_trip_prep_sent` **W** | Record that prep went out, so it doesn't repeat. |

**Bills** — only when `bills.enabled` is true in `config.json`.

| Tool | Does |
|---|---|
| `fetch_bill_emails` **W** | At most **one** bill per call, with its PDF text extracted. Marks nothing. |
| `mark_bill_processed` **W** | The second half: fetch → deliver → *then* mark. |

### Two of these are queues, not mail readers

`fetch_school_emails` and `fetch_bill_emails` exist to feed a scheduled caller.
They filter aggressively, return at most a narrow slice, and hand back a bare
`[]` on several different drop paths. **Never call either to answer a person
asking about their mail** — `gog gmail messages search "<q>" --max 5 --json`
does that in one call.

Both are half of a two-phase contract: they return work *unmarked*, and the
caller marks it only after the message actually went out. Marking first is how
an email gets consumed by a send that failed.

## Rules that are not guessable

- Route every household action through `tools.py`. Never use `write`/`edit` to
  save household data.
- One call per kid per meal slot. Never compound foods into one call.
- Only claim a tool succeeded if you have seen its confirmation string this
  turn. If it returns an error starting with `❌`, surface that verbatim.
- After any state-changing call, reply with a one-line summary. An empty turn
  after a flurry of tool calls is a known failure mode.
- **homebase has no calendar tools.** It keeps a read-only *sync* of the family
  calendar for the briefings and travel mode; Google is the `gog` skill's.
  Read and write the calendar with `gog` directly.
- If you run a feature script directly (only those with a `__main__` block),
  use `.venv/bin/python3`. Bare `python3` resolves to an interpreter without
  this skill's packages. Measured: `.venv/bin/python3` 132 calls / 0 failures,
  bare `python3` 12 calls / 9 failures. `features/meals/meal_tracker.py` is a
  library with no `__main__` — never run it directly.
- The skill is `homebase`. There is no `family-calendar-aggregator`.

## Incoming images: act, don't describe

Read the photo with the `view_image` tool (path as a string, not a list), infer
the action from context and document type — snack calendar → `save_snack_schedule`,
receipt → `log_restaurant_visit`, itinerary → a calendar write through `gog` —
then take it. Never end the turn having only extracted the content.

- **Give the `view_image` call a target.** Ask it for the fields the tool you
  are about to call needs. A bare "what is this and what should be done?" gets
  answered from the *sender's* point of view — a restaurant bill came back as
  "process a payment from the customer", which is advice for the restaurant.
- **There is no "personal" exemption.** One adult's dinner receipt is household
  data. Classifying a photo as personal and asking what to do with it is the
  same failure as describing it.
- **Each photo lands in its own `openclaw-staged-<uuid>/` directory.** Two
  images sent minutes apart do not share one. To re-read an earlier photo, take
  its path from that photo's own earlier `view_image` call in this transcript —
  do not reuse the most recent path, and do not `ls` one staged directory and
  conclude it is the only image. `view_image` answers the prompt it is given:
  asked for "the morning snack schedule" while pointed at the afternoon
  calendar, it will return afternoon items under a "Morning" heading.

`log_restaurant_visit` merges on `(date, restaurant)`, so a receipt for a meal
the evening sync already auto-logged enriches that record rather than creating a
second one. Log it; do not check first.

## Travel: put the trip on the calendar

When the family says they are travelling — "we're in Seattle next week", "I'm
away the 3rd to the 7th", a forwarded itinerary — that means one calendar write.
Create it with `gog`, using the `calendar_id` from `get_message_targets`:

```
gog calendar create <calendar-id> --summary "Trip to Seattle" \
  --from 2026-08-29 --to 2026-09-07 --all-day \
  --location "Seattle, WA" --json --no-input
```

Google's all-day end date is **exclusive**: a trip whose last night away is
Sep 6 is written `--to 2026-09-07`.

Three properties are load-bearing — do not improvise them:

- **All-day, spanning every night away.** `get_travel_status` reads only all-day
  events, because a timed one is something that happens *during* a day rather
  than a statement about where the household is sleeping. Booking the flight is
  not enough: "Flight UA2316 LAX to SEA" is timed and changes nothing.
- **A title the matcher recognises** — `Trip to X`, `Travel to X` (also
  `Travelling`/`Traveling`), `X trip`, `Vacation in/to/at X`, bare `Vacation`,
  `Out of town`, or `In X (trip)`. Anything else silently does nothing.
  ⚠️ `X trip` matches *any* word before "trip", so an all-day **`Field trip`**
  on the family calendar will read as the household being away. Title school
  outings something else.
- **`--location` as a geocodable place** — "Seattle, WA", not a nickname. It is
  what the forecast is fetched for.

Say what you created and over which dates. This event is why the briefings
follow the family, so a wrong range is a week of wrong weather. Telling *you* is
not enough: a scheduled briefing never talks to the agent, and the calendar is
the only thing you both read.

## What homebase does not do

- **Never composes or sends a message.** No WhatsApp, no email, no LLM call.
- **Never schedules anything.** No cron, no timers. Drive it from your own
  scheduler through `bin/homebase.sh`.
- **Holds no credentials.** `gog` owns the Google OAuth token and mints an
  access token per invocation. `core/gcal.py` and `core/gmail.py` are the only
  modules that reach Google, and both do it by exec'ing `gog`.
- **Never reads OpenClaw's own state** — no session store, no cron tables.

## Requirements and setup

- Python 3.12+ and a populated `.venv` (the most common install failure).
- The `gog` CLI, authenticated for Gmail + Calendar. It is a **binary**
  dependency; pip cannot install it.

```
cp config.example.json config.json && chmod 600 config.json   # then fill it in
gog auth add <your-google-account> --services gmail,calendar
pip install -e .
python -m pytest          # 587 tests
python setup_check.py     # config + gog auth + live calendar sanity check
```

`config.json` is the only file holding anything private — group ids, phone
numbers, kid names, the calendar id, school addresses. Keep it `chmod 600`;
`setup_check.py` verifies that. Tests never read it: they run against their own
fixture via `HOMEBASE_CONFIG`.

## State and privacy

All household state is local JSON under `household/` and `calendar_data/`,
written atomically (tempfile + fsync + rename) so a crash mid-write cannot
leave corrupt JSON. Files land at mode 600.

Outbound network, the complete list:

- **Google Gmail + Calendar**, reached indirectly — homebase execs `gog`, and
  `gog` makes the HTTPS call. No Google traffic starts in this skill's process.
- **Open-Meteo**, keyless and account-less, no PII sent: `api.open-meteo.com`
  (forecasts), `geocoding-api.open-meteo.com` (destination → coordinates),
  `air-quality-api.open-meteo.com` (AQI).
- **`zenquotes.io`** for the briefing's thought of the day. No key; on any
  failure it falls back to a local pool.

No telemetry, no analytics, no third-party tracking. Nothing else is contacted.

## Limitations

- Google access requires `gog`, which stores its refresh token in the macOS
  Keychain. Elsewhere it depends on whatever keyring backend gog finds;
  `gog auth status` reports which.
- The calendar sync merges every `supported_calendars` entry with
  `enabled: true`. Disabling an entry also evicts its cached events.
- Health warnings are advisory. Nothing refuses a dose.

## Troubleshooting

- **Briefing missing weather** — Open-Meteo rate limit. The 60-day reliability
  tracker in `household/briefing_reliability.json` flags the day `degraded`.
- **Gmail or Calendar auth error** — check `gog auth status`, re-authorize with
  `gog auth add <account> --services gmail,calendar`. The school email monitor
  alerts once on an auth failure, then goes silent until fixed.
- **JSON file corrupt** — atomic writes prevent this normally. If it happens
  (e.g. disk full), delete the file and the loader recreates an empty one.

## Reference

- `{baseDir}/references/agent.md` — exact arguments for all 48 tools.
- `{baseDir}/README.md` — installation and configuration.
- `{baseDir}/CHANGELOG.md` — what changed, and when.

## License

MIT
