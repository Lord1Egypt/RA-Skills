# Specificity and thought visibility

This document describes the *deepest* signal that separates AI-looking text from human-written text, and the one that detector-style tools are most sensitive to. It is **not** about word choice. It is about *what the text knows and how it shows it*.

If you only have time to internalize one idea from this skill, internalize this one.

## The core claim

AI text and human text differ most clearly on two dimensions:

- **Specificity**: how concrete the claims are.
- **Thought visibility**: how much of the writer's reasoning is on the page.

AI text tends to be **abstract, uniform, and reasoning-free**. Human text tends to be **specific, varied, and reasoning-revealing**. The gap between them is what most readers (and most detectors) actually notice, even when they cannot name what is wrong.

Removing AI lexical patterns (the catalog in `anti-ai-patterns.md`) is necessary but not sufficient. A draft that uses "significant" instead of "pivotal" is still AI-looking if every claim is generic and the reasoning is hidden.

## Specificity: the cure for "AI slop"

"AI slop" is the name for text that says nothing wrong and nothing useful. It is grammatically clean, lexically correct, and informationally empty. The most common form:

- "The product improves productivity."
- "This approach has many benefits."
- "The team is passionate about delivering value."

Each sentence is true, vague, and says nothing the reader did not already know.

The fix is **specificity on five axes**.

### 1. Numbers

Replace "many" with a count. Replace "improve" with a delta. Replace "fast" with a millisecond figure.

| AI slop | Specific |
| --- | --- |
| Many users adopted it | 1,840 teams signed up in the first month |
| Performance improved | p99 latency dropped from 800ms to 95ms |
| It is popular | 4,200 GitHub stars, 18 contributors |
| We grew revenue | Q3 ARR went from $1.2M to $1.9M |

When the draft has invented numbers, remove or soften them. When the user supplies real numbers, keep them front and center. Real numbers are the strongest single signal of human authorship.

### 2. Time

Anchor claims in time. "Recently" is vague. "Last Tuesday" is real.

- "Earlier this year" → "In March 2026"
- "Currently" → "As of the June 1 release"
- "Soon" → "By end of Q3" or "before the holiday freeze"

When the user supplies a time, keep it. When the AI inserts a vague time, replace it with the actual time the user's draft implies, or remove it.

### 3. Place and context

Anchor actions in place when it matters.

- "At the company" → "In our 4-person platform team in Berlin"
- "In the codebase" → "In `internal/billing/`, line 142"
- "In the meeting" → "In the Tuesday product review with Priya and Marcus"

The reader can picture the scene. The AI text cannot.

### 4. Names

Use real names. AI tends to anonymize. Real writers know who they are talking about.

- "A user reported" → "Dana from Acme wrote in"
- "A senior engineer mentioned" → "Marcus, who has been on the team since 2019, said"
- "The team decided" → "Priya, Sam, and I agreed on Friday"

Names are a high-signal marker of voice. They are also a privacy concern — use them only when the user has the right to share.

### 5. Sensory and concrete detail

AI text lives in abstractions. Real text uses senses.

- "The food was good" → "The broth was cloudy, the noodles had bite, and the chili oil numbed my tongue"
- "The room was busy" → "Six people were on calls, two were arguing about a deploy, and one was eating a sandwich at the desk"

Sensory detail is most useful in narrative and review writing. It is wrong for technical docs. Match the surface.

## Thought visibility: showing the work

Specificity is necessary but not sufficient. The other half is **showing how the writer got there**.

AI text usually reads as: *claim, claim, claim, conclusion*. Human text usually reads as: *claim, but also, because, although, so*. The visible reasoning is what makes the reader trust the conclusion.

### 1. Show the "but"

Every interesting claim has a counter-claim. Real writers acknowledge the tension. AI often hides it.

- AI: "We chose Postgres."
- Human: "We chose Postgres over SQLite. SQLite would be simpler, but our row count and replication needs make Postgres the better fit."

The "but" can be small. It just has to be there.

### 2. Show the "because"

Conclusions need a reason that is on the page.

- AI: "We are moving to gRPC."
- Human: "We are moving to gRPC because the protobuf schema gives us end-to-end type safety, and our latency budget on the hot path is too tight for JSON parsing."

The "because" can be a number, a constraint, a prior failure, or a principle. The point is that the reader can follow the chain.

### 3. Show the "I don't know"

Hedging is a feature when it is honest. AI hedges to seem careful. Real writers hedge when they actually do not know.

- AI: "This may or may not improve performance."
- Human: "I do not have benchmark data for write-heavy workloads, so I am not sure."

The second one is a useful hedge. The first is noise.

### 4. Show the "I changed my mind"

Real writers update. AI does not (in a single response). Visible updates are a strong human signal.

- "Initially I thought X. After talking to Priya, I think Y."
- "The first version used SQLite. We switched when the read traffic hit 10k QPS."

Visible change of mind is also a sign of intellectual honesty. Keep it where the user's draft has it.

### 5. Show the comparison

Real claims come from comparison. AI often states them bare.

- AI: "The new design is better."
- Human: "The new design is easier to learn, but harder to extend. For our use case (internal tools, small teams), easier-to-learn wins."

A useful comparison names the alternative and the criterion. It is also how a reader can disagree with the conclusion while respecting the writer.

### 6. Show the limit

A claim with a stated limit is more credible than a universal claim.

- AI: "This works for any team."
- Human: "This works well for teams under 50, with a single product, on a single time zone. Outside that, the latency assumptions break."

Stating a limit is one of the most effective humanizing moves. It signals that the writer actually understands the thing.

## How to apply both at once

The simplest test for an AI-looking paragraph:

1. **Substitution test**: replace every specific noun with a generic one and every number with a vague one. If the paragraph still makes sense, it was not saying anything specific. Rewrite for specificity.
2. **Deletion test**: remove every clause that says "because", "but", "although", "so", "I think", "I don't know". If the paragraph still makes sense, the reasoning was decorative, not load-bearing. Rewrite to make the reasoning load-bearing.
3. **Stance test**: read the paragraph aloud. Does it sound like a person with a position, or a press release? If the latter, find the writer's actual position and put it on the page.

A draft that fails all three tests is not just AI-looking. It is not doing its job. The rewrite is not a polish pass. It is a re-do.

## Where this is not appropriate

- **Reference, encyclopedic, and legal writing**: precision is more important than visible reasoning. The user may want neutral, impersonal prose. Do not inject "I think" into a statute.
- **Marketing copy aimed at buyers**: the buyer wants the *outcome*, not the writer's reasoning. Keep the specificity, drop the visible "because" chain.
- **Headlines and short social posts**: there is no room for reasoning. Specificity is the only lever.

Match the surface. The point is to write *well* for the surface, not to apply a fixed recipe.

## The meta-point

The reason "AI detectors" exist is that a lot of AI-generated text is generic. The reason human text reads as human is that humans actually have something to say. Specificity and thought visibility are not tricks. They are what good writing always did. The catalog in `anti-ai-patterns.md` and the profile in `voice-profile-deep.md` are diagnostic tools. This document is the *substance* they serve.
