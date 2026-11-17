# Installation & Instantiation

This skill is portable; a *running instance* is setup-specific. Installing means
binding the generic skill to one machine's paths, tools, schedule, and delivery
choice. Do it once per setup.

## 1. Resolve the environment

- **Profile root:** `$HERMES_HOME` if set, else the directory this skill is
  installed under (parent of `skills/`).
- **Target file:** `<profile>/memories/USER.md`. Create it if missing.
- **Host timezone:** read from the system (e.g. `timedatectl`). The schedule and
  all date math use this zone.

## 2. Discover capabilities

List the tools the setup exposes and map them to the four roles
(CALENDAR / SESSIONS / EMAIL / MEMORY — see `data-sources.md`). Record which are
present. Absent roles are fine; the skill degrades. Confirm each tool resolves
before relying on it (a context engine in fallback mode counts as absent).

## 3. Choose configuration

| Knob | Default | Notes |
|------|---------|-------|
| `deliver` | `local` | Silent, write-only. Set to a chat target only if the owner wants a morning push (usually unnecessary — USER.md reaches the agent via session load). |
| `schedule` | daily, early morning, host TZ | e.g. cron `0 7 * * *` for 7am. |
| `word_budget` | 300 | Max words in the block. |

## 4. Register the scheduled job

On Hermes, add a cron job in `<profile>/cron/jobs.json`. The cron prompt is
**inlined** and does not auto-read this SKILL.md, so the prompt must carry the
workflow itself. Build the prompt from the skill's workflow (Steps 0-8), with the
resolved USER.md path and chosen `deliver` substituted in. Set the job's `deliver`
field to the chosen target (`local` for silent). Keep the prompt and this skill in
sync on every future change (see `constraints.md`).

A minimal job shape:

```json
{
  "name": "daily-user-context",
  "skills": ["ocas-usercontext"],
  "schedule": { "kind": "cron", "expr": "0 7 * * *" },
  "deliver": "local",
  "prompt": "<workflow prompt with resolved path + deliver=local>"
}
```

`deliver` values: `local` = no chat delivery (write-only); `origin` = the channel
the job originated from; a platform name (e.g. `telegram`) = that platform's home
channel. The Hermes scheduler resolves `local` to no delivery.

## 5. Verify

- Trigger one run (or wait for the schedule). Confirm the `## Daily Context` block
  in USER.md updated and that no other section changed (`validation.md` safety
  gates).
- Confirm delivery matched intent: silent for `local`, a single message for a chat
  target.

## Reference instance (author's box)

For context, the original deployment (indigo profile) is configured as:

- Profile: `$HERMES_HOME` = `~/.hermes/profiles/indigo`; target
  `memories/USER.md`.
- Roles present: CALENDAR + EMAIL (google-workspace), SESSIONS (`session_search`),
  MEMORY (`memory`). The chronicle context engine runs in fallback there, so its
  query tool is treated as absent.
- Schedule `0 7 * * *` (host TZ America/Los_Angeles), `deliver: local` (silent),
  `word_budget: 300`.
- Harness cap: `context_file_max_chars: 12000` (explicit in `config.yaml`, so it
  overrides the dynamic cap). At a recent run USER.md was ~1.9K chars total with
  ~1.3K in sections other than Daily Context, leaving ample headroom; the skill
  still measures and enforces it every run rather than assuming.
- Calendar access: Google Workspace via `google_auth.py`. The primary account's
  OAuth token may expire between cron runs — the agent's own account
  (`<agent-email>`) serves as fallback (has calendar sharing).
  See `references/cron-calendar-access.md` for the full fallback pattern.
- Companion ocas skills handle adjacent jobs (weather/briefing, planning); this
  skill emits none of that. They are optional companions, not dependencies.

This block is illustrative, not required. A fresh install derives all of it from
Steps 1-4.
