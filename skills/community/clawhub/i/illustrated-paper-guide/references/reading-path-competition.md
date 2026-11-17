# Reading Path Competition and Source Review

Use this workflow only for a new full paper guide or a material redesign of an
existing guide. Focused questions and local edits stay single-reader.

## Shared Source Inventory

Before proposing routes, the main agent creates one mechanical inventory that
all readers share:

- canonical paper version and paper type;
- top-level sections and claim-bearing subsections;
- decisive figures and tables, central equations, and appendices or
  supplements that materially affect the conclusion;
- abstract and conclusion claims;
- methods or model assumptions;
- stated limitations and negative results.

The inventory prevents repeated clerical work. Route readers still inspect the
source independently when deciding order and evidence dependencies.
Split panels only when they support distinct claims. Group procedural or
reference-only supplementary material so inventory work does not dominate
paper reading.

## Candidate Route Lenses

Assign different objectives explicitly. Do not ask several readers for the
same generic "best reading order."

### Argument-first

Optimize the fastest correct causal story:

```text
problem -> gap -> proposed mechanism -> main result -> significance -> limits
```

### Evidence-first

Optimize the fastest source-grounded assessment:

```text
main claims -> decisive figures or derivations -> controls and methods
-> assumptions -> limitations
```

### Learner- or goal-first

Optimize cognitive load for the reader's background and goal:

```text
minimum prerequisites -> simplest example -> concept dependencies
-> mechanism -> difficult math or figures -> research transfer
```

Use the third lens for complex papers. With two route readers, keep one route
argument-first and make the other learner/evidence-first according to the
paper's main difficulty.

## Candidate Output Schema

Each route proposal must contain:

1. objective and intended reader;
2. ordered passes with exact sections, figures, tables, or equations;
3. the learning output expected from every pass;
4. prerequisite and dependency reasons for the order;
5. a shallow stopping point and estimated effort;
6. cumulative effort at each stopping point;
7. deferred source items, why they are deferred, and when they return;
8. source-inventory IDs covered in each pass;
9. the route's largest likely misunderstanding.

Agents propose only. They do not edit the guide, checklist, coverage ledger, or
the user's completion marks.

## Comparison Rubric

Reject a route before scoring if it fails any hard gate:

- a central claim lacks an evidence location;
- a source section or major visual has no disposition;
- methods, controls, assumptions, negative results, or limitations disappear
  rather than return in a later pass;
- author interpretation is presented as direct observation;
- a model result is presented as a biological demonstration without evidence;
- the route pre-checks work the reader has not completed.

Score surviving routes with this default weighting:

| Criterion | Weight |
| --- | ---: |
| Time to the first correct mental model | 25% |
| Major-claim coverage | 20% |
| Evidence traceability | 20% |
| Assumption and limitation coverage | 15% |
| Prerequisite burden | 10% |
| Stop, resume, and self-test quality | 10% |

The main agent normally synthesizes rather than selecting one route verbatim.
A useful pattern is argument-first orientation, learner-first conceptual
scaffolding, and evidence-first deep reading. Do not concatenate every proposal
into one oversized sequence.

## Progressive Route Contract

The merged route should be monotonic: later passes add precision, evidence, and
critical depth without revealing the central conclusion for the first time.

| Level | Typical outcome | Required planning fields |
| --- | --- | --- |
| L0 Orientation | State problem, approach, main claim, and scope boundary. | exact targets, estimated and cumulative effort, stop point |
| L1 Conceptual spine | Reconstruct the whole story with minimum vocabulary. | exact targets, estimated and cumulative effort, stop point |
| L2 Claims and evidence | Read core mechanisms, results, and decisive visuals. | exact targets, estimated and cumulative effort, stop point |
| L3 Technical depth | Inspect methods, equations, controls, and assumptions. | exact targets, estimated and cumulative effort, stop point |
| L4 Critical coverage | Audit alternatives, limitations, supplements, and open questions. | exact targets, estimated and cumulative effort, stop point |

Every level names exact targets, an observable output, a stop point, and
deferred items. If deeper reading invalidates an earlier simplification, repair
the earlier layer rather than leaving contradictory explanations.

## Independent Source Review

After the main agent merges the route and drafts the guide, a non-author reader
checks the original paper, inventory, coverage ledger, and guide. The reviewer
looks for:

- central claims without evidence mapping;
- omitted decisive figures, controls, negative results, or qualifications;
- undisclosed assumptions;
- correlation written as causation;
- simulations or model behavior written as biological evidence;
- author interpretation written as direct measurement;
- supplements or appendices that materially change the conclusion;
- contradictions between the guide and source;
- deferred content with no return pass.
- core figures that are link-only even though reuse rights and repository
  policy allow a readable local embed;
- missing or incorrect figure files, figure/version mismatches, unreadable
  rendered text, cropped-out panel letters, axes, units, legends, scale bars,
  or claim-bearing annotations;
- missing nearby attribution, canonical source, license or permission basis,
  or crop/adaptation disclosure.

Source-grounding, coverage, and causal-overstatement findings are blocking.
Figure availability, identity, readability, completeness, and attribution
findings are also blocking for core figures. A documented link-only fallback
is acceptable when embedding is not legally or technically permitted.
Wording or layout suggestions are non-blocking unless they change meaning.
Resolve blockers and stabilize guide headings before generating the checklist.
After checklist generation, the main agent performs a final mechanical check
of anchors, exact link labels, and retrieval-based completion criteria; this
does not require a second full source review.

## Compact Coverage Ledger Template

```markdown
# Coverage ledger: [paper title]

| ID | Source locator | Kind | Importance | Paper states | Evidence type | Guide anchor | Disposition | Guide state | Review | Reason / uncertainty |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CLM-01 | Abstract; Results section | claim | core | | | | L0 and L2 | mapped | pending | |
| FIG-01A | Figure 1A | figure | core | | | | L2 | explained | pending | |
| ASM-01 | Methods | assumption | core | | | | return in L3 | inventoried | pending | |
| LIM-01 | Discussion | limitation | core | | author interpretation | | L4 | mapped | pending | |
```

IDs should remain stable when prose changes. Keep learner progress in
`CHECKLIST.md`; do not add hundreds of inventory rows to the reading checklist.

Before shipping:

- central claims are mapped to evidence;
- decisive figures or tables are explained now or assigned a later level;
- scope-changing assumptions and limitations appear in the guide;
- every core or in-scope row has `Review = pass`;
- deferred and out-of-scope dispositions have `Review = pass`;
- no row has `Review = pending` or `Review = blocker`;
- every out-of-scope disposition includes a reason.
