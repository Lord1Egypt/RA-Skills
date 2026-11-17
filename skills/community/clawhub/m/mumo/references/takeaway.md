# Takeaway

Reference for the `takeaway` flag on `create_deliberation` / `append_round` and the `round_takeaway` artifact it produces.

## Flag

| Flag | Accepted on | Effect |
|---|---|---|
| `takeaway` | `create_deliberation` AND `append_round` | Generates a per-round **Takeaway** (`round_takeaway`) when the round completes. Surfaces on `get_session` once written. |

Defaults `false` — no behavior change unless you opt in.

## The artifact

`get_session` returns `rounds[].round_takeaway` for any opted-in round whose generation has completed (null otherwise):

- `bottom_line` — one-paragraph answer to "what did this round establish?"
- `items[]` — the round's key questions, each `{ question, answer, consensus, claim_ids }`. `consensus` states where the panel agreed or split; `claim_ids` reference the round's claim map, so you can jump from a Takeaway item to the underlying reactions.

## Cost

Takeaways bill via the standard credit wallet at **0 bps markup** (at-cost passthrough) — typically around a cent per round.

## When to set it

Set `takeaway` any time a round-level summary may matter later, or when the round's claim map has enough structure that a curated read path will save you work. It's cheap; when in doubt, opt in.

## Public contract

Full contract: https://mumo.chat/docs/mcp#round-takeaway-artifacts
