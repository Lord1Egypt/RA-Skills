# Infinite Research + Hidden NO

## Overview

This skill enables structured, verified reasoning through a master loop that combines research, debugging, verification, and refinement. Instead of generating answers directly, it investigates, verifies, stabilizes, and delivers reliable conclusions. The framework is designed to detect hidden blockers (Hidden NOs) that prevent premature finalization and to manage iteration budgets to prevent endless optimization.

## Core Workflow: The Master Loop

The framework operates through this sequential process:

1. **Understand** - Identify the user's true objective, explicit and implicit intent, constraints, ambiguity level, and whether research is required.
2. **Decide Tools** - Determine whether tools or external research are needed for verification and accuracy.
3. **Research** - Gather supporting evidence, contradicting evidence, alternative interpretations, and official documentation.
4. **Synthesize** - Construct reasoning that prioritizes stability, usefulness, evidence quality, contextual fit, clarity, and internal consistency.
5. **Test Reasoning** - Internally verify that the solution addresses the user objective and that assumptions are justified.
6. **Debug** - Search for logical contradictions, weak assumptions, unsupported conclusions, and hidden ambiguity.
7. **Detect Hidden NO** - Identify any reason the current reasoning should NOT yet finalize.
8. **Refine** - Isolate weak layers and refine only what is unstable.
9. **Deliver** - Provide the final result with key findings, remaining uncertainty, and confidence level.
10. **Store Lesson** - Preserve high-value lessons and reusable patterns for future synthesis.

## When to Use This Skill

Apply this skill when:

- **Research verification is critical** - Information may be outdated, external verification matters, or evidence quality is important.
- **Contradictions must be detected** - Multiple perspectives exist or assumptions may conflict with facts.
- **Reasoning must be debugged** - Logical flaws, weak assumptions, or unsupported conclusions need identification.
- **Stability matters more than speed** - The cost of an incorrect answer exceeds the cost of slower verification.
- **High-risk decisions** - The user explicitly requests depth or the task involves significant consequences.
- **Complex synthesis** - Multiple sources, perspectives, or interpretations must be reconciled.

## Key Concepts

### Tool-Awareness Layer

Decide strategically whether tools or external research are needed. Use research/tools when:

- Information may be outdated
- External verification matters
- APIs or frameworks may have changed
- Evidence quality matters
- Technical accuracy is important
- Source comparison is necessary

Never assume tool outputs are correct without verification.

### Budget Control

Manage internal limits to prevent endless optimization:

- **Max research loops:** 3
- **Max debug loops:** 3
- **Max refinement loops:** 3
- **Max speculative assumptions:** 3

Escalate only if the task is high-risk, the user explicitly requests depth, or major Hidden NO remains unresolved.

### Hidden NO Detection

A Hidden NO is any reason the current reasoning should NOT yet finalize. Examples include:

- Contradiction
- Unsupported claim
- Weak sourcing
- Instability
- Misunderstood intent
- Hidden risk
- Shallow analysis
- False certainty
- Premature synthesis
- Incomplete verification

Assign severity levels:

| Severity | Meaning | Action |
| --- | --- | --- |
| 0 | No issues | Finalize if stable |
| 1 | Minor weakness | Finalize if stable; do not endlessly loop |
| 2 | Meaningful issue | Refine reasoning and re-evaluate |
| 3 | Major blocker | Do NOT finalize; research deeper or revise assumptions |

### Memory Layer

After completion, preserve only high-value lessons:

**Store:** Reusable patterns, recurring user preferences, important constraints, failed assumptions, strong reasoning structures, validated insights.

**Ignore:** Noise, trivial details, one-off irrelevant facts.

**Priority:** High = reusable and important; Medium = useful soon; Low = discard.

### Stop Condition

Finalize when:

- The user objective is sufficiently solved
- No Hidden NO ≥ 2 remains
- Evidence is stable enough
- Uncertainty is acceptable
- Further iteration would provide diminishing returns

The goal is stable usefulness, not infinite perfection.

## Output Format

Default output includes:

```
Result:
[Primary answer or conclusion]

Key Findings:
[Main discoveries and insights]

Remaining Uncertainty:
[Unresolved questions or limitations]

Confidence:
[low / medium / high]

Hidden NO Status:
[Summary of any detected issues and how they were resolved]

TLDR:
[Too Long; Didn't Read summary]
```
