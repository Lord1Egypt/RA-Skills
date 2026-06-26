# Replies — classification and forwarding

## The contract (Law #4, restated in detail)

Poke has no ears. The agent forwards inbound user messages:

```bash
poke --reply "<user's exact message>" --channel <ch> --target <tgt> [--from <sender-id>]
# or, for sensitive content:
echo "<user's exact message>" | poke --reply-stdin --channel <ch> --target <tgt> [--from <sender-id>]
```

Prefer `--reply-stdin` when the reply may contain personal content —
`--reply "..."` puts the text in shell history, `ps` listings, and any
log that captures argv. `--reply-stdin` reads the same text from stdin
so it never appears on the command line.

Output is one line:

- `REPLY matched id=<id> action=<intent>` — matched a pending reminder
- `REPLY matched id=<id> action=snooze until=<iso>` — snooze, with the
  resolved snooze-until timestamp
- `REPLY no_match` — no candidate matched; agent ignores and moves on

Forwarding ANY message is safe — `no_match` just means there was nothing
to match against (no pending reminders on that channel/target pair, or
the text doesn't look like a reply).

`--from SENDER` is optional but recommended in any context where multiple
users share a channel/target pair. When provided, only reminders whose
`target` or `origin_target` matches `SENDER` are eligible — anyone else's
message returns `no_match` without running the classifier.

Do not forward replies from public threads or multi-user rooms where
other participants can see poke messages — use a private DM or dedicated
channel per user.

## When the agent should forward

Forward anything that *could* be a reply to a recent poke. Cheap
heuristic: if there's been a delivered poke on this channel/target in
the last ~hour and the user's new message could plausibly be answering
it, forward. The classifier is robust; over-forwarding is fine, the cost
is one CLI call returning `no_match`.

Don't forward: messages clearly addressed to a different topic, system
events, the agent's own outputs.

## Intent classification

Poke uses a bilingual heuristic first (regex against English + Chinese
patterns). If `--agent` is set and the heuristic doesn't match, an
LLM classifier runs against the pending candidate list (top 5 by
recency).

The intents:

- **confirm** — user says the task is done.
  English: "done", "did it", "handled", "finished", "completed", "got it
  done", "wrapped up", "taken care of", "took care of"
  Chinese: 好了, 完成了, 做完了, 搞定了, 处理好了, 已经处理, 已完成, 弄完了

- **cancel** — user wants reminders to stop entirely.
  English: "stop", "cancel", "leave me alone", "shut up", "don't remind",
  "no more reminders"
  Chinese: 取消, 别提醒了, 不用提醒, 别再提醒, 不要再提醒, 停掉, 停了,
  闭嘴, 别催了

- **snooze** — user wants a delay. Default 15 minutes. Parses durations
  like `snooze 30m`, `give me 1 hour`, `later 2h`, `稍后 30 分钟`.
  Recognized units: `min`, `minute(s)`, `m`, `hour(s)`, `hr(s)`, `h`.

- **followup** — user acknowledges but isn't done. Suppresses the
  unconfirmed-followup without ending the cycle.
  English: "later", "give me a minute", "give me a sec", "i saw it",
  "saw it", "in a bit", "working on it", "on it", "will do", "got it",
  "okay", "ok", "kk"
  Chinese: 等会儿, 等会, 稍后, 一会儿, 待会, 等下, 待一下, 我知道了,
  知道了, 看到了, 收到, 在弄, 马上, 回头弄, 晚点

- **ignore** — text doesn't match any pattern. Returns `no_match`.

## What happens per intent

| Intent | One-off | Recurring (calendar) |
|---|---|---|
| **confirm** | Marks `confirmed=true`, deletes the reminder. | Ends this iteration. Advances `next_base_due_at` to the next OnCalendar match. Re-arms `pre_fire_fired`/`post_fire_fired` so the next cycle runs hooks again. |
| **cancel**  | Marks `cancelled=true`, deletes. | Same — permanently terminates. |
| **snooze**  | Sets `snooze_until`, clears next poke + followup, decrements `cycle_poke_count` by one (undoes one escalation level). Reschedules for after snooze expiry. | Same. |
| **followup** | Clears the current cycle's poke + followup but leaves the base due. (For one-off w/o a base due, terminates.) | Ends iteration, advances. |

After any successful match, `maybeRunPongCommand` fires the
`--on-pong-command` stage (if set). It fires at most once per cycle
(gated by `pong_fired`).

## Snooze grammar (detail)

`parseSnoozeDuration(text)` looks for `(\d+)\s*(unit)` where unit is one
of `min`, `minute`, `minutes`, `m`, `hour`, `hours`, `hr`, `hrs`, `h`.
Examples:

- `"snooze"` → 15 minutes (default)
- `"snooze 30m"` / `"snooze for 30m"` → 30 minutes
- `"give me 2h"` / `"later 2h"` → 2 hours
- `"稍后 30 分钟"` (parses Chinese digits + English unit synonyms via
  the catch-all) — note Chinese 分钟 won't match the unit regex; for
  Chinese specify the unit numerically with an `m` or `h` if you want
  precise parsing, otherwise it falls back to the default 15 minutes.

## Smoke test

```bash
poke --reply "done"        --channel discord --target user:1
# REPLY matched id=tr-… action=confirm

poke --reply "snooze 30m"  --channel discord --target user:1
# REPLY matched id=tr-… action=snooze until=2026-…

poke --reply "irrelevant"  --channel discord --target user:1
# REPLY no_match
```
