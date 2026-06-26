# Figure Class Taxonomy

Use this taxonomy to route inspiration/case figure requests before writing prompts or generating images.

## Core Subtypes

| Subtype | Reader Question | Best Paper Slot | Required Decisions |
|---|---|---|---|
| Problem teaser | What concrete problem makes the paper necessary? | introduction / teaser / slides | protagonist or object, problem state, unmet need, one memorable visual hook |
| Motivating case walkthrough | How does one example reveal the research gap? | introduction / qualitative / appendix | example state, observation, failure or limitation, insight, method need |
| Failure-to-need map | Where does an existing approach fail and why does this paper intervene? | introduction / analysis / rebuttal | failure trigger, affected module/state, observed consequence, paper response |
| Before/after contrast | What changes from current practice to the desired/proposed state? | introduction / method teaser / slides | left/right conditions, comparison boundary, invariant inputs, changed behavior |
| Observation-to-hypothesis | What observation inspired the design principle or hypothesis? | introduction / analysis | observation, pattern, hypothesis, proposed design consequence |
| Scenario storyboard | What user/system/environment scenario exposes the problem? | introduction / human-centered systems / robotics / agents | actor, task, context, friction, desired interaction |
| Evidence-to-inspiration board | What compact evidence supports the inspiration claim? | introduction / results teaser / rebuttal | claim, supplied evidence cards, comparison boundary, conclusion |
| Taxonomy hook | Which design space or category map reveals a missing region? | introduction / related work / method | axes, categories, examples, highlighted gap |
| Mechanism spark | What intuition makes the idea plausible before the method details? | introduction / method | cause-effect chain, variable roles, mechanism contrast |
| Reviewer concern case | What concrete case resolves a likely reviewer concern? | rebuttal / limitation / appendix | concern, concrete example, boundary condition, paper's honest stance |

## Routing Axes

- Reader question: why the paper is needed, what case exposes the gap, what failure is unacceptable, what insight motivates the design.
- Paper slot: first figure, introduction teaser, method lead-in, analysis, limitation, rebuttal, slide.
- Evidence type: example, observation, failure, contrast, scenario, taxonomy, metric, qualitative output, proof intuition.
- Layout skeleton: single focal case, storyboard, split contrast, evidence tiles, design-space map, failure chain, mechanism mini-map.
- Density: teaser simple, paper-intro moderate, rebuttal/evidence dense.
- Multi-label status: record all applicable labels first, then one primary rendering subtype.

## Multi-Label Routing

Do not make the taxonomy exclusive. A single inspiration figure can be both a case walkthrough, failure map, evidence board, mechanism intuition, and method teaser. Record all applicable labels and explain which one is primary for the current reader effect. If labels conflict, prefer the one that best answers the user's target paper slot and reviewer question.

## Default Production Choice

If the target paper has a clear concrete example, default to `motivating_case_walkthrough`. If no concrete example is supplied but a failure or surprising observation exists, default to `failure_to_need` or `observation_to_hypothesis`. If only broad related-work gaps are available, default to `taxonomy_hook`.

## Evidence Lineage

This taxonomy is grounded in `references/evidence-lineage-summary.md`, which indexes claims back to the builder-run corpus and the inspiration/case subset.
