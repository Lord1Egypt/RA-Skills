# Takeaway

Reference for the `takeaway` flag on `create_deliberation` / `append_round` and the `round_takeaway` artifact it produces.

## Flag

| Flag | Accepted on | Effect |
|---|---|---|
| `takeaway` | `create_deliberation` AND `append_round` | Generates a per-round **Takeaway** when the round completes. It appears as a Takeaway section in the round text once written. |

Defaults `false` — no behavior change unless you opt in.

## The artifact

`wait_for_round` and `get_session` print a Takeaway section for a round that requested one, once it is generated:

- a bottom line — one paragraph answering "what did this round establish?"
- the round's key questions and answers, with references to the claims in the groups above, so you can go from a Takeaway item to the underlying reactions.

On the REST API this is `rounds[].round_takeaway`.

## Cost

Takeaways bill through the credit wallet at cost — typically around a cent per round.

## When to set it

Only when the user asks for one. You already receive the models' reactions and their full prose and synthesize from those yourself, so a Takeaway adds a model call and its cost without telling you anything new. When in doubt, leave it off.

## Public contract

Full contract: https://mumo.chat/docs/mcp#round-takeaway-artifacts
