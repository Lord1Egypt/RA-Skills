# Audience Cognition Mapper v0.2

## Purpose

Map the audience's current knowledge, likely confusion, trust barrier, and best entry point before writing.

Audience translation is not tone adjustment.
Audience translation is the reconstruction of the audience's path from confusion to understanding.

## Required Output

Before drafting, internally produce:

```yaml
audience_cognition:
 audience_label:
 knowledge_floor:
 likely_unknown_terms:
 likely_misunderstanding:
 trust_barrier:
 emotional_state:
 practical_question:
 best_entry_point:
 forbidden_entry_point:
 analogy_budget:
 terminology_budget:
 evidence_need:
 desired_shift:
```

## Field Definitions

### audience_label

Examples:

* zero_ai_background
* general_public
* business_executive
* investor_nontechnical
* technical_team
* product_manager
* regulator
* customer_first_touch
* expert_reader

### knowledge_floor

What can be assumed?

Examples:

* understands daily work risk
* understands software products
* understands AI at consumer level
* understands model/prompt/evaluation
* understands system architecture

### likely_unknown_terms

Terms that should be avoided or explained.

Examples:

* model
* prompt
* workflow
* guardrail
* harness
* evaluation
* feedback loop
* hallucination
* runtime
* agent

### likely_misunderstanding

What might the audience wrongly think?

Examples:

* AI is always right if it sounds confident.
* A better prompt solves everything.
* Writing quality equals reliability.
* A checklist reduces creativity.
* Automation means no human judgment is needed.

### trust_barrier

What prevents them from believing the message?

Examples:

* AI sounds impressive but unreliable.
* Technical explanation sounds abstract.
* The concept seems like jargon.
* The value is unclear.

### practical_question

What question is the audience really asking?

Examples:

* Why can't I just use AI directly?
* What can go wrong?
* How does this make work safer?
* Why does this matter to me?

### best_entry_point

Start from the audience's lived problem.

Examples:

* "AI can make mistakes that are hard to notice."
* "A good answer is not the same as a safe answer."
* "Important work needs checks before delivery."

### forbidden_entry_point

Avoid starting from insider concepts.

Examples:

* "This is not just prompt engineering."
* "This is a model-runtime constraint layer."
* "This improves agentic workflow reliability."
* "This is a guardrail evaluation system."

### analogy_budget

How many analogies are allowed?

Default:

* short output under 500 Chinese characters: max 1 analogy
* long output: max 2 analogies

### terminology_budget

How many technical terms can appear?

Default:

* zero_ai_background: 0-2 terms, each must be explained
* general_public: 2-4 terms
* technical_team: unrestricted if useful

### evidence_need

How much proof does this audience need?

Options:

* low
* medium
* high

### desired_shift

Format:

Before:
[what the audience thinks now]

After:
[what the audience should understand]

## Mapping Rules

```text
Rule 1:
Do not confuse audience simplicity with audience stupidity.

Rule 2:
For zero-AI-background audiences, explain the risk before the mechanism.

Rule 3:
For technical audiences, explain the mechanism before the analogy.

Rule 4:
For investor audiences, explain the business consequence before the architecture.

Rule 5:
For customer audiences, explain the workflow impact before the conceptual definition.

Rule 6:
If the target audience is unclear, infer from the user's wording and task type.
Do not ask follow-up unless the task cannot proceed.

Rule 7:
For short outputs, do not expose this mapping unless requested.
```

## Narrative Authority Override Rule

Audience adaptation must not override narrative authority.

The audience determines:

```text
entry point
vocabulary
metaphor
pace
emotional temperature
level of technical detail
```

The audience must not determine:

```text
central judgment
protagonist
value at stake
claim boundary
actual mechanism
opposing force
```

## Anti-Overfitting Rule

Do not overfit the story to the audience.

Bad:

```text
For children, turn the entire concept into a toy story.
For rappers, add slang and rhythm.
For short-video viewers, only optimize for hook.
For investors, remove human stakes and speak only in market language.
```

Better:

```text
For each audience, find the doorway they can enter through while preserving the story's core judgment.
```

## Audience Entropy Tolerance

Before rendering, estimate the audience's entropy tolerance.

```yaml
audience_entropy:
  tolerance: low | medium | high
  reason:
  max_new_concepts:
  metaphor_limit:
  surprise_limit:
```

## Default Tolerances

```text
child audience: low
zero AI background: low
general public: low-medium
business audience: medium
technical team: medium-high
expert audience: high
investor audience: medium-high
close one-on-one listener: medium
cold outreach listener: low-medium
```

## Rules

1. Low-tolerance audiences need familiar ground before surprise.
2. Expert audiences can handle higher conceptual entropy, but still need structure.
3. One-on-one communication should avoid excessive surprise; relevance matters more than shock.
4. Short-form public content can use stronger surprise, but must resolve quickly.
5. If audience tolerance is unknown, default to medium-low.

## Required Internal Check

Before rendering, ask:

```text
What changed for the audience?
What stayed fixed from the story?
```

If the answer is unclear, return to Narrative Authority Mapper before drafting.
