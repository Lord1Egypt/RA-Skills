# Research-Direction Mining Best Practices

This reference strengthens the deep-reading workflow for users whose main goal is to find new research directions and research points.
It should be used together with `research-generative-methodology.md` and the main `SKILL.md`.

## 1. Direction-Mining Three-Pass Reading

### Pass 1: Five-C triage with research promise

Answer:

1. `Category`: What kind of paper is this?
2. `Context`: What field conversation and prior assumptions does it depend on?
3. `Correctness`: Do the high-level assumptions, task, data, and comparisons look plausible?
4. `Contributions`: What does the paper claim to add?
5. `Clarity`: Is the argument readable and auditable?

Then add:

- likely hidden assumption
- likely missing mechanism
- likely weak evidence point
- whether the paper deserves a full direction-mining read

### Pass 2: Evidence / method / figure chain

Reconstruct the paper as:

`problem -> broken assumption -> design principle -> module -> formula -> figure/table -> experiment -> claim`

Required outputs:

- challenge-to-module table
- claim-to-experiment map
- formula role notes
- figure/table support notes
- proxy-vs-ideal mechanism notes

### Pass 3: Virtual reimplementation and hidden-assumption attack

Read as if you had to rebuild the paper.

Ask:

- What assumptions must be true for each module to work?
- Which assumptions are implicit rather than stated?
- What proof step, code step, data choice, or metric definition is carrying the argument?
- What special case makes the method easy to understand?
- What counterexample would break the method?
- What experiment would settle the main uncertainty fastest?

Required output:

- hidden-assumption list
- tiny example or special-case explanation
- dropped-assumption failure modes
- future-work triggers

## 2. Reverse Citation and Successor-Paper Reading

When tools and time allow, inspect a small set of successor papers or citation trails.

Use successor reading to distinguish:

- what the original paper claimed
- what later papers actually reused
- what later papers criticized or avoided
- what became a standard assumption
- what remains under-tested
- what has already become saturated

Do not fabricate trends.
If successor search was not performed, mark successor-derived directions as unavailable or lower confidence.

## 3. Critical + Creative Reading

Critical reading checks:

- Are the assumptions reasonable?
- Are the data and metrics suitable?
- Are baselines and controls sufficient?
- Is the evidence aligned with the claims?
- Are simpler explanations ruled out?
- Are the limitations honest and complete?

Creative reading asks:

- What good idea can transfer to a new setting?
- What stronger or cleaner assumption break would make a new paper?
- What missing mechanism should replace a proxy?
- What negative result would change how the community thinks?
- What would a first-week experiment test?

## 4. Reviewer-Grade Direction Audit

Use reviewer objections as idea generators.

| Audit dimension | What to ask | Direction trigger |
|---|---|---|
| Novelty | What is genuinely new relative to prior work? | If novelty is narrow, search for a broader mechanism or setting. |
| Significance | Who would use or build on this? | If impact is local, find a more important stress condition. |
| Soundness | Are claims technically supported? | If support is weak, propose decisive validation. |
| Methodology rigor | Are baselines, ablations, and controls enough? | Missing control becomes an experiment seed. |
| Statistical validity | Are uncertainty, variance, and sample size convincing? | Weak statistics becomes robustness or evaluation seed. |
| Reproducibility | Are details sufficient to recreate results? | Missing detail becomes replication or protocol seed. |
| Limitation honesty | Are structural weaknesses named? | Hidden limitation becomes assumption-violation seed. |
| Constructive critique | What feedback would improve the paper? | Actionable critique becomes a new project plan. |

## 5. Seed Types

Use these seed types in `direction_board.json`.

### 5.1 Assumption violation

`current method works if H; under not-H it breaks; build method for not-H`

Examples of `H`:

- labels are reliable
- data are IID
- clients are honest
- compute is sufficient
- distribution shift is mild
- proxy signal correlates with target mechanism
- evaluation benchmark represents deployment

### 5.2 Unavailable mechanism

The borrowed method normally needs an ideal mechanism `Y`, but the target setting lacks it.
The paper builds surrogate `Z`.
A new direction appears when `Z` is weak and another surrogate is possible.

### 5.3 Proxy mismatch

The paper optimizes a proxy signal.
Ask whether the proxy can be gamed, become stale, or diverge from the real target.

### 5.4 Evidence gap

A main claim lacks the exact experiment, ablation, proof, or dataset needed to verify it.
The seed is a decisive test.

### 5.5 Tiny example or counterexample

A small special case exposes either the method's core insight or a failure mode.
The seed is to generalize from that case.

### 5.6 Successor-paper gap

Later work uses the paper but leaves a limitation unresolved.
The seed is to solve the unresolved limitation with updated tools or settings.

### 5.7 Reviewer objection

A reviewer-grade weakness becomes a concrete research plan.

### 5.8 Negative result

A surprising failure, if carefully analyzed, may be publishable because it changes understanding.

### 5.9 Cross-domain transfer

A mechanism works in one field but has not been tested in another field where the same hidden assumption fails.

## 6. Minimum Viable Experiment Pattern

Each strong seed should include:

1. **Setup**: smallest dataset, benchmark, theorem case, synthetic environment, or controlled reproduction.
2. **Intervention**: the one mechanism or assumption to change.
3. **Comparison**: baseline, ablation, or prior method.
4. **Metric**: the number, proof property, or qualitative outcome that decides the question.
5. **Decision rule**: what result supports, weakens, or kills the direction.
6. **Negative-result interpretation**: why failure still teaches something.

## 7. Killer Objection and Killer Result

A direction is stronger when it survives a serious objection.

For every top seed, write:

- `killer_objection`: the best reason the idea may be trivial, already solved, untestable, too expensive, or not impactful
- `killer_result`: the smallest result that would make the direction compelling

## 8. Direction Board Output Contract

Each seed in `direction_board.json` should include:

- `seed_id`
- `title`
- `seed_type`
- `trigger_interpretation_type`
- `paper_anchor_claim_ids`
- `trigger_evidence_summary`
- `hidden_assumption_or_gap`
- `research_question`
- `hypothesis`
- `proposed_mechanism`
- `minimum_viable_experiment`
- `negative_result_interpretation`
- `killer_objection`
- `killer_result`
- `first_week_plan`
- `score`
- `risk_level`
- `expected_value`
- `confidence`

## 9. Honesty Rules

- Do not claim a direction is novel unless checked against available sources.
- Do not claim author intent as fact.
- Do not turn every weakness into a high-value idea; many weaknesses are merely engineering cleanup.
- Do not ignore negative results; they can reveal the true boundary of a method.
- Mark missing evidence and search limitations explicitly.
