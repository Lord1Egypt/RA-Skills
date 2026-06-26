---
name: karpathy-guidelines
description: engineering execution guardrails for coding, implementing features, fixing bugs, debugging failures, reviewing diffs, refactoring code, simplifying overbuilt solutions, and planning multi-step code changes. use for choosing implementation approaches, editing code safely, reviewing correctness and scope, reducing unnecessary complexity, surfacing hidden assumptions, deciding what belongs in deterministic code rather than model judgment, defining concrete verification steps, and keeping software tasks to the smallest effective change.
---

# Karpathy Guidelines

Apply this skill to non-trivial software engineering work. The goal is to produce smaller, safer, more verifiable changes with fewer hidden assumptions.

For trivial edits such as a typo, a one-line mechanical rename, or an obvious localized fix, use judgment and do not add ceremony.

## Default operating loop

For non-trivial tasks, follow this sequence:

1. Restate the task in concrete engineering terms.
2. Read the nearest relevant callers, utilities, tests, and conventions before editing.
3. Name the assumptions or ambiguities that could change the implementation.
4. Choose the smallest viable approach.
5. Make only the changes required for that approach.
6. Verify the result with concrete checks.
7. Report what changed, how it was verified, and any remaining uncertainty.

When useful, think in this compact frame before acting:

- **assumptions:** what must be true
- **read:** the nearby evidence that guides the change
- **plan:** the minimum set of steps
- **verify:** the checks that define success

## Core rules

### 1. Think before coding

Do not silently pick an interpretation when the request is ambiguous.

- State assumptions that materially affect design or code changes.
- Surface the main options when multiple interpretations would lead to different implementations.
- Prefer the lower-risk interpretation when it still satisfies the request.
- Stop and call out conflicts between the request, the prompt, and the codebase.
- Push back on complexity when a simpler path clearly achieves the goal.

### 2. Simplicity first

Implement the minimum change that solves the actual problem.

- Do not add features that were not requested.
- Do not add abstractions for a single use case unless the local codebase already needs that pattern.
- Do not introduce flags, extension points, or configuration without a present need.
- Prefer straightforward control flow over cleverness.
- Prefer the substantially smaller solution when two options achieve the same result.

Use this test: would a strong senior engineer call this overbuilt for the current requirement? If yes, simplify.

### 3. Surgical changes

Touch only what the request requires.

- Do not refactor adjacent code just because you noticed something better.
- Do not reformat, rename, or reorganize unrelated code.
- Match existing local style and patterns unless the task explicitly asks for a broader change.
- Remove imports, variables, functions, or files that become unused because of your own change.
- Mention unrelated dead code or separate bugs without changing them unless they block the requested work.

Every changed line should trace back to the request or to a direct dependency of the request.

### 4. Goal-driven execution

Convert vague requests into verifiable outcomes.

- For bug fixes: reproduce or isolate the failure, apply the fix, then verify the failure is gone.
- For new features: define observable acceptance checks before implementation.
- For refactors: preserve behavior with tests, builds, or focused before-and-after checks.
- For risky edits: prefer incremental steps with verification after each step.
- For multi-step tasks: say what each step will prove before moving on.
- Write tests that assert the intended behavior or invariant, not just tests that execute the changed code.

Weak success criteria such as "make it work" are not enough. Anchor the work to a checkable result.

### 5. Agent-era discipline

Treat coding agents as accelerators for engineering work, not as a place to hide deterministic product logic.

- Put parsing, validation, routing, migrations, retry policy, and other deterministic decisions in code or tests instead of relying on model judgment.
- Read local code before writing. Nearby callers, helper functions, fixtures, and error paths are usually more authoritative than a generic plan.
- When the codebase shows conflicting patterns, expose the conflict and choose a specific precedent instead of averaging them together.
- Make skipped work visible. If tests, data, migrations, tool output, or credentials are unavailable, say exactly what was skipped and why.
- For long agent loops, checkpoint before continuing: summarize what has been tried, what evidence changed, and what the next verification step proves.
- Prefer explicit failure over silent fallback when missing data or ambiguous state would make the result misleading.

## Task-specific guidance

### When implementing code

- Prefer the smallest diff that meets the requirement.
- Reuse existing utilities before creating new ones.
- Keep existing comments unless they become inaccurate because of your change.
- Do not broaden API surface area without a demonstrated need.
- Do not use an LLM call as a hidden parser, validator, or policy engine when ordinary code can express the rule.

### When debugging

- Narrow the failure mode before changing code.
- Prefer evidence from tests, logs, traces, or a minimal reproduction over guesswork.
- Separate confirmed facts from hypotheses.
- After fixing, verify both the target bug and the nearest likely regression boundary.
- If a tool, fixture, or environment dependency fails, surface that failure instead of treating missing evidence as success.

### When reviewing code

- Focus first on correctness, simplicity, scope control, and verification.
- Flag hidden assumptions, unnecessary abstractions, and unrelated changes.
- Flag silent fallbacks, unverifiable claims, and places where deterministic behavior depends on model judgment.
- Distinguish must-fix issues from optional improvements.
- Prefer comments that point to concrete risk or a simpler alternative.

### When planning work

- Offer the minimum viable plan first.
- Include explicit verification points.
- Mention tradeoffs only when they materially affect implementation or risk.
- Avoid speculative future-proofing unless the task is explicitly about architecture.
- For long tasks, define checkpoint moments where the plan can be corrected using fresh evidence.

## Response expectations

For non-trivial engineering tasks, the final response should usually include:

- what changed or what should change
- the key assumption or tradeoff, if any
- how the result was verified or should be verified
- any remaining risk, uncertainty, or directly relevant follow-up

Keep the response concise. Let the discipline show up in the work rather than in long explanations.
