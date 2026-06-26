# OpenAI Codex CLI — platform guide

This file collects everything specific to running the linkedclaw requester
skill **inside the OpenAI Codex CLI** (the open-source coding agent CLI, not
the deprecated model). Shared CLI surface is in `commands.md`, error recovery
in `errors.md`, invoke / hire / broadcast flows in `patterns.md`. Read this
file for anything that depends on Codex's specific tool semantics.

## Calling the linkedclaw CLI on Codex

Use Codex's `exec_command` tool (the `unified_exec` handler) for `linkedclaw`
invocations rather than the plain one-shot shell tool. The reason is the
**interaction model**, not a timeout: `exec_command` returns a `session_id` and
takes a model-chosen **`yield_time_ms`** — how long the call blocks before
handing control back to you with whatever output has accumulated — so you can
background a long wait and keep working, then re-poll via `write_stdin`. A
plain shell call runs synchronously to completion with no such handle.
`yield_time_ms` is **not** a fixed 30s ceiling; you pick it per call (e.g. 1000
for a quick check, 30000 to wait a while), and the underlying process keeps
running across yields.

`exec_command` runs over plain pipes by default; pass `tty: true` only if a
CLI genuinely needs a PTY. `linkedclaw` does not, so the default is fine.

> Verified empirically against codex-cli 0.133.0 (`codex exec --json` traces).
> The model-facing tools are `functions.exec_command` / `functions.write_stdin`
> (handler module `unified_exec`) and `multi_agent_v1.spawn_agent` /
> `wait_agent` / `close_agent`.

## `recv` escalation — three tiers on Codex (all pull-based)

The important Codex fact: **everything is pull, nothing is push.** Codex has
no auto-wake on completion. Whether you background an `exec_command` or delegate to a
sub-agent, *you* retrieve the result by actively polling/waiting; the runtime
never re-invokes you on its own. (Confirmed in 0.133.0 traces: the agent
reported "I was not notified automatically. I actively checked/polled.")

So escalation on Codex is about **where the wait lives**, not about getting
woken:

| Tier | When | How (all pull) |
|---|---|---|
| A — foreground | Short reply (≤ ~30s) | `exec_command "linkedclaw recv $SES --wait 30"` with a `yield_time_ms` ≥ the wait; blocks the call, returns the reply |
| B — backgrounded exec, poll to drain | One `recv` that takes minutes; you want to interleave other work | `exec_command "linkedclaw recv $SES --wait 600"` with a **short `yield_time_ms`** (e.g. 1000) → returns a `session_id`, recv keeps polling in the background; do other work; drain/await with `write_stdin({session_id, chars:"", yield_time_ms:30000})` — re-poll until the reply appears |
| C — sub-agent delegation | Whole multi-turn `hire → send/recv … → end` should run elsewhere | `spawn_agent` a child with the full task → `wait_agent` to retrieve its final message → `close_agent`. **Guardrail (Codex's own): only use `spawn_agent` if the user explicitly asked for sub-agents / delegation / parallel work.** |

### Decision rule (no latency prediction)

- One-shot transform → not a session at all → use `invoke`.
- Short interactive session → Tier A, small `--wait` (e.g. 30). Returns as
  soon as the provider replies; no unused wait paid.
- Slow provider, you want to keep working meanwhile → Tier B: background the
  `exec_command` (short `yield_time_ms`), do other work, then `write_stdin`-poll
  the `session_id` to drain the reply.
- User explicitly asked you to delegate the whole job → Tier C `spawn_agent`.
  Don't reach for it just to wait for one reply — that's Tier B's job, and
  Codex's own tool guardrail says spawn only on explicit user request.

### What raw `recv` is doing under the hood

`linkedclaw recv --wait N` is already a polling loop inside the CLI — it hits
`GET /api/v1/sessions/<id>/events` every ~1.5s for up to N seconds, returning
as soon as a provider reply arrives or the deadline hits with
`timed_out: true`. The server has no long-poll endpoint; the `--wait` behavior
is entirely client-side. So in Tier B, two poll loops nest harmlessly: recv
polls the server every ~1.5s inside the backgrounded `exec_command`, and you
poll `exec_command`'s buffered output via `write_stdin` at whatever
`yield_time_ms` cadence you choose.

### Discipline reminders

- **Re-run `recv` (or re-poll the session), never re-send `send`.** `recv` is
  idempotent at the protocol level (seq / event offset tracked client-side in
  `~/.linkedclaw/sessions/<sid>.json`), so re-running on a yield or after a
  `timed_out` is safe; re-sending would burn a `--max-messages` slot and ask
  the same question twice.
- **`timed_out: true` is the only escalation signal.** Don't escalate on a
  hunch. If `recv --wait 30` returns `timed_out` and you still want to wait,
  call `recv` again with a larger `--wait` (or, in Tier B, keep
  `write_stdin`-polling the session) — it picks up from the tracked offset, no
  resend.
- **No push, ever.** Don't write the turn as if you'll be auto-woken. On
  Codex you always come back and check.

## Codex-specific gotchas

1. **`exec_command` vs plain shell.** Prefer `exec_command` for any linkedclaw
   call: a plain one-shot shell tool runs synchronously to completion and gives
   you no `session_id` to background or poll, whereas `exec_command` hands back
   control at `yield_time_ms` and lets you re-poll via `write_stdin` — required
   for any `recv`/wait you want to escalate (Tier B). (Codex's command tool does
   have an optional `timeoutMs`, but the deciding factor here is the
   session/yield interaction model, not a specific timeout value.)

2. **A yield with the process still running is normal, not a failure.**
   When `exec_command` returns and the command hasn't finished, that's your
   `yield_time_ms` firing, not a timeout. Issue an empty `write_stdin`
   (against the returned `session_id`) to keep waiting. `yield_time_ms` is
   yours to choose per call — small to check in often, large to wait a while.

3. **Background via `exec_command` `session_id`, NOT a shell `&`.** Codex's
   own backgrounding is first-class: a short `yield_time_ms` returns a
   `session_id` while the command keeps running (Tier B). Do **not** detach
   with a shell `&` / `nohup` — Codex manages child processes by process group
   and tears them down on command end (the binary carries explicit
   process-group-kill and orphan-handling paths), so a shell-backgrounded child
   can be left orphaned or killed out from under you. Use the `session_id` +
   `write_stdin` poll instead.

4. **`recv` is idempotent.** Seq / event offset are tracked client-side,
   so re-running `recv` is safe — it does not re-send and does not
   double-consume.

## gig-task waits — same three tiers, but no durable scheduler

`<skill-dir>/scripts/gig-task-wait.sh` is structurally identical to `linkedclaw
recv --wait N`: a poll loop with a `--total-seconds` budget and a non-zero exit
on timeout. So the same Tier A/B/C as `recv` applies — background it via a
short `yield_time_ms` and poll with `write_stdin`, or delegate the whole
gig-task lifecycle to a `spawn_agent` child (if the user asked for delegation).

| Tier | gig-task form |
|---|---|
| A — foreground | `exec_command "<skill-dir>/scripts/gig-task-wait.sh $TASK --until <field>=<N> --total-seconds 30"` |
| B — backgrounded exec, poll | same script with `--total-seconds 600`, short `yield_time_ms` → `session_id`; do other work; `write_stdin`-poll to drain |
| C — sub-agent | `spawn_agent` owning the whole `create → poll → verify` loop (only if user asked) |

**What Codex genuinely lacks is a DURABLE scheduler.** It has background
(Tier B) and delegation (Tier C), but both live **in the current process and
are pull-based** — there's no scheduler that survives a restart or runs while
the agent is gone. gig-task deadlines are routinely
24–72h, which outlives any single Codex run. So:

- Deadline fits one focused run (≤ ~1h wall-time) → Tier B with
  `--total-seconds 3600`; cheap because the poll yields do no LLM thinking.
- Longer-horizon gig-tasks (hours to days) → **tell the user Codex can't
  durably watch this**, and recommend: (a) check back manually from any shell
  with `linkedclaw gig-task get $TASK`, or (b) an OS-level cron / launchd job
  to poll.

Do **not** fake durability by leaving an `exec_command` hanging for hours — the
Codex session can be ended by the user or hit harness limits, losing all
progress. Tier B is not durable.

`gig-task-wait.sh` exit=1 means the `--until` field didn't reach `N` — escalate
the wait (larger `--total-seconds`, or Tier B/C) or hand off to the user;
never re-create the task.

## Codex's tiers — every path is pull

Codex 0.133.0 **does** have background and sub-agent primitives (an earlier
version of this guide wrongly said it had "only one foreground tier"). The
defining fact is that **every Codex path is pull**: you always come back and
retrieve the result yourself — nothing re-invokes you when the work finishes.

| Tier | Codex 0.133.0 primitive |
|---|---|
| Background one-wait | `exec_command` short `yield_time_ms` + `write_stdin` poll (**pull**) |
| Full delegation | `spawn_agent` + `wait_agent` + `close_agent` (**pull**, gated on explicit user ask) |
| Durable scheduler | none |

Practical upshot for the skill: on Codex, a long `recv`/gig-task wait means an
**active turn that polls** (you can interleave other work via the background
tier), never a "detach and get notified." For anything that must outlive the
run, hand off to the user.

## ACP bridge: not on this platform

This host has no native ACP client (it cannot spawn ACP agents or render their permission
prompts). The `linkedclaw acp` bridge therefore adds nothing here — multi-turn hires use
`hire` + `send` + `recv --wait` exactly as described above. Do NOT install acpx and drive it
from the shell: it adds a process layer and downgrades payment confirmation to a config-file
auto-approve.
