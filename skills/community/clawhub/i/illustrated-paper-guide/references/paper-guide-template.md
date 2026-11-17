# Paper Guide and Checklist Template

Use this template as a strong default, then adapt section depth to the paper and
the reader's goal.

## README.md

```markdown
# [Paper title]: illustrated study guide

> This is a study guide, not the original paper.
> Reading progress: [CHECKLIST.md](./CHECKLIST.md)

<a id="ckpt-bp1"></a>
## BP1 Problem: what is this paper trying to solve?

[Motivation, gap, and the question in plain language.]

<a id="ckpt-bp2"></a>
## BP2 Method: what did the authors do?

[Subjects/data, intervention or model, comparisons, and measurements.]

<a id="ckpt-bp3"></a>
## BP3 Conclusion: what should I remember?

[Three to six main results and one overall claim.]

<a id="ckpt-bp4"></a>
## BP4 Reading map

[Use the reviewed route. Name exact targets, output, stop point, and deferred
material for each pass.]

| Level | Read | Produce | Estimated effort | Cumulative effort | Stop when | Deferred material and return pass |
| --- | --- | --- | ---: | ---: | --- | --- |
| L0 Orientation | | | | | | |
| L1 Conceptual spine | | | | | | |
| L2 Claims and evidence | | | | | | |
| L3 Technical depth | | | | | | |
| L4 Critical coverage | | | | | | |

<a id="ckpt-l0"></a>
### L0 Orientation

[Exact source targets, expected output, effort, stop point, and deferred items.]

<a id="ckpt-l1"></a>
### L1 Conceptual spine

[Exact source targets, expected output, effort, stop point, and deferred items.]

<a id="ckpt-l2"></a>
### L2 Claims and evidence

[Exact source targets, expected output, effort, stop point, and deferred items.]

<a id="ckpt-l3"></a>
### L3 Technical depth

[Exact source targets, expected output, effort, stop point, and deferred items.]

<a id="ckpt-l4"></a>
### L4 Critical coverage

[Exact source targets, expected output, effort, stop point, and deferred items.]

<a id="ckpt-a1"></a>
## A1 Paper information

| Field | Value |
| --- | --- |
| Title | |
| Authors | |
| Venue and year | |
| DOI or canonical URL | |

[Continue with A-F sections appropriate to the paper.]

<a id="ckpt-e1"></a>
## E1 Figure [N]: [question answered by the complete figure]

![Figure N: concise accessible description](./images/figure-n-short-name.png)

> **Source:** [Authors, paper title, Figure N, exact version](canonical-url),
> [license or permission basis]. [Complete figure / cropped from PDF page N /
> adapted; describe modifications if any.]

1. **Read first:** [panel, axis, comparison, or visible region].
2. **Visible evidence:** [what is actually shown].
3. **Narrow conclusion:** [what this figure supports].
4. **Do not infer:** [tempting claim not established by the figure].

[If embedding is unavailable, replace the image with a direct source link and
state the legal or technical reason.]
```

## CHECKLIST.md

```markdown
# Reading checklist: [short paper title]

> Main guide: [README.md](./README.md)

## Top-down reading sequence

- [ ] [L0 Orientation](./README.md#ckpt-l0)
  **Targets and effort:** [Exact targets; estimated and cumulative effort.]
  **Done when:** I can state the problem, approach, main claim, and scope
  boundary without looking.

- [ ] [L1 Conceptual spine](./README.md#ckpt-l1)
  **Targets and effort:** [Exact targets; estimated and cumulative effort.]
  **Done when:** I can reconstruct the whole argument with the minimum required
  vocabulary.

- [ ] [L2 Claims and evidence](./README.md#ckpt-l2)
  **Targets and effort:** [Exact targets; estimated and cumulative effort.]
  **Done when:** I can map each central claim to its decisive result, figure,
  table, or derivation.

- [ ] [L3 Technical depth](./README.md#ckpt-l3)
  **Targets and effort:** [Exact targets; estimated and cumulative effort.]
  **Done when:** I can explain the methods, equations, controls, and assumptions
  that determine whether the conclusions hold.

- [ ] [L4 Critical coverage](./README.md#ckpt-l4)
  **Targets and effort:** [Exact targets; estimated and cumulative effort.]
  **Done when:** I can state the alternatives, limitations, deferred material,
  and open questions without overstating the evidence.

## Big Picture and detailed checkpoints

- [ ] [BP1 Problem: what is this paper trying to solve?](./README.md#ckpt-bp1)
  **Done when:** I can explain the gap without reading the abstract.

- [ ] [BP2 Method: what did the authors do?](./README.md#ckpt-bp2)
  **Done when:** I can name the data or subjects, comparison, and measurement.

- [ ] [BP3 Conclusion: what should I remember?](./README.md#ckpt-bp3)
  **Done when:** I can state the main result without overstating causality.

- [ ] [BP4 Reading map](./README.md#ckpt-bp4)
  **Done when:** I know the next source target, the expected output, the first
  safe stopping point, and where deferred material returns.
```

Generate this checklist only after route review and heading stabilization.
Preserve existing checked items as reading history when reorganizing a guide.
Do not pre-check work for the reader.

## COVERAGE.md

Use a separate author/reviewer ledger for a full new guide. A short, linear
paper may keep this as a compact table in `README.md` instead.

```markdown
# Coverage ledger: [paper title]

| ID | Source locator | Kind | Importance | Paper states | Evidence type | Guide anchor | Disposition | Guide state | Review | Reason / uncertainty |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CLM-01 | Abstract; Results | claim | core | | | | L0 and L2 | mapped | pending | |
| FIG-01A | Figure 1A | figure | core | | | | L2 | explained | pending | |
| ASM-01 | Methods | assumption | core | | | | return in L3 | inventoried | pending | |
| LIM-01 | Discussion | limitation | core | | author interpretation | | L4 | mapped | pending | |
```

Every central claim needs an evidence mapping. Every top-level section and
major visual needs a disposition. Deferred items require both a reason and a
later return level.

The guide is ready only when central claims map to evidence, decisive visuals
are explained or assigned a return level, scope-changing assumptions and
limitations appear in the guide, every core or in-scope row and every deferred
or out-of-scope disposition has review passing, pending and blocker rows are
zero, and every out-of-scope item has a reason.

## Stable Anchor Rules

- Put `<a id="ckpt-code"></a>` immediately above the linked heading.
- Start the heading with the same code used by the anchor.
- Keep the checklist label and heading identical character for character.
- Use one checkpoint per testable learning outcome, not per paragraph.
- If a heading changes, update the heading, anchor, and checklist together.

## Completion Criteria Patterns

Prefer observable outcomes:

- “I can draw the causal chain from memory.”
- “I can identify the control and explain why it matters.”
- “I can point to the panel region supporting the claim.”
- “I can separate the measured result from the authors' interpretation.”

Avoid vague outcomes such as “I understand this section.”
