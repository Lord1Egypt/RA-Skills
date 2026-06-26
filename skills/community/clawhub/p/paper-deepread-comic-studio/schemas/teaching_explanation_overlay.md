# Teaching-Explanation Overlay

This overlay turns a rigorous paper deep-read into material that can be taught, discussed, and defended.
It is a non-weakening overlay: every original deep-read, formula-preservation, proof-to-practice, figure/table, reviewer, OpenReview, research-generative, validation, and handoff requirement remains mandatory.

## Core principle

A paper is ready to teach only when the reader can answer five questions without hiding the hard parts:

1. What problem did the paper make important?
2. What assumption breaks in the target setting?
3. What ideal mechanism would solve the problem but is unavailable?
4. What surrogate mechanism does the paper build?
5. Which evidence supports the surrogate, and where can it fail?

Every key concept should be taught in the same four-step order:

```text
直觉 -> 数学公式或 formal definition -> 具体例子 -> 局限 / failure case
```

For complex modules, the teaching explanation must still name inputs, outputs, symbols, dimensions, training parameters, fixed hyperparameters, and training-vs-inference data flow. Simplify the language, not the factual content.

## Teaching equation

Use the same research equation, but translate it for a listener:

```text
Old success: A(P) works under assumption C.
New reality: target constraint T makes C false.
Almost-useful tool: method family M could help but needs unavailable mechanism Y.
Paper move: construct surrogate Z.
Evidence question: does Z behave enough like Y under the actual stress setting?
```

## Required teaching deliverables inside the authoritative report

### 1. Audience map

| Audience | Prior knowledge | Likely confusion | Best entry point | Math depth | Evidence needed |
|---|---|---|---|---|---|

### 2. Three-layer summary

- 30 seconds: one vivid, accurate story.
- 3 minutes: problem -> failed assumption -> core idea -> evidence -> caveat.
- 10 minutes: add method modules, key formula, main experiments, and limitations.

### 3. Story spine

```text
Before -> Pain -> Failed old assumption -> Key replacement -> Mechanism -> Evidence -> Caveat -> Next idea
```

### 4. Formula teaching table

| Formula | Plain-language purpose | Term-by-term explanation | Verbal script | Algorithm role | Fragility |
|---|---|---|---|---|---|

### 5. Figure/table teaching table

| Visual | First thing to point at | Claim supported | Misreading risk | What remains unclear | Verbal script |
|---|---|---|---|---|---|

### 6. Experiment teaching unit

For each experiment block:

- Question answered:
- Skeptical objection addressed:
- Setup/baselines/metrics:
- Expected result if claim is true:
- Actual result:
- What it proves:
- What it does not prove:
- One-sentence explanation of the table/curve:

### 7. Role-play discussion pack

| Role | Checks | Output |
|---|---|---|
| Archaeologist | ancestry and prior-work relation | cited ancestor, inherited assumption, modification |
| Bug Hunter | rigor and reproducibility | attack questions, likely author response |
| Researcher | future scientific value | follow-up projects and boundary idea |
| Industry Practitioner | deployability | adoption conditions and practical risk |
| Social Impact Assessor | broader impacts | positive and negative impacts |
| Author Defender | acceptance logic | strongest pitch and weakest claim |
| Teacher | learnability | analogy, prerequisites, teachback questions |

### 8. Q&A bank

| Question | Audience | Evidence-backed answer | Confidence | Report section / paper evidence |
|---|---|---|---|---|

### 9. Misunderstanding guardrails

- The paper does not claim:
- The analogy breaks when:
- The result should not be generalized to:
- The easiest-to-overinterpret baseline/result is:
- The limitation that must be stated aloud is:

### 10. Slide / talk blueprint

| Slide | Title | One-sentence point | Visual/formula | Speaker notes | Transition | Likely question |
|---|---|---|---|---|---|---|

### 11. Teachback self-test

Include 8-12 questions covering setting, assumption, method dataflow, formula, evidence, limitation, reviewer attack, and future direction.

### 12. Complete numeric training-to-inference example

Include one tiny numeric example that follows the method from input construction through a training loss/update and then through one inference decision. Mark any simplified toy values that are not paper-explicit.

## Output policy

The authoritative detailed report remains the single source of truth. Optional teaching sidecars may be generated, but only as derivatives from the authoritative report:

- `generated/teaching/<paper-slug>/teaching_outline_cn.md`
- `generated/teaching/<paper-slug>/slide_blueprint_cn.json`
- `generated/teaching/<paper-slug>/qa_bank_cn.json`
- `generated/teaching/<paper-slug>/role_play_discussion_pack_cn.md`

Sidecars must not introduce new unsupported claims.
