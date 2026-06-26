# Figure Pattern Library

Use these evidence-backed patterns to build inspiration/case figures. Pick one primary pattern, keep secondary labels as constraints, then move through the mandatory visual candidate bridge.

## Patterns

1. **Single-Case Hook**
   - Use for a first figure that shows one memorable example.
   - Shape: concrete input/context -> problematic behavior -> insight label -> paper need.
   - Risk: becoming anecdotal; attach the case to the paper's general claim.

2. **Failure Chain**
   - Use when the motivation is a breakdown, hallucination, bias, brittleness, unsafe behavior, or limitation.
   - Shape: trigger -> existing method state -> failure observation -> consequence -> proposed need.
   - Risk: implying the paper fully solves the failure if it only studies the boundary.

3. **Before/After Split**
   - Use when the figure needs instant contrast between existing and desired behavior.
   - Shape: left lane "current/baseline" and right lane "desired/proposed"; keep input constant.
   - Risk: unfair baseline caricature; use labels backed by the paper.

4. **Observation Ladder**
   - Use for an empirical or qualitative observation that inspires a hypothesis.
   - Shape: observed phenomenon -> recurring pattern -> inferred principle -> method implication.
   - Risk: weak causality; label as observation/hypothesis unless evidence proves causation.

5. **Scenario Storyboard**
   - Use for user-facing, robotics, agent, multimodal, or system papers where context matters.
   - Shape: 3-5 panels with actor, environment, task, friction, desired resolution.
   - Risk: too illustrative for technical venues; keep labels technical and compact.

6. **Evidence Tile Board**
   - Use for rebuttal, result teaser, or claim support.
   - Shape: central inspiration claim surrounded by compact evidence cards.
   - Risk: invented metrics; include only supplied metrics, outputs, or qualitative examples.

7. **Design-Space Gap Map**
   - Use when the inspiration is a missing quadrant, axis, category, or unserved regime.
   - Shape: matrix, axis map, or grouped tiles with highlighted gap.
   - Risk: arbitrary axes; every axis must be paper-justified.

8. **Mechanism Spark**
   - Use when the inspiration is an intuition, analogy, or causal mechanism.
   - Shape: simple causal chain or variable interaction, plus a small "why it matters" callout.
   - Risk: replacing the method with metaphor; keep the method link explicit.

9. **Reviewer Concern Case**
   - Use for rebuttal or limitation figures.
   - Shape: concern -> concrete case -> boundary/evidence -> paper stance.
   - Risk: overclaiming; state the boundary honestly.

## Multi-Label Pattern Mixing

- case walkthrough + failure map: story panels are primary, failure labels are secondary.
- failure map + evidence board: limitation taxonomy is primary, supplied evidence cards support each node.
- design-space gap + before/after: axis map is primary, contrast is a highlighted inset.
- mechanism spark + case hook: one case travels through the causal chain.
- scenario storyboard + method teaser: scenario is primary, method appears only as the answer to the problem.

## Prompt Pattern

Each generated image brief should state:

- selected pattern;
- fixed figure thesis and paper slot;
- exact labels allowed;
- what varies across candidates;
- sample-image transfer rules, if any;
- forbidden elements and no-code-rendering rule.
