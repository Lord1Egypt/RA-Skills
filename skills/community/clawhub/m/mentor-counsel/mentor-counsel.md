# SKILL: mentor-counsel

## Purpose
Provide strategic guidance to the developer with clarity, trade-offs, and risk framing — without dependency creation.

## When to Use
- The user is stuck, uncertain, or overwhelmed
- A strategic decision must be made (architecture, product, governance)
- The user asks for “what should I do” guidance

## Inputs
- `problem` (required): the decision or situation
- `context` (required): current state, constraints, timeline
- `constraints` (optional): non-negotiables (governance, security, budget, time)

## Steps
1. Reframe the problem (what is actually being decided).
2. Identify the real objective (success criteria + non-goals).
3. Present 2–3 viable paths.
4. Evaluate trade-offs per path:
   - time/cost
   - risk
   - reversibility
   - governance alignment
5. Recommend a direction and provide the next 1–3 actions.

## Validation
- Recommendation is consistent with stated constraints.
- Risks are explicit (no hidden assumptions).
- If confidence is low, say so and propose verification steps.

## Output
- `recommendation`
- `reasoning`
- `risks`
- `next_actions`

## Safety Rules
- No emotional manipulation.
- No false certainty; do not overclaim.
- Do not replace user judgment; return agency.

## Example
Input:
- problem: “Should we ship now or refactor first?”
- context: “Bug reports rising; limited time.”
Output:
- recommendation: “Ship a minimal fix with tests, then schedule refactor behind a flag.”
- risks: “Tech debt persists; mitigate with characterization tests.”

