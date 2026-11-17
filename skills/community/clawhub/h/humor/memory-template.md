# Memory Templates — Humor

File formats for `~/Clawic/data/humor/`. Create each file on its first real entry, not preemptively.

## profile.md — the learned taste

```markdown
# Humor Profile

## Works
<!-- Types that land. Format: "type: evidence, date" -->
<!-- e.g. "dry wit: quoted my staging line back, 2026-07-20" -->

## Fails
<!-- Types demoted. Format: "type: what happened, date" -->

## Intensity
<!-- subtle | moderate | bold — highest EARNED level (still capped by humor_ceiling) -->

## Contexts
<!-- Where humor is welcome/unwelcome, incl. per-room evidence. Format: "context: level" -->
<!-- e.g. "#team-x channel: dry wit landed room-wide" / "their client drafts: zero, flagged" -->

## Signals
<!-- How THIS user shows amusement, as deltas from baseline. Format: "signal: meaning" -->
<!-- e.g. "'ha.' with period = strong positive; reflexive 'lol' = noise" -->

---
*Empty sections = no data yet. Start subtle, observe, fill.*
```

Type statuses (Locked/Unlocked/Works/Failed) and transition rules: `feedback.md`.

## history.md — the attempts log

One line per humor event, newest last. Trim to the last 30 entries; fold any pattern into `profile.md` before deleting (`feedback.md` Maintenance).

```markdown
# Humor History

- 2026-07-20 | dry wit | debugging aftermath, 1:1 | strong positive ("lmao")
- 2026-07-21 | callback (staging server) | casual | mild positive
```

## callbacks.md — running jokes

```markdown
# Callbacks

- "the staging server survived" — born 2026-07-20 (1:1); uses: 2; last: 2026-07-21; status: alive
```

Track the room it was born in (callbacks don't cross rooms, `groups.md`), use count, and status. Retire after two flat reactions (`types.md`).

## wins.md — verbatim hits

The exact wording of jokes that drew ladder-level 1-3 reactions, for pattern study — reuse the *pattern*, never the joke (`signals.md`).
