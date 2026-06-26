# Stages — pre / poke / post

Every poke has up to three stages. Each stage is independently either a
**command** (argv, no shell) or an **agent-prompt** (handed to an agent).

```bash
poke --remind "check server" --once 1h \
  --pre-cmd "systemctl start myapp.service" \
  --post-task "Verify myapp is healthy and report any anomalies." \
  --channel CH --target TGT
```

- `--pre-cmd CMD` — argv command before delivery
- `--post-cmd CMD` — argv command after delivery
- `--pre-task PROMPT` — agent-prompt before delivery; delivered to the
  origin channel/target captured at create time
- `--post-task PROMPT` — agent-prompt after delivery
- `--on-pong-command CMD` — argv command when the user replies (any of
  confirm / cancel / snooze / followup)
- `--hook-env VAR` — opt a parent env var into the hook's environment
  (repeatable, e.g. `--hook-env API_TOKEN --hook-env HASS_URL`)

## Argv parsing (`--pre-cmd` / `--post-cmd` / `--on-pong-command`)

Either form works:

- **JSON array** (explicit, recommended for anything with quoting):
  `--pre-cmd '["systemctl","start","myapp.service"]'`
- **Whitespace-tokenized string** (friendly, with `'`/`"` quotes):
  `--pre-cmd "systemctl start myapp.service"`

No `$VAR` expansion, no pipes, no redirects. If you need any of those,
write a script and pass its path.

Each hook invocation gets these env vars: `POKE_HOOK`, `POKE_ID`,
`POKE_TEXT`, `POKE_AGENT`, `POKE_CHANNEL`, `POKE_TARGET`,
`POKE_ORIGIN_CHANNEL`, `POKE_ORIGIN_TARGET`, `POKE_COUNT`,
`POKE_REPLY_ACTION`, `POKE_STATE_FILE`.

Hooks run with a **minimal environment**, not the full parent `process.env`:
only `PATH`, `HOME`, `USER`, `LOGNAME`, `SHELL`, `LANG`, `LC_ALL`, `TZ` are
passed through, plus the `POKE_*` vars above. This keeps ambient secrets and
tokens out of hook subprocesses. If a hook genuinely needs a parent var, opt
it in explicitly with `--hook-env VAR` (repeatable). Even so, only configure
hooks with scripts you wrote or explicitly trust.

Stdout/stderr/exit code go to `.runtime/hook-log.jsonl` per call. A
failing hook does NOT stop delivery.

## Design principle — pokes vs scripts

**Agent-prompts are for *content* (deciding what to say, what to check).
Scripts are for *side-effects* (LEDs, audio, services, anything
continuous or smoothly timed).**

A reminder that pokes every 30 seconds to nudge the user does NOT also
drive a 5-minute LED fade — that fade belongs in a script the pre-stage
launches once. Pokes can't be smooth: each fire is a discrete event
spaced minutes apart, and an agent-prompt fire takes seconds of
cold-start latency. Anything that needs frame-rate or sub-second timing
belongs in a long-running script.

The shape:

- **`--pre-cmd`** launches the side-effect script *once* per cycle (fires
  on the first delivery; re-arms on recurring cycle advance so a daily
  reminder runs the script fresh every morning).
- **main `--remind` / `--task`** does the user-facing nudging, escalates
  if no reply.
- **`--on-pong-command`** fires once on the first reply, kills the
  side-effect script.

## Hooks block — scripts must self-daemonize

`--pre-cmd` runs via `execFileSync` with no shell. The hook waits for
the child to exit. So a script that needs to outlive the hook must
self-daemonize (e.g. `setsid` + write a PID file) and exit its parent
process quickly. Don't put `&` in the argv — there's no shell to
interpret it. Either daemonize from inside the script, or write a tiny
wrapper that does the daemonization.

## Canonical pattern — wake-up light

User: "remind me to get up at 7, fade my bedroom lights up smoothly
until I'm awake, stop when I reply."

```bash
poke --remind "Time to get up." \
  --on-calendar 'Mon..Fri *-*-* 07:00:00' \
  --pre-cmd '["/home/USER/sh/wake-light-fade.sh","--start"]' \
  --on-pong-command '["/home/USER/sh/wake-light-fade.sh","--stop"]' \
  --escalation-intervals '5,5,5,5,5' --max-pokes 6 \
  --channel matrix --target user:1
```

What happens:

1. **07:00 Mon–Fri** — base occurrence fires. `--pre-cmd` runs once
   (gated by `pre_fire_fired`, which resets only on cycle advance, not on
   escalation pokes). The script daemonizes, writes its PID (e.g. to
   `/tmp/wake-light.pid`), and runs its own smooth ramp loop.
2. **Same fire** — reminder text goes to matrix.
3. **Every 5 minutes** — escalation poke fires (up to 6 total). LEDs do
   NOT get touched by these pokes — that's the script's job.
4. **User replies anything** ("done", "ok", "later", "stop") — the
   classifier hits one of the four intents, the cycle ends, and
   `--on-pong-command` fires `wake-light-fade.sh --stop`.
5. **Tomorrow morning 07:00** — `clearCycleState` already re-armed
   `pre_fire_fired` when the reply came in, so the script launches
   again fresh.

The `wake-light-fade.sh` script needs to:

- On `--start`: self-daemonize (`setsid bash -c '…' &`, or re-exec with
  a flag meaning "you're the child now"), write its PID to a known path,
  then run the ramp loop. The parent must exit quickly so the hook
  returns.
- On `--stop`: read the PID file, `kill` it, remove the PID file.
  (Avoid the `pkill -f wake-light-fade` shortcut — `-f` matches any process
  whose command line contains that string, which can kill unrelated
  workloads. Use the PID file unless you control the entire process
  namespace.)

## Anti-patterns

- ❌ **LED ramp inside a `--task` prompt.** Re-spawns a cold agent on
  each escalation tick — 5–30s of latency per step. Nowhere near smooth.
- ❌ **Sub-minute `--escalation-intervals` to drive a fade.** Intervals
  are in minutes; OS scheduler jitter ruins smoothness even at finer
  grain.
- ❌ **Synchronous LED ramp inside `--pre-cmd`.** The hook blocks until
  the child exits, so the reminder text would only go out *after* the
  fade finished.

## Stage migration — old `--pre-fire` / `--post-fire` gone

The old `--pre-fire CMD` / `--post-fire CMD` (single-string, shell-run)
flags were removed. Use `--pre-cmd` / `--post-cmd` (argv, no shell)
instead. Old state files persisted with `pre_fire_command` are migrated
in-place on load — no action needed for existing reminders, only new
ones must use the new flags.
