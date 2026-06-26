# Adapter: Physics

Use this adapter when the paper's contribution depends on physical modeling, derivations from governing laws, approximations, asymptotic regimes, symmetries, or the link between theory and observables.

## What to prioritize

1. The physical question and the regime of validity.
2. Governing equations, conserved quantities, symmetries, or constraints.
3. Approximations, closures, perturbative steps, and where they enter.
4. Limiting cases and dimensional consistency.
5. Mapping between theoretical objects and observables.
6. Experimental, numerical, or phenomenological support if present.

## Questions to answer in the note

- What physical system or phenomenon is being modeled?
- In what regime should the result be trusted?
- Which approximation or scaling argument makes the derivation go through?
- What symmetry, conservation law, or boundary condition matters most?
- What does the result predict for measurable quantities?
- How does it connect to known theories or limiting cases?

## Minimum insertions into the note

Add or expand these sections:

### Problem setup

- physical system
- regime / scales / control parameters
- boundary or initial conditions if relevant

### Technical core

- governing equations
- derivation path
- approximation points
- limiting-case checks
- interpretation of key dimensionless groups if any

### Evidence

- comparison to experiment, simulation, or known exact result
- whether discrepancies are explained or ignored

## Special reading rules

- Preserve equations that carry the physical mechanism.
- Note where a derivation changes regime, drops terms, linearizes, coarse-grains, or assumes equilibrium.
- Check units or dimensions when they matter.
- Ask whether the result behaves correctly in simple or extreme limits.

## Typical failure patterns to watch for

- approximation introduced without a clear error discussion
- regime of validity left vague
- physical interpretation weaker than the mathematics suggests
- numerics or experiment not clearly aligned with the theoretical claim
- hidden dependence on boundary conditions or idealizations

## Reusable note prompts

- “The key physical approximation is …”
- “The result should be trusted in the regime …”
- “The derivation hinges on dropping … under the assumption …”
- “A useful limit check is …”
