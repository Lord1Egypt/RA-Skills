# Research-Generative Methodology

Use this reference when the user wants more than grounded verification.
Its goal is to turn a paper reading into a **research-generation exercise** while keeping every important statement source-aware.

The core move is:

> Read the paper as a hidden design path.

## 1. Research Equation

Compress the paper into:

`old success + broken assumption + hard setting + borrowed tool + surrogate mechanism`

Useful questions:

- What important paradigm already worked?
- What hidden assumption made it work?
- In what realistic setting does that assumption fail?
- What neighboring method almost transfers?
- What missing mechanism `Y` blocks direct transfer?
- What surrogate `Z` does the paper build instead?

## 2. How the Direction Was Likely Found

Use evidence-backed phrasing:

- "The authors likely noticed that ..."
- "A plausible thinking path is ..."
- "The setup suggests ..."

Try to reconstruct:

- starting dissatisfaction
- tempting transferred method
- blocking constraint
- replacement logic

## 3. How the Story Was Built

Look for:

`challenge -> failure mode -> design principle -> module -> ablation`

Strong papers often create a loop instead of a bag of tricks.
Explain whether one module creates the resource that the next module needs.

## 4. Method Deep Reading

For each module, reconstruct:

`failure + ideal unavailable solution + available proxy + design choice + hidden assumption + risk`

The most useful framing is usually:

> This module is not just a trick; it is a surrogate for the missing mechanism `Y`.

## 5. Reverse Citation Logic

Treat citations as narrative functions:

- field anchor
- limitation evidence
- method ancestor
- neighboring inspiration
- baseline pressure
- protocol justification
- contrast boundary

Explain what permission each key citation gives the paper.

## 6. Experiments as Story Evidence

Read each result as:

`claim + counterfactual + metric + stress condition`

Ask:

- what claim it supports
- what alternative explanation it rules out
- which module it validates
- whether the stress condition really matches the paper's target difficulty

## 7. Story Pattern Worth Learning

Extract one reusable pattern, such as:

- replacement story
- three-module story
- two-axis empty cell
- closed-loop contribution
- hidden-assumption break

## 8. Weakness to New Idea Conversion

Use:

`future work = current method + violated assumption + new mechanism`

For each strong weakness, ask what next paper becomes possible if the key hidden assumption fails harder.

## 9. Writing Rules

Prefer phrasing like:

- "A plausible author-side thinking path is ..."
- "This module is best understood as a surrogate for ..."
- "The citation is not ornamental; it functions as ..."
- "This weakness can be converted into a new research direction ..."

Avoid:

- restating the abstract
- listing sections without causal explanation
- paraphrasing equations without saying why they exist
- speaking as if private author intent were directly observed

---

# Direction-Mining Upgrade for v1.2.0

This upgrade adds explicit research-seed generation to the original research-generative reading method.
The original method asks how a paper was likely invented; this upgrade asks which next paper can be tested.

## 10. Research Seed Equation

Turn any strong weakness into:

`Seed = evidence trigger + hidden assumption + violated setting + new mechanism + minimum viable experiment`

A useful template is:

```text
The paper's method works because H is usually true.
In setting S, H is false or unverifiable.
Current proxy Z is insufficient because of failure F.
A new mechanism Z' may solve F.
The minimum viable experiment is E.
A negative result would mean N.
A killer result would be K.
```

## 11. New Direction Templates

### 11.1 Assumption-violation seed

```text
Current paper: M works if H.
Break: H fails under S.
Research question: Can M be redesigned for not-H?
Mechanism: replace proxy P with mechanism Q.
Minimum viable experiment: compare M and Q under controlled not-H stress.
```

### 11.2 Proxy-mismatch seed

```text
Current paper: proxy P is used as a surrogate for ideal signal Y.
Break: P diverges from Y under condition S.
Research question: Can we estimate Y more directly or build a better surrogate?
Minimum viable experiment: construct a stress test where P and Y disagree.
```

### 11.3 Reviewer-objection seed

```text
Objection: the paper does not rule out alternative explanation A.
Research question: Is the reported gain due to the proposed mechanism or A?
Minimum viable experiment: isolate A with matched controls.
Killer result: proposed mechanism wins when A is controlled.
```

### 11.4 Negative-result seed

```text
Popular belief: method family M should help in setting S.
Negative result: M fails despite careful tuning.
Why this matters: failure reveals that assumption H is false.
Minimum viable experiment: reproduce failure across small but representative cases.
```

### 11.5 Successor-gap seed

```text
Original paper: introduced mechanism Z.
Successor papers: reuse Z but avoid setting S.
Gap: no one has tested Z under S or replaced it when it fails.
Minimum viable experiment: benchmark Z in S against a simple robust alternative.
```

## 12. Scoring Candidate Directions

Score top seeds on 0-5 scales:

- `novelty`: Does this differ from direct follow-up work?
- `significance`: Would the field care if the result is true?
- `testability`: Can a first experiment decide anything useful?
- `feasibility`: Can the user plausibly start it soon?
- `evidence_anchor`: Is the seed grounded in paper evidence?
- `risk_adjusted_value`: Is the upside worth the uncertainty?

Prefer a diverse board:

- one low-risk validation direction
- one medium-risk mechanism direction
- one high-risk boundary-pushing direction

## 13. Minimum Viable Experiment Discipline

A minimum viable experiment is not a full paper.
It is the smallest decisive test that reduces uncertainty.

It must specify:

- dataset or synthetic setup
- baseline or ablation
- changed mechanism
- metric or proof target
- expected result
- decision rule
- negative-result interpretation

Do not output research directions without at least a draft minimum viable experiment.

## 14. Boundary-Pushing Direction Filter

A direction is likely boundary-pushing only if it changes at least one of:

- the assumption under which a method family works
- the mechanism used to replace an unavailable ideal signal
- the benchmark or stress condition used to define progress
- the theory of why a method should work
- the community's understanding through a surprising negative result

Engineering cleanup is useful, but do not label it boundary-pushing unless it changes understanding.
