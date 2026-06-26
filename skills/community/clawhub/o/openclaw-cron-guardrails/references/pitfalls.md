# OpenClaw Cron Pitfalls

These are the real failure patterns to avoid.

## Pitfall 1 — Treating OpenClaw cron like Unix cron

Wrong mental model:
- “It just runs a command later.”

Better mental model:
- OpenClaw cron = scheduler + agent runtime + session routing + delivery routing

This means failures often happen **after** the job logic succeeds, during delivery.

## Pitfall 2 — Implicit `channel=last` on isolated jobs

This is the most common trap.

What happens:
- isolated jobs default to announce delivery
- CLI defaults delivery channel to `last`
- if `sessionKey` is missing, delivery resolution can fall back to the agent main session
- in multi-channel setups, this can fail with:
  - `Channel is required when multiple channels are configured ...`

Practical rule:
- in multi-channel environments, do not depend on implicit `last` for isolated visible jobs

## Pitfall 3 — No explicit delivery target for visible output

If the job is supposed to post somewhere externally, do not assume OpenClaw can infer:
- channel
- target
- account
- thread

Set them explicitly.

For Discord, prefer:
- `channel:...`
- `user:...`

## Pitfall 4 — Using isolated jobs for simple reminders

If the task is really “remind me later”, isolated is usually overkill.

Prefer:
- `main/systemEvent`

This removes most routing complexity.

## Pitfall 5 — Too-short timeouts

Typical failure pattern:
- prompt asks for analysis / planning / summarization
- job timeout is 60s
- run always dies as timeout, even though logic is otherwise fine

Repair rule:
- if the task is non-trivial, raise timeout before changing anything else

## Pitfall 6 — Missing timezone on recurring jobs

If wall-clock meaning matters, set `tz` explicitly.

Do not trust host-local defaults when the schedule matters to a human.

## Pitfall 7 — Debugging only the job definition, not the run log

Always inspect recent runs:

```bash
openclaw cron runs --id <jobId> --limit 10
```

You are trying to distinguish among:
- scheduler not firing
- job logic error
- delivery-target error
- channel auth/permission issue
- timeout

These are different bugs.

## Pitfall 8 — Assuming docs examples are enough

Docs examples are often valid, but they are not always hardened for:
- multi-channel setups
- multiple accounts
- thread-specific delivery semantics
- local environment quirks

Cross-check docs with source behavior when the routing model matters.

## Repair heuristics

### If the run has a good summary/output but final status is error

Suspect delivery, not the agent logic.

### If the error says channel is required or target missing

Suspect implicit route resolution.

### If every run dies around the same short duration

Suspect timeout.

### If the schedule looks right but runs occur at the wrong wall-clock time

Suspect timezone.

## Safe triage order

1. `openclaw cron runs --id <jobId> --limit 10`
2. classify the failure
3. fix one variable only:
- delivery
- timeout
- schedule/tz
- prompt
4. test again

## Known UX rough edges worth remembering

- Some CLI subcommands are not as structured/JSON-friendly as you would expect.
- Flag naming may differ from intuition (`--disable` vs expected variants).
- CLI behavior and agent-tool behavior can differ around session context.

Because of that, prefer explicit, boring, reproducible cron definitions over clever shorthand.

## Real-world failure patterns that motivated this skill

These patterns were observed in real local cron state, not just imagined during design:

- delivery-route failures in multi-channel setups
- visible jobs relying on fragile implicit routing such as `channel=last`
- explicit delivery channel without explicit delivery target
- implicit or too-short timeout on non-trivial jobs

This skill is meant to catch or prevent these patterns before they turn into silent failures.
