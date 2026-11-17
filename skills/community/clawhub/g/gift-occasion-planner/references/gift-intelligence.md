# Gift Intelligence Reference

## Why Gift Systems Fail

Three failure modes kill gift planning:

1. **No lead time** — you remember 2 days out; every option left is expedited
   shipping or gas-station flowers. Lead time converts panic into thought.
2. **No memory** — "what did I give her last year?" Most people can't answer
   for 5+ people. Repeating a gift, or re-gifting the same category forever
   (books, books, books), reads as low effort even when the budget was real.
3. **No profile** — without recorded interests/sizes/taboo lists, every
   purchase is a guess. Gift quality = profile quality.

This skill attacks all three: reminders at 60/21/7/1 days, permanent history
per person, and a profile that compounds yearly.

## Occasion Types

| Kind | Date logic | Notes |
|---|---|---|
| birthday | fixed MM-DD | auto-created from `add-person --birthday` |
| anniversary | fixed MM-DD | add explicitly |
| mothers-day | 2nd Sunday of May (US) | computed per year — never hardcode |
| fathers-day | 3rd Sunday of June (US) | computed per year |
| thanksgiving | 4th Thursday of November | computed |
| graduation / custom | one-time or fixed date | review annually |

For non-US Mother's/Father's Day dates (UK Mothering Sunday = 4th Sunday of
Lent; others differ), use `--kind custom --month-day` with the local date.

## The Recommendation Logic

1. **Never repeat** — suggestions are filtered against history with token
   overlap ≥60% (near-dupe detection, so "garden kneeler" blocks "kneeler
   for garden" but not "opera tickets").
2. **Interest rotation** — the engine detects which interest the last gift
   related to and rotates to a different one (single-interest profiles are
   exempt). This is what prevents the "another gardening thing" spiral.
3. **Category rotation** — categories used in the last 2 years
   (tool/experience/consumable/personal) are deprioritized: book →
   experience → gear → personal.
4. **Taboo filter** — hard exclusion on profile taboo tokens.
5. **Wish-list first** — if notes record a mentioned want ("said she wanted
   better pruners"), that suggestion surfaces first: explicitly-stated wants
   have the highest hit rate of any gift class.

The engine proposes, the human decides. Suggestions always carry their
rationale so the plan card reads as reasoning, not randomness.

## Budget Model

- Per-person budget per occasion; suggestions land within ±20% flex.
- `budget` shows planned (budget × occasions) vs spent for the year —
  December's damage becomes visible in March.
- Rule of thumb for setting budgets: the number that would make you mildly
  annoyed to spend twice in one month, not the number you think sounds
  reasonable in the abstract.

## Lead-Time Ladder

| Reminder | Purpose |
|---|---|
| T-60 | thinking window: recommendations, non-urgent ideas, handmade options |
| T-21 | decision point: pick the gift, order anything shippable |
| T-7 | escalation: if still IDEA, restrict to fastest available options |
| T-1 | wrap/card/day-of logistics |

ICS export creates all four as all-day events per occasion with profile
summary (interests/budget/taboo) in the description — the reminder is
self-contained even if you never open the tool again.

## Plan Card Deadlines

- **Buy by** = occasion date − max(7, min(days_left, 14)) days — a shipping
  buffer that grows with remaining lead time.
- **Wrap by** = day before.
- **Card angle** = derived from the first profile interest; replace with
  something specific from notes whenever possible ("for the rose bed that
  beat the neighbors again" beats "enjoy gardening").

## Gifting Heuristics Worth Knowing

- **Consumables + one durable** beats one big item for most recipients.
- **Experiences** outperform objects in satisfaction research for anything
  past acquaintance level — but only if scheduling friction is low (include
  a concrete date option, not a voucher).
- **Sizes**: never guess clothing sizes; if it's on the profile, it was
  checked. If not, accessories and non-size gifts are safer.
- **Kids**: age-band gifts turn over fast; check the age every year.
- **Partner anniversaries**: the card matters as much as the gift; budget
  20% of effort for it. The #1 complaint is not "cheap gift", it's
  "obviously last-minute".
- **Group gifting**: record who contributed what in notes — next year's
  split is easier and avoids the same person always organizing.

## Privacy

All data local (`gifts.json`). Gift plans are among the most sensitive
household data there is — spouse-surprise gifts, budgets, personal notes.
Nothing leaves the machine.
