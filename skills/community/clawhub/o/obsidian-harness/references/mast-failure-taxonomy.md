# MAST Failure Taxonomy for Multi-Agent Systems

Classify failures into three categories to determine the correct fix:

## Three Failure Types

| Type | Share | Symptoms | Fix Direction |
|---|---|---|---|
| **Design** | ~40% | Wrong task decomposition, unclear agent boundaries, bad tool selection | Redesign architecture and task splitting |
| **Alignment** | ~35% | Agent understood the task but drifted, wrong output format, creatively bypassed constraints | Improve prompts, add constraints, refine acceptance criteria |
| **Verification** | ~25% | Output looks correct but isn't, missing quality checks, errors amplified downstream | Add Verification Agent, set quality gates |

## Diagnostic Five-Question Protocol

When a multi-agent task fails:

1. **What did the agent believe was happening?** (task understanding) → Alignment issue
2. **What tools were called, in what order?** (execution path) → Design issue
3. **What signal was missing?** (information gap) → Design issue
4. **Which guardrail should have caught this?** (missing protection) → Verification issue
5. **How can we detect this faster next time?** (observability) → All types

## Key Insight

65% of multi-agent failures (Design + Verification) have nothing to do with model capability. Switching to a stronger model won't fix them. Only 35% (Alignment) might benefit from a better model or better prompts.

**Fix the harness first, then consider the model.**
