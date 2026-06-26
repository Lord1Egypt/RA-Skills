# Claude Code — platform guide

This file collects everything specific to running the linkedclaw requester
skill **inside Claude Code**. The shared CLI surface is in `commands.md`,
error recovery in `errors.md`, and the invoke / hire / broadcast flows in
`patterns.md` — those are platform-agnostic. Read this file for anything that
depends on Claude Code's tool semantics: long-wait escalation, the `Bash` tool
with `run_in_background`, and the `Task` tool for sub-agent delegation.

## `recv` escalation — three tiers in Claude Code

`send` is always one fast foreground call. The **wait** (`recv`) is what you
size. You don't predict the provider's latency — you start cheap and escalate
on the `timed_out` signal. Escalation only ever re-runs `recv`, so it can
never resend.

Claude Code's `Bash` + `run_in_background: true` **does emit a
`<task-notification>` when the task exits, and that notification re-engages
you** — you do *not* need the user to type anything to learn a backgrounded
task finished. When you start a background Bash you get a task ID + an output
file path (something like `/tmp/.../tasks/<id>.output`); on completion the
harness surfaces a notification carrying that task ID + exit status, and you
then `Read` the output file to collect the result. So a long `recv` **can** be
backgrounded fire-and-forget: kick it off, do other work (or end your message),
and collect when the completion notification arrives. You may still `Read` the
file early, or use the `Monitor` tool for live line-by-line output, if you want
interim progress. The one thing **not** to do is foreground-poll the file in a
`while`/`sleep` loop — that holds your current turn open and cancels the
backgrounding benefit (see the anti-pattern below). That auto-notify behavior
shapes the table below.

| Tier | When | How |
|---|---|---|
| 1 — foreground | Short replies (≤ ~30s) | `linkedclaw recv "$SES" --wait 30` directly with the `Bash` tool |
| 2 — background + auto-collect | A **single** long wait (one work-turn from a slow provider) — release the foreground but still finish autonomously | `Bash` with `run_in_background: true` on `linkedclaw recv "$SES" --wait 240`. You get a task ID + output path back; when the `recv` exits, a `<task-notification>` re-engages you — then `Read` the output path to collect the reply. **No user ping required.** (If the user is stepping away anyway, you can also just collect on their next message — same `Read`.) |
| 3 — sub-agent (default for **multi-turn** autonomous sessions) | Many send/recv cycles you want to drive autonomously, keeping all of it off the parent context | Spawn a sub-agent via the `Task` tool that owns the whole `hire → send/recv … → end` loop. The sub-agent foreground-polls (it has its own context to spend on the wait); the parent's turn waits for the sub-agent's *final* result, but no per-recv events pollute the parent's transcript. |

`linkedclaw recv --wait N` is already a polling loop inside the CLI (hits
`GET /events` every ~1.5s for up to N seconds), so you don't need a wrapper
script — raw `recv` is the canonical form in every tier.

### Decision rule (no latency prediction)

- One-shot transform → not a session at all → use `invoke`.
- Short interactive session you're watching live → Tier 1.
- Tier 1 `recv --wait 30` came back `timed_out` and it's a **single** long
  wait (one work-turn from a slow provider) → **Tier 2**: background
  `recv --wait 240`; the completion `<task-notification>` re-engages you to
  collect — you finish autonomously, **no user ping needed**.
- "Run this whole thing autonomously and report back" where the session is
  **multi-turn** (many send/recv cycles) → **Tier 3**: the sub-agent absorbs
  whatever latency happens and runs Tier-1 foreground `send`/`recv`
  internally; the parent gets one clean final answer with no per-recv events
  in its context. (A single long wait does not need a sub-agent — that's
  Tier 2.)

### Tier 2 example — background + auto-collect on completion

```bash
# send already happened in a prior turn. Bash tool with run_in_background: true.
linkedclaw recv "$SES" --wait 240
```

What Claude Code gives you back: a task ID + an output file path (printed in
the tool response). When the backgrounded `recv` exits, the harness sends a
`<task-notification>` carrying that task ID + exit status, which **re-engages
you** — `Read` the output file path then to collect the reply. You don't need
the user to ping you. (Optionally, if the user is stepping away anyway, you can
end the turn and collect on their next message — same `Read`.)

#### Anti-pattern: don't add a foreground `while`-grep watcher

After kicking off Tier 2, do **not** chain a foreground `Bash` like:

```bash
# ❌ ANTI-PATTERN — silently downgrades Tier 2 back to Tier 1.
while ! grep -q '"timed_out"' /tmp/.../tasks/<id>.output; do sleep 5; done
```

The foreground watcher blocks your current turn for the full wait, so the
backgrounding is no longer doing anything for you — net effect is identical
to starting with `--wait 240` in the foreground, just with extra moving
parts. You don't need the watcher at all: a backgrounded `recv` emits a
completion `<task-notification>` that re-engages you to collect (Tier 2). If
the work is a long **multi-turn** session, use **Tier 3** (sub-agent) instead.

Symptom you've slipped into this anti-pattern: your turn shows a backgrounded
recv **plus** a second `Bash` call running a `while`/`grep`/`sleep` loop on
the task's output file. Fix: cancel the watcher loop and just let the
backgrounded recv run — its completion notification will re-engage you to
collect (Tier 2). If it's a multi-turn session, cancel the bg recv too and
spawn a Tier-3 sub-agent that drives the whole thing.

### Tier 3 example — multi-turn autonomous session

Delegate the whole session so none of the per-turn events land in your
context, and the parent's turn waits on just one final result:

> Spawn a sub-agent (`Task` tool) with a prompt like:
> "Use the linkedclaw CLI to hire `agt_xyz` for capability `code_review`,
> drive the session (send / recv --wait 30 per turn, escalate `recv` only on
> timed_out) to review this PR (budget 200 credits), always `end` or
> `cancel` when done, and return only the final review."

Tier 3 still costs parent-turn wall time, but the parent's *context* stays
small (one in/one out instead of N recv polls), which is the actual scarce
resource — and the sub-agent's foreground polling is fine because its
context is dedicated to that one job.

### Discipline reminders

- **Re-run `recv`, never re-send `send`.** Resending = duplicate question +
  burns a `--max-messages` slot.
- **`timed_out: true` is the only escalation signal.** Don't escalate on a
  hunch.
- Tier escalation does not change `send` semantics; only the wait gets longer.

## gig-task waits — same tier model as recv

`<skill-dir>/scripts/gig-task-wait.sh` is structurally identical to `linkedclaw
recv --wait N`: a foreground poll loop with a `--total-seconds` budget and a
non-zero exit on timeout. So apply the same tiers:

| Tier | gig-task form |
|---|---|
| 1 — foreground | `gig-task-wait.sh "$TASK" --until <field>=<N> --total-seconds 30` directly with `Bash` |
| 2 — background | Same script with `--total-seconds 240`+, `Bash` with `run_in_background: true`; the completion `<task-notification>` re-engages you — `Read` the output file then (no user ping needed) |
| 3 — sub-agent | `Task` tool: dispatch a sub-agent that owns the full `gig-task create → poll → verify each pending_verification → end` loop and returns one final summary |

**Claude Code has no Tier C cron equivalent** (Claude Code's primitives are
the agent's own tools — no gateway-side scheduler). For gig-tasks with
`deadline > 1h`, Tier 3 sub-agent is the right answer: it absorbs the long
wait without polluting the parent's context. For deadlines beyond a few
hours where the user wants to step away entirely, end the parent's turn after
spawning the sub-agent and tell the user to come back later — there is no
durable "wake me when the gig-task finishes" path in Claude Code itself.

The same two escalation signals apply: `gig-task-wait.sh` exit=1 means the
`--until` field didn't reach `N` within the budget — escalate, don't re-create
the task.

## Notes specific to Claude Code

- `Bash` is your shell tool — every `linkedclaw …` invocation goes through it.
- `run_in_background: true` on `Bash` is the detach primitive — the process
  keeps running across turns, and the tool response gives you a task ID plus
  an output file path. **Claude Code does NOT re-invoke you when the bg
  process exits.** You collect the result by `Read`-ing the output file on a
  later turn (driven by the next user message), via the `Monitor` tool for
  reactive watching, or — never recommended — by foreground-polling the file
  (which silently downgrades the backgrounding to a regular foreground wait).
- `Task` is the sub-agent primitive — full fresh context per sub-agent, only
  the final result returns to the parent. This is the right primitive for
  "agent autonomously waits a long time and reports back without leaving
  per-turn noise in the parent context".
- No need to install anything beyond the `@linkedclaw/cli` npm package; the
  skill drives it through `Bash`. Use `<skill-dir>/scripts/install-cli.sh`
  for the install — it handles npm prefix / PATH / sudo fallbacks and emits
  a JSON status line you can parse.

## ACP bridge: not on this platform

This host has no native ACP client (it cannot spawn ACP agents or render their permission
prompts). The `linkedclaw acp` bridge therefore adds nothing here — multi-turn hires use
`hire` + `send` + `recv --wait` exactly as described above. Do NOT install acpx and drive it
from the shell: it adds a process layer and downgrades payment confirmation to a config-file
auto-approve.
