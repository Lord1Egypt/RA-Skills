---
name: job-heartbeat
description: Dead-man's switch for cron jobs and recurring tasks via the hosted AO Job Heartbeat API. One check per task, ping only after success, alert when late.
homepage: https://beat.austinoaksapi.com/
metadata: {"openclaw": {"emoji": "⏰", "homepage": "https://beat.austinoaksapi.com/", "primaryEnv": "JOB_HEARTBEAT_API_KEY", "requires": {"env": ["JOB_HEARTBEAT_API_KEY"], "bins": ["python3"]}, "envVars": [{"name": "JOB_HEARTBEAT_API_KEY", "required": true, "description": "API key for the hosted AO Job Heartbeat service (starts with ak_). Needs an AO Job Heartbeat account that the human creates at https://beat.austinoaksapi.com/ (free plan; the service also sells an optional paid plan, see Costs and accounts). The human sets the key outside the chat. The skill never prints it."}]}}
---

# AO Job Heartbeat

AO Job Heartbeat is a hosted dead-man's switch run by Austin Oaks Solutions.
You create a **check** for a recurring task. The task calls the check's ping
URL each time it finishes successfully. If no ping arrives within the period
plus the grace, the service records a late event and alerts the account's
email (once the address is confirmed) and, on the paid plan, its webhooks.

This is **not** OpenClaw's built-in heartbeat (the scheduled agent turn). This
skill watches a recurring job from the outside.

## When to use this

- The human wants to know when a cron job, backup, scheduled script or
  recurring task did not run, or did not finish successfully.
- The human wants to see, inspect or remove their existing checks.

Do not use it for OpenClaw's own heartbeat settings, for website uptime
checks (this service does not poll anything; it waits for pings), or for
one-off tasks.

## Costs and accounts

The service is separate from OpenClaw and ClawHub. It needs an account and an
API key.

| Plan | Price | Checks | Alerts |
|---|---|---|---|
| Free | $0 | 10 | email, after the human confirms their email address |
| Paid | $7 a month | 100 | email and webhooks |

Both plans keep a 30-day event log. Alerts are email and webhooks only. This
skill is free. It has no signup, upgrade or payment command.

## Setup (the human does this, not you)

1. The human creates a free account in their own browser at
   https://beat.austinoaksapi.com/. The API key is shown **once**. They save it
   in their password manager.
2. The human opens the confirmation email and presses "Confirm my email".
   Alert email stays off until then. Tell them to check Junk too.
3. The human sets `JOB_HEARTBEAT_API_KEY` in the environment OpenClaw runs
   in. They do this outside the chat.
4. You run `account` to confirm the key works and to see the plan.
5. The sign-up form on the website also creates a first monitor, and it
   starts timing at once. Run `list`. Reuse that check for the job it was
   made for, or, with the human's yes, delete it. Do not leave it unpinged:
   it goes late, can send a false alert, and uses a plan slot.

Never sign up on the human's behalf unless they explicitly tell you to. Even
then, this skill has no signup command, on purpose: the key is shown once and
would pass through this chat and its logs. Explain that and point them to the
page above.

Never ask for the key in chat. Never print, echo, log or write it, and never
put it in a file, a check name, a crontab or a ping line. If the human pastes
a key into the chat anyway, do not repeat it. Tell them to replace it: the
"Lost your API key?" link on the website sends a recovery link that turns off
every old key and shows one new key.

## Commands

Run the helper with `python3 {baseDir}/scripts/jobhb.py <command>`.
Output is JSON, except `snippet`.

| Command | What it does | Needs the key |
|---|---|---|
| `account` | plan, `email_verified`, checks in use and allowed | yes |
| `list` | all checks: id, name, status, period, grace, last ping | yes |
| `get ID` | one check | yes |
| `create --name N --period P [--grace G]` | one new check (refuses if the plan is full or the name exists) | yes |
| `delete ID --confirm` | cancel a check, only after the human said yes | yes |
| `ping ID` | sign of life, only after the task succeeded | no |
| `fail ID` | the task knows it failed: mark the check failed now | no |
| `events ID` | recent late and recovered events, with delivery results | yes |
| `snippet ID` | prints (does not run) a ping line for the human's own job | no |

Periods and grace accept seconds or a unit: `300`, `15m`, `1h`, `1d`.
Exit codes: 0 ok, 2 bad input, 3 refused, 4 API or network error, a timeout
or an answer that cannot be read (for `ping` and `fail`: not confirmed; the
message says whether it is unknown or did not count), 5 key missing,
malformed or not accepted, 6 not counted (`ping` or `fail` answered
`"ok": true` with `"dropped": true`, or refused with HTTP 429). The helper
never retries and never sends a call twice.

## Create one check per recurring task

1. Run `account`. If the checks in use already equal the limit, stop and
   tell the human.
2. Run `list`. If a check for this task already exists, reuse it.
3. Pick a short **name** for the task. The service stores it and includes it
   in alerts, so leave out secrets and personal data.
4. **Period** = how often the task is scheduled (60 seconds to 30 days).
5. **Grace** = how late is still fine (0 to 30 days). Make it at least as long
   as the task's finish time can vary, plus some slack. If you leave it out,
   the helper uses the same defaults as the service's sign-up page:

   | Period up to | Default grace |
   |---|---|
   | 5 minutes | 1 minute |
   | 15 minutes | 2 minutes |
   | 1 hour | 5 minutes |
   | 6 hours | 15 minutes |
   | longer | 30 minutes |

6. Run `create`. Example for a nightly backup that can take up to 40 minutes:
   `python3 {baseDir}/scripts/jobhb.py create --name nightly-backup --period 1d --grace 1h`

The check is armed the moment it is created. The first ping must arrive
within period + grace (the output shows `first_ping_due_by`). After each
ping, the next one is due one period after that ping, plus grace.

## Ping only after the task succeeded

1. Before you wire up the ping, write down the task's own success
   conditions. Examples: exit code 0, the output file exists and is not
   empty, the expected number of rows arrived.
2. Ping **only** when all of them hold, as the very last step:
   `python3 {baseDir}/scripts/jobhb.py ping ID`
   - Exit 0: the ping counted. The service answered HTTP 200 with
     `"ok": true` and `"dropped": false`, and nothing less counts.
   - Exit 6: the ping was dropped and did **not** count; the deadline did
     not move. More than 10 calls a minute usually means duplicate pings or
     a shared URL.
   - Exit 4: the ping was not confirmed. The message says why: for example a
     timeout (the request may or may not have reached the service), a
     server error, or no such check. If it did not count, the deadline
     catches it.
   - After exit 4 or 6: Do not send it again automatically, and never in a
     loop. Tell the human what the message says.
3. If the task clearly failed, do not ping. Either run `fail ID` so the
   service records a late event now (then check `events ID` for what was
   delivered), or do nothing and let the deadline catch it. If `fail` exits
   4 or 6, the same rule applies: do not send it again automatically; tell
   the human.
4. Never ping on a timer, from a failure branch, or "to keep it green". A
   ping that does not mean "the work succeeded" makes the check useless.

For the human's own cron or shell jobs, run `snippet ID` and give them the
printed line, with its comments. It is one line, used once, in place of the
job's current command, and it runs the job once. It pings only when the job
exits successfully, and it exits 0 only when the service confirms the ping
counted (HTTP 200, `"ok": true`, `"dropped": false`, an unchanged body that
is valid UTF-8 JSON, and no key repeated in any object). After a failure it
reports the failure at once and keeps the job's own exit code. It never
retries, and it reads no curl config file. When the job succeeded but the
ping was not confirmed, it exits 75 (curl failed: a timeout, a network
error, or curl missing or too old; the ping may not have counted) or 76 (the
answer did not confirm it: dropped, an error or unreadable). It then prints
a `job-heartbeat:` message on stderr; a job that itself exits 75 or 76 looks
the same except for that message. A failure report that is not confirmed
also prints that message, and the line still exits with the job's own code.
It uses `GET /ping/{id}` and `GET /ping/{id}/fail`, and needs `sh`, `curl`
7.54 or newer and `python3` on the machine that runs the job.

The job command must be ONE command or a script path: no pipe (only the
pipe's last command decides success), no trailing `&`, and no `#` comment.
The printed comments give the most bytes the command may have, because
macOS cron keeps only 999 bytes of a crontab command (it counts bytes, not
characters: a plain ASCII character is 1 byte, others take 2 to 4); a line
cut short, or one with a `#` comment, does not run at all. If the command is
longer or is a pipe, tell the human to put it in a script and use the
script's path. Do
not split the line into two lines or two schedule entries: the job would run
twice. It contains no API key. This skill never edits a crontab or any other
scheduler; the human adds the line.

For a recurring task that you run yourself, the ping is the final step of
that task, after you have checked its success conditions. Add it only when
the human asks for monitoring of that task.

The ping URL needs no key, but anyone who has it can ping that check. They
can also call its `/fail` address with no key. That marks the check failed,
sends alert email and uses up the account's daily email allowance, which can
hold back real alerts. Keep the URL out of public places. Pings and fails
together are limited to 10 a minute per check; extra calls answer with
`"dropped": true` and do not count. The helper then exits 6. The printed
line exits 76 after a successful job, or keeps a failed job's own exit code,
with a `job-heartbeat:` message either way.

## List, inspect and delete

- `list` and `get ID` show each check's status: `new` (armed, never pinged),
  `up` (pinged in time), `late` (no ping within period + grace), `failed`
  (`fail` was called) or, from `get` only, `deleted` (the check was
  cancelled; its event log stays readable).
- `events ID` shows the recent `check.late` and `check.recovered` events and
  what happened to each delivery.
- `delete ID --confirm` cancels a check. Ask the human first, naming the
  check. Afterwards, remind them to remove the ping step from the job. The
  30-day event log stays readable.

## Plan limits

- Never create more checks than the plan allows. The helper checks the count
  first and refuses. If the service answers `402 PLAN_LIMIT`, stop.
- Do not delete checks to make room unless the human says so.
- Never start an upgrade, a checkout or any payment. If the human wants more
  checks or webhooks, they decide on the website themselves.

## Honest reporting

- `up` means the job checked in. It does not prove that alerts work.
- `email_verified: true` means alert email is switched on. It does not mean
  an alert will reach the Inbox.
- **Known limit (as of 2026-09-30):** alert emails to Microsoft, Outlook and
  Hotmail addresses have been landing in Junk. Tell those users to check
  Junk and to mark the message as not junk. Treat this as unsolved.
- In `events`, an email delivery with `ok: true` means the service's mail
  step reported success. Nothing here can see the human's Inbox.
- The service also caps alert emails per account per day
  (`alert_emails_per_day` in `account`).
- In `events`, an email entry with `skipped: email_unverified` means no
  email was sent, because the address is not confirmed. An event with no
  email entry at all (for example `delivery: []`) means no email was sent
  for it, usually because the daily cap was used up. `pending: true` means
  delivery has not finished; look again later.
- `fail` answers only whether a late event was recorded. It does not show
  what was delivered; check `events ID`.
- If the helper shows a field as `null`, or exits 4 saying the answer could
  not be read, the service did not say. Report it as unknown.
- Never tell the human an alert reached them. Say what the service recorded,
  for example: "The service recorded a late event and reports the email step
  as successful. Please check your Inbox and Junk."
- If the helper cannot reach the service, say the state is unknown. Do not
  guess.

## Seeing a real alert (optional, the human decides)

If the human wants to see an alert arrive, and a check slot is free: run
`account` first (no email is sent unless `email_verified` is true), create a
test check, run `fail ID` on it, then run `events ID` to see what the
service recorded, and ask them to look in Inbox and Junk. Then, with their
yes, delete the test check. You cannot see whether the email arrived; only
the human can.

## Permissions and data

- **Network:** only `https://beat.austinoaksapi.com`. The host is fixed in the
  helper; no setting or flag changes it. System proxy settings are ignored
  and redirects are refused.
- **Routes used:** `GET /v1/account`, `GET /v1/checks`, `GET /v1/checks/{id}`,
  `POST /v1/checks`, `DELETE /v1/checks/{id}`, `GET /v1/checks/{id}/events`,
  `GET /ping/{id}`, `POST /ping/{id}/fail`.
- **Data sent:** the API key in the `Authorization` header (account and
  check routes only); the check id in the URL; for `create`, only `name`,
  `period_s` and `grace_s`. `ping` and `fail` send no key and no body. Every
  request carries `User-Agent: job-heartbeat-skill/1.0.0` and
  `Accept: application/json`; `create` adds `Content-Type: application/json`.
  The service also sees the caller's IP address.
- **Data shown:** plan, `email_verified`, check counts, check details and
  event results. The account's email address is not shown.
- **Environment:** reads `JOB_HEARTBEAT_API_KEY` only. It refuses to send a
  value that does not start with `ak_`.
- **Local system:** writes no files and keeps no state. It never edits a
  crontab, creates scheduled tasks, starts other programs, runs shell
  commands from strings or asks for elevated privileges. `snippet` prints a
  shell line that uses `curl` and `python3` for the human's own job; the
  skill itself never runs that line.

## Removing it

1. With the human's yes, run `delete ID --confirm` for each check they no
   longer want.
2. The human puts each job's own command back in place of the printed line
   (or removes the ping step from a task).
3. The human removes `JOB_HEARTBEAT_API_KEY` from the environment.
4. Remove this skill's folder. This skill does not close the account.

## Do not

- Do not sign up, log in, upgrade, start a checkout or handle payment.
- Do not ask for, show, store or log the API key.
- Do not create more checks than the plan allows, or a second check for the
  same task.
- Do not ping before the task's success conditions hold.
- Do not edit crontabs or schedulers; print the line for the human.
- Do not send requests to any host other than `beat.austinoaksapi.com`.
- Use only the helper. Do not call the service API directly, and do not call
  routes the helper does not use: webhook targets, email change,
  confirmation resend, key recovery or billing. Webhook targets, email
  changes and key recovery are for the human to do themselves.
- Do not claim an alert reached the human.
