# Adapter: Method / Algorithm

Use this adapter when the paper's main contribution is a model, estimator, training recipe, inference procedure, optimization procedure, operator, architecture component, decoding strategy, or algorithmic mechanism, and the paper's core claim is that this mechanism improves some target behavior under evaluated settings.

This adapter is the direct successor to the older broad `ml-method.md`, but it is narrower and more explicit. It should be used for papers whose real contribution is the method itself, not primarily a benchmark, dataset, survey, or systems tradeoff.

## What to prioritize

1. The exact mechanism: objective, estimator, update rule, operator, architecture change, or inference-time procedure.
2. The paper's main move: what is genuinely new and load-bearing.
3. The reduction story: what the method becomes if the claimed key component is removed.
4. The training, optimization, or inference pipeline when it materially affects the result.
5. Where the gain is supposed to come from: representation, optimization, inductive bias, search, memory, retrieval, scale, or engineering.
6. The minimum implementation detail needed to preserve the paper's real mechanism faithfully.

## Questions to answer in the note

- What is the exact method, not just the intuition or marketing phrase?
- Which component is doing the conceptual work?
- What would the method reduce to without that component?
- Is the paper proposing a new mechanism, a new composition of known parts, or a new training/inference regime?
- Where are the reported gains most plausibly coming from?
- Which details would matter most if I had to re-explain or reimplement the method later?

## Minimum insertions or expansions into the base note

Add or expand these sections.

### Problem setup

Include:

- the target task or scientific objective
- the performance target or failure mode being addressed
- the regime in which the method is meant to help
- what prior methods are claimed to miss

### Main idea

Be explicit about both:

- the plain-language move
- the technical move

State what the method changes relative to a reasonable baseline.

### Technical core

Include as needed:

- objective function, estimator, recursion, or state update
- architecture / module / operator definition
- inference-time or training-time workflow
- what input, state, memory, or latent object is transformed at each step
- complexity, scaling, or resource implications when part of the claim

Preserve equations when the mechanism depends on them. Use pseudocode or numbered steps when execution order matters.

### Evidence

Focus on evidence that validates the claimed mechanism, not just the headline score.

Include:

- the strongest comparisons relevant to the method claim
- ablations that isolate the main move
- evidence about optimization sensitivity or inference sensitivity when relevant
- evidence distinguishing method gain from scale, budget, or engineering gain

### Implementation / reproduction notes

Include:

- details that materially affect outcomes
- hidden assumptions in preprocessing, batching, augmentation, prompt construction, retrieval, caching, decoding, or training schedule
- any missing detail that would block faithful reconstruction

## Special reading rules

- Separate method novelty from benchmark choice.
- Separate method gain from compute, data, or hyperparameter advantage.
- Separate conceptual novelty from assembly of known components.
- Ask whether the central mechanism is actually tested, or only bundled with other changes.
- When results are strong, inspect whether scale or engineering is doing more work than the paper's named idea.
- When the method is simple, do not penalize simplicity; judge whether the mechanism is real and well-supported.

## Typical failure patterns to watch for

- the paper claims a mechanism but only tests a bundle
- the decisive gain comes mostly from scale, tuning, or data differences
- the baseline omits the closest or strongest relevant alternative
- the method is underspecified where implementation choices matter
- the headline novelty is only a relabeling of known design patterns
- the note starts describing outcomes without preserving the actual update rule or procedure

## Reusable note prompts

- “The paper's main move is …”
- “Without the key component, the method reduces to …”
- “The claimed gain appears to come mainly from … rather than …”
- “The strongest evidence for the mechanism is …”
- “A faithful reconstruction would need …”
