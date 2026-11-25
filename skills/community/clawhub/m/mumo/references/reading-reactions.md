# Reading reactions

Reactions are the structured output of each round. They show which claims were made, who originated them, and how other models reacted.

## Reading order

Read the models' reactions before diving into full prose. The reactions tell you *where* the interesting structure is; prose tells you *why*. If you read prose first, you can anchor on whichever model writes most persuasively.

Exception: in small sessions with only a few claims, read however is natural.

## What a claim row contains

- **The quoted claim** — a specific passage from a model's response.
- **The quoted model** — who originated the claim.
- **Reactions** — how other models (and the moderator, in later rounds) reacted, each with a type and optional comment.

Agreement shows as multiple KEEP reactions on the same claim; CORE says a model finds the point significant, not that it is right. Agreement is not verification: models can agree on something wrong. Disagreement shows as CHALLENGE reactions. A point that drew no reaction does not appear in the groups; it lives only in the responses.

## The four groups

When a round has reactions, the read tools print reacted-to claims in four groups, in this order: **Contested** (a model challenged it), **Open** (a model wants it explored), **Pivotal** (a model called it central, or it changed a model's frame), **Kept** (a model kept it). A claim appears once, under the strongest reaction another model gave it (or yours, if only you reacted), with all of its reactions listed. All four counts print, zero included, so an empty Contested group is itself a signal. A round with no reactions prints no groups.

The groups describe reactions, not truth. A claim in Pivotal was important to the argument; nobody verified it.

Reactions are visible to you and the user, not to the other participants — each model sees only its own prior reactions (as private notes to weave into its next response) plus everyone's prose. The models' reactions are your privileged view of the full ledger; see the kernel's "Reactions are in the ledger, responses are on the record" section for how to steer with them.

## Continuation signals

The models' reactions are your primary signal for whether to continue.

**Continue when:**
- A decision-relevant claim has unresolved CHALLENGE reactions.
- A promising claim has no reactions — it was raised but not engaged with.
- A SHIFT reaction suggests a model changed its position, but the implications haven't been explored.

**Stop when:**
- Key claims show convergent reactions (mostly KEEP).
- Remaining disagreements are on claims that don't affect the decision.
- The reactions are stable across rounds — same claims, same positions, no movement.

Don't continue just because unresolved claims exist. Only unresolved claims on the decision-relevant subset warrant another round. Peripheral disagreements are noise, not signal.

## Choosing what to react to

Use the models' reactions to decide where to focus, then choose exact quotes from the prose.

Good targets:
- Claims that multiple models reacted to differently.
- Claims that one model challenged and others ignored.
- Isolated claims that seem important.
- Shifts in framing.
- Core constraints that need anchoring.

## Attribution accuracy

When you write your own reactions or summarize for the user, attribute every quote to the model that wrote it. Check the response before setting `quoted_model`. If two models made the same point independently, say so; don't credit one. Users can audit quotes against the raw responses.

## Reactions are not verdicts

The reactions compress argumentative structure but lose rhetorical nuance and confidence texture. They show where attention clustered, not a ruling on who's right. Use them to navigate, then read the prose to understand.
