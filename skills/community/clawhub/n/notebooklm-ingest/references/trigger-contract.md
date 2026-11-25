# notebooklm-ingest — trigger contract

What starts a run, and why the schedule is an `openclaw cron` job **inside this
container** registered by the skill itself rather than by javis-server.

## The trigger

```
openclaw cron add \
  --name notebooklm-ingest-daily-v2 \
  --cron "<the expression the USER chose>" \
  --message "<the run's steps; scripts/cron.js MESSAGE>" \
  --agent main \
  --session isolated \
  --no-deliver \
  --tz "<the user's IANA zone>"
```

Built by `scripts/cron.js`'s `buildCronAdd`, which is the **only** constructor
for this argv, and run by `scripts/notebooklm-ingest.js schedule`.

### Why the skill registers its own cron

`gmail-wiki-ingest`'s job is registered **server-side**, from a fixed
`_SKILL_CRONS` record in
`javis-server/app/services/skill_install_service.py:139`, and reconciled on
every default-skills pass. That works because its schedule is a constant: 7am,
for everyone.

R13 asks for a schedule the **user** picks. A user-chosen expression cannot live
in a server-side constant, so the registration has to happen where the choice is
made — in the container, next to the thing it runs. No other skill in ClawSkills
does this today; the only in-house precedent for the argv is
javis-skill-creator's `buildCronAdd`, which is not vendored here, so its rules
are carried across explicitly in `cron.js` and pinned by `test/cron.test.js`.

### Flags, not positionals

openclaw's current docs show `cron add "<expr>" "<prompt>"`. **The binary
deployed in these containers (2026.5.12-beta.1) rejects that form** and wants
`--cron` / `--message`. Check the installed binary's `cron add --help`, not the
repo docs — a cron that fails to register fails silently: no job, no scheduled
run, no error anyone sees.

`--schedule` and `--command` are not openclaw cron flags at all. `cron.js`
refuses to emit them and refuses to accept them smuggled in through any option.

| flag | why |
|---|---|
| `--name` | openclaw keys a job by name, so a re-register under the same name is a no-op rather than a duplicate. That is also what makes the name **versioned** — see below. |
| `--cron` | the expression. Required: there is no defaultable "daily", and guessing an hour would schedule a run the user never agreed to. |
| `--message` | the turn's instructions. A cron turn is an isolated session openclaw's own timer started — no dispatcher has told it which skill it is — so `"Run the notebooklm-ingest skill"` would lean entirely on the agent finding SKILL.md unaided. The message spells out `doctor` → the selected notebooks → `notes` → `fetch` → `push` → `report`, restates the always-report rule, and points at SKILL.md, which stays the authority on the flow. **`fetch` reads its note ids from stdin**, so the message shows the `echo … | fetch` form: `-v1` said only "run fetch", which refuses with `bad_input` and made the daily job a silent no-op. |
| `--agent main` | `cron add` warns and falls back to the default agent when omitted; pinning it keeps the turn in the session that has the skill loaded. |
| `--session isolated` | keeps the turn out of the user's main chat session, matching every agentTurn job already in a prod `jobs.json`. |
| `--no-deliver` | a cron job otherwise fallback-delivers the agent's final text to a chat — whatever the turn happened to end on, unformatted. This skill delivers deliberately instead: `report` POSTs a rendered digest to `/api/agent/push`, which the flag does not touch. So the flag suppresses the raw prose while the formatted message still lands. |
| `--tz` | cron expressions otherwise run in the container's local zone, which is UTC: "7am daily" would fire at midnight for a Pacific user. Omitted entirely when the zone is unknown, so openclaw's own default applies rather than an empty value. |

### Changing the message

**A job's message is baked in at registration.** Editing `MESSAGE` in a later
bundle reaches **new** registrations only; every container that already has the
job keeps firing the text it was created with, forever.

That is why `JOB_NAME` carries a version suffix and `LEGACY_NAMES` sits beside
it. To change the message: bump the suffix, push the old name onto
`LEGACY_NAMES`, and publish. `notebooklm-ingest-daily-v1` is already on that
list — its message ran `fetch` with nothing on stdin, so a container still
holding it fires a job that cannot ingest anything. `planRegistration` then adds the current job
**first** and removes the legacy ones **after**, so a failed add can never leave
a user with no job at all. Every superseded name stays listed, not only the one
immediately before it, so a container dormant since the first rollout still
loses its original job.

A **schedule** change on the same name is the one case that removes first: openclaw
keys by name, so an add under an existing name is a no-op and the old job has to
go before the new expression can land. `planRegistration` returns that removal
as `replace`, separately from the legacy `remove`, so the ordering is visible
rather than implied. After a `replace` the right check is `openclaw cron list` —
and `cron_failed` says so, rather than claiming the schedule is set.

### Removal

**Positional, by job id**: `openclaw cron remove <id>`. There is no `--name`
flag and passing one errors, so the id comes out of the
`cron list --json --all` listing `schedule` already fetches.

## On demand (R22)

The on-demand path **never touches the cron job**. Nothing in
`notebooks`/`notes`/`fetch`/`push`/`report`/`history` builds an argv from
`cron.js`, and `test/cli.test.js` asserts it by counting openclaw spawns across
the whole flow. A user who asks "fetch my notebooklm now" gets a run; their
schedule is exactly where it was afterwards.

## What "daily" actually means

**Daily, on the next container start after the job comes due.** The container is
reaped roughly 10 minutes after the user's last activity
(`GATEWAY_IDLE_TIMEOUT`), and cron cannot wake a stopped container. openclaw
catches a missed job up once on its next start (`runMissedJobs` —
`src/cron/service/timer.ts`), not once per skipped day.

On prod (measured 2026-08-30) 16 of ~20 per-user containers were `Exited`,
several for 6–8 weeks. So on any given day this trigger reaches the users who are
already around, and everyone else gets their run on their next visit.

**That is acceptable here, and the reason is specific.** A late run reads the
notes as they are now, and a note's content hash is what decides whether
anything is written — so a run that is a week late ingests the same thing a
punctual one would have, minus the intermediate edits. Nothing is lost by
waiting; what is lost is only the freshness the user did not see anyway because
they were not using the app. Any feature that must fire at a wall-clock time
cannot use this pattern and needs a server-side sweep instead.

## Why not a server-side trigger

Two reasons, and either alone would settle it.

1. **The schedule is the user's** (R13), and a server-side `_SKILL_CRONS` record
   holds one expression for everyone.
2. **The transport would not survive it.** An earlier shape of this design had
   the agent call server-injected tools. Those are `_LOCAL_TOOL_REGISTRY`
   entries javis-server injects as `body.tools`
   (`app/services/openclaw_service.py:340-383`), and **an `openclaw cron` turn is
   started by openclaw's own timer with no `body.tools` at all**. Under that
   transport a cron job would have fired on schedule and found no tools, every
   day, forever. `gmail-wiki-ingest`'s own trigger contract documents exactly
   this, and it is why that skill uses `POST /api/agent/push`.

**The consequence for this skill, stated plainly:** `chat_emit_action_buttons`
and `chat_emit_success_card` exist **only** on an on-demand turn that
javis-server dispatched. On the scheduled path they are absent, and `report` is
the only way the run can say anything. A scheduled run that skips `report` is a
silent run, which is the design's anti-goal.

## Verifying it

Inside the user's container:

```
openclaw cron list                # the job, its schedule, last/next run
openclaw cron run <job-id>        # force a run without waiting for the schedule
```

Cron state on the deployed version lives in `<user-data>/config/cron/jobs.json`
(plus `jobs-state.json` for run state and a `runs/` directory). A newer openclaw
moves this into a shared SQLite state database and renames the legacy file
`.migrated` after importing it once; when these containers update, any reader of
the file stops seeing jobs and will need to shell out to `openclaw cron list`
instead. It is a scheduled break, not a current one.
