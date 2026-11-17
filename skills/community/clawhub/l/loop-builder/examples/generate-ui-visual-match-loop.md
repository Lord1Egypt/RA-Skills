# Example: UI Visual-Match Loop

## Confirmed Context

- target screenshot: supplied by the user;
- current page: available in a local development environment;
- viewport: 1440 x 900;
- allowed scope: one page component and its styles;
- feedback: same-viewport screenshot plus human review;
- forbidden actions: dependency replacement, unrelated redesign, commit, push,
  or deployment.

## Recommended Artifact

A full `Plan-Execute-Verify` Loop package with a human visual-acceptance gate.

Why:

- the task has a repeatable render action;
- each screenshot provides comparable feedback;
- bounded style and component changes can correct the mismatch;
- final visual equivalence remains partly subjective.

## Derived Control

- start with three implementation iterations;
- each iteration targets the largest remaining mismatch;
- continue only when the screenshot comparison reveals a new bounded correction;
- stop early after two iterations without meaningful visual improvement;
- request the user's decision when the remaining mismatch depends on hidden
  design intent or brand preference.

## Logic Confirmation Card

```md
## Workflow confirmation
- Goal: match the supplied screenshot at 1440 x 900
- Non-goals: responsive redesign, dependency migration, deployment
- Artifact: full Loop package
- Primary pattern: Plan-Execute-Verify
- Phases: inspect -> plan one visual delta -> implement -> render -> compare
- Feedback: same-viewport screenshot and remaining-delta list
- Maximum iterations: 3, because render feedback is cheap and changes are reversible
- Early stop: 2 iterations without meaningful improvement
- Human gate: subjective final acceptance or missing design intent
- Forbidden actions: unrelated files, commit, push, deploy
```

The executable Planner, Maker, Checker, and Evaluator Prompts are generated only
after the user confirms this logic.
