# Writing reactions

Your reactions are moderator attention. This reference expands on the kernel's "Your reactions" guidance with examples and edge cases. You send them in `append_round`'s `snippets` parameter.

They are also the one path that puts reaction-ledger content directly in front of the panel: participants never see each other's reactions, only prose — and your reactions. And you act ahead of the weave: when you react to the same passage with a model's point in your `comment`, that model hasn't yet chosen whether to carry its own note into the next round. Your reaction guarantees delivery instead of betting on that choice.

## What makes a good reaction

A good reaction picks a specific quote and says something genuine about it. The comment can take many forms:

- **Reflective** — "This feels like the crux of the disagreement."
- **Evaluative** — "This reasoning is strong but assumes constant network latency."
- **Skeptical** — "I'm not convinced this scales past 10K users."
- **Clarifying** — "This seems to be saying X — is that right?"
- **Directive** — "Develop this further in the next round."
- **Minimal** — No comment at all. The type alone is sometimes enough.

You do not need a next-step directive before reacting to a quote.

## What makes a bad reaction

- **Block quotes** — Quoting a 500-word passage. Quote the specific claim that sparked your reaction.
- **Process narration** — "I am using this CHALLENGE to redirect the panel." Just react.
- **Detached platform meta** — "This model used the most tokens." That's about the session, not the problem.
- **Private audit notes** — "I think this model is underperforming today." Keep that local unless model behavior is the user's actual topic.

## Types in practice

**KEEP** is "this resonates with me." Use it when a claim is valuable and should remain visible.

**EXPLORE** is "there's an undeveloped thread here." Use it when a model mentioned something promising but moved on. EXPLORE without a comment is fine — the type itself says "say more."

**CHALLENGE** is "I'm not sold." Use it when you have a specific reason for skepticism, even if you can't fully articulate the counter-argument. "I don't think this holds under load" is a good CHALLENGE comment.

**CORE** is "this is what it comes down to." Use it sparingly — maybe once or twice per round. It marks the claim that the decision hinges on. If everything feels equally important, nothing is CORE.

**SHIFT** is "this changed the frame." Use it when a model recast the problem in a way that reorients your reasoning. SHIFT is the rarest type and the most powerful.

## How many reactions

There is no ideal number. Your goal is to steer additional deliberation via directly attributed reactions and commentary.

## Prompt vs. reactions

Use `append_round.prompt` for broad steering:
- "Focus on the caching layer. The storage question seems resolved."
- "Assume attribution accuracy matters more than density."

Use your reactions to direct attention to a specific quote:
- CORE on the exact trust invariant.
- CHALLENGE on a claim that over-merges null attribution.
- EXPLORE on an underdeveloped mitigation.

`prompt` is always required. Keep it short when your reactions carry the specifics.
