# gmail-wiki-ingest — trigger contract

What starts a run, and why it is an `openclaw cron` job **inside this
container** rather than a server-side poller. (SKILL.md's reference list used to
have this backwards. The poller was designed, then deleted; see "Why not a
server-side trigger".)

## The trigger

An `openclaw cron` job inside this container, registered at skill-install time
by javis-server and reconciled on every default-skills pass
(`app/services/skill_install_service.py::ensure_skill_cron`):

```
openclaw cron add \
  --cron "0 7 * * *" \
  --message "<the fetch → judge → submit → report steps; see below>" \
  --name gmail-wiki-ingest-daily-v3 \
  --agent main \
  --session isolated \
  --no-deliver \
  --tz <the user's IANA zone>
```

**Flags, not positionals.** openclaw's current docs show
`cron add "<expr>" "<prompt>"`. The binary deployed in these containers
(2026.5.12-beta.1) rejects that form and wants `--cron` / `--message`. Check the
installed binary's `cron add --help`, not the repo docs — a cron that fails to
register fails silently: no job, no daily run, no error anyone sees.

| flag | why |
|---|---|
| `--name` | openclaw keys a job by name, so re-registration is a no-op rather than a duplicate. That is what makes the reconcile pass safe to run every sweep — and what makes the name **versioned**: see "Changing the prompt" below. |
| `--agent main` | `cron add` warns and falls back to the default agent when omitted; pinning it keeps the turn in the session that has the skill loaded. |
| `--no-deliver` | A cron job otherwise fallback-delivers the agent's final text to a chat — whatever the turn happened to end on, unformatted. This skill now delivers deliberately instead: `report` POSTs a rendered digest to `/api/agent/push`, which the flag does not touch. So the flag suppresses the agent's raw prose while the formatted message still lands, which is exactly the split this skill wants. Retained, for that reason rather than the original one. |
| `--session isolated` | Keeps the turn out of the user's main chat session, matching every agentTurn job already in a prod `jobs.json`. |
| `--tz` | Cron expressions otherwise run in the container's local zone, which is UTC — "7am daily" would fire at midnight for a Pacific user. Comes from `User.timezone`; omitted entirely when unset, so openclaw's own default applies. |

**The message carries the steps, not just the skill name.** A cron turn is an
isolated session started by openclaw's own timer — no dispatcher has told it
which skill it is — so `"Run the gmail-wiki-ingest skill now."` would lean
entirely on the agent finding this SKILL.md unaided. The only hand-written
ClawSkills cron in production (`calendar-extractor-self`) does not take that
bet: its message spells out `fetch` → extract → `push`. This one spells out the
run's steps, restates the empty-batch rule, and points at SKILL.md, which stays
the authority on the flow and `rubric.md` on the judgment. The exact text lives
in `skill_install_service._SKILL_CRONS` and is pinned by tests.

**The `-v2` message was out of date in the worst direction, and `-v3` is the
correction.** v2 described a three-step run and told the agent the items are
"thread METADATA only … there are no bodies and you must not go looking for
them" — with `content` in the bundle, an instruction not to use the step the
judgment pass is built on. Fixing it could not be a bundle publish: a job's
message is baked in at registration, so the bundle alone reaches nobody. The
server record now carries `"name": "gmail-wiki-ingest-daily-v3"`,
`"legacy_names": ["gmail-wiki-ingest-daily-v2", "gmail-wiki-ingest-daily"]`,
`"min_bundle_version": "0.5.0"` and a five-step prompt with `content` between
the fetch and the judgment.

**Publish order still matters.** `min_bundle_version` gates the registration on
the bundle actually on disk, so a container behind 0.5.0 keeps its v2 job until
its own update sweep catches up — which is the safe direction, and the reason
the bundle must reach ClawHub before anyone expects the new job to appear.

The job is registered whether or not the install step ran this pass: the
install sentinel says the *bundle* is present, which is a different claim from
*the cron exists*. A container recreated from an image has the marker and no
job, and the failure mode of a missing cron is silence.

## Changing the prompt

**A job's message is baked in at registration.** `ensure_skill_cron` skips the
add when a job of the wanted name already exists, so editing the prompt in
`_SKILL_CRONS` reaches new installs only — every already-provisioned container
keeps firing the text it was created with, forever.

That is why the name carries a version. The record holds
`"name": "gmail-wiki-ingest-daily-v3"` plus
`"legacy_names": ["gmail-wiki-ingest-daily-v2", "gmail-wiki-ingest-daily"]` —
every superseded name stays listed, not just the one immediately before it, so
a container dormant since the first rollout still loses its original job — and
the reconcile pass removes any job matching a legacy name **after** adding the
current one, so a failed add cannot leave a user with no job at all. Removal is positional by
job **id** — `openclaw cron remove <id>`, there is no `--name` flag and passing
one errors — so the id comes out of the `cron list --json --all` listing the
pass already fetches.

The upshot for anyone editing the daily prompt: bump the version suffix and push
the old name onto `legacy_names`, or the change silently reaches nobody who
already has the skill. Existing containers converge on their next default-skills
sweep (12h); a dormant user converges when their container next starts.

The v2 prompt is the one that ends in `report`. A container still running the v1
job never calls it, which is harmless — the digest is simply absent — and is
also why the ClawSkills bundle ships before the server change rather than after:
a prompt that calls `report` against a bundle that predates it would fail the
turn's last step every morning. The same ordering applies to the `content`
step: publish the bundle first, then bump the cron to `-v3`, so a prompt that
names `content` never meets a bundle that has no such command.

## Why not a server-side trigger

An earlier revision of this design put the trigger on javis-server — a poller
that called `trigger_skill` for users whose ingest was due. It existed for one
reason: the two candidate calls were openclaw **client tools**, present only in
the `body.tools` of a request javis-server itself makes, and a cron turn gets
no such body. Under that transport a cron job would have fired on schedule and
found no tools, every day, forever.

Moving the calls onto gateway-token HTTP removed the reason. A cron turn can run
a script, and a script can hold `OPENCLAW_GATEWAY_TOKEN`, so the trigger went
back where the schedule belongs — in the container, next to the thing it runs.
`app/workers/gmail_ingest_poller.py` was deleted with it; javis-server now
schedules nothing for this skill.

## What "daily" actually means

**Daily, on the next container start after the job comes due.** The container is
reaped roughly 10 minutes after the user's last activity
(`GATEWAY_IDLE_TIMEOUT`), and cron cannot wake a stopped container. openclaw
catches a missed job up once on its next start (`runMissedJobs` —
`src/cron/service/timer.ts`), not once per skipped day.

**How often that actually is, measured.** On prod (2026-08-30), 16 of ~20
per-user containers were `Exited`, several for 6–8 weeks; only a handful were
`Up`. The one hand-written calendar cron had never fired — its `jobs-state.json`
was frozen at creation three months earlier — while an active user's cron state
had been written that same week. So on any given day this trigger reaches the
users who are already around, and everyone else gets their run on their next
visit rather than on schedule.

That is acceptable here because the sync is bounded by a **content watermark**
(`gmail_ingest_scopes.cursor_epoch`), not by a clock: a late run covers a longer
window and loses nothing. A dormant user finds their ingest waiting when they
come back, which is when they want it. Any feature that must fire at a wall-clock
time cannot use this pattern and needs a server-side sweep instead.

## The on/off switch

`gmail_ingest_scopes.enabled`, the row iOS writes and a Google disconnect
clears. The cron always fires; `fetch` returns `{"error": "disabled"}` when the
scope is off, and SKILL.md's Errors table stops the run there, silently, with
no digest. (A `submit` that lands after a mid-run switch-off answers the same
`disabled`, writes nothing, and the run stops the same way.)

This reverses an earlier trade. `fetch` used to return an ok, empty batch for
a disabled scope, so the empty-batch rule pushed "nothing new" daily — proof of
life, on the theory that an absent message is what a broken sync looks like.
For a user who switched the sync off or disconnected Google it was the
opposite: a daily message about a feature they had ended. Proof of life still
holds for every user whose scope is ON, which is the only case where silence
could mean breakage. javis-server bug doc:
docs/javis-dev/spec/2026-10-02-google-disconnect-leftovers-bug.md, #4b.

## Verifying it

Inside the user's container:

```
openclaw cron list                # the job, its schedule, last/next run
openclaw cron run <job-id>        # force a run without waiting for the schedule
```

Cron state on the DEPLOYED version lives in
`<user-data>/config/cron/jobs.json` (plus `jobs-state.json` for run state and a
`runs/` directory) — verified on prod, where javis-server's `cron_service.py`
reader is therefore correct today.

A newer openclaw moves this into a shared SQLite state database and renames the
legacy file `.migrated` after importing it once. When these containers update,
that reader stops seeing jobs and will need to shell out to `openclaw cron list`
instead. It is a scheduled break, not a current one.
