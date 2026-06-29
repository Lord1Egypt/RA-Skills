---
name: programming-as-theory-building
description: "Use when writing, generating, modifying, debugging, reviewing, or refactoring code. Treat code work as rebuilding and preserving the program theory: how real-world affairs map into program behavior, why the current shape exists, which existing facility the new demand resembles, and what observable behavior proves the change belongs."
license: MIT
---

# Programming as Theory Building

Karpathy-style operating rules for Peter Naur's "Programming as Theory Building". Use these rules to avoid context-free patches, speculative abstractions, and code that only looks right as text.

**Tradeoff:** This skill slows down trivial edits. For non-trivial code, pay the small upfront cost so the change fits the program.

## Core Idea

Programming is not text production. The useful asset is the theory held by the programmer: how the program execution supports some real-world activity, why the program is shaped this way, and how it should change when the world changes.

Source code, tests, docs, and comments are evidence of that theory, not the theory itself.

## Before Coding

Answer these briefly before a non-trivial edit:

1. **World Mapping:** What real-world workflow, rule, protocol, or invariant is this code meant to support?
2. **Current Theory:** Why is the current code shaped this way? What names, tests, callers, data shapes, or runtime behavior reveal that?
3. **Similarity:** Which existing facility is the new demand most similar to? Where would a maintainer who knows the system expect it to live?
4. **Boundary:** What real-world cases are intentionally outside this program's scope?
5. **Proof:** What behavior, test, command, or review evidence would show the theory is now better supported?

If you cannot answer the first three, inspect more before patching.

## Workflow

### 1. Rebuild Only The Needed Theory

- Inspect the relevant code path, callers, callees, tests, fixtures, docs, names, and current runtime behavior.
- Prefer executable behavior over stale comments or stale docs when they conflict.
- Find at least one concrete example of how the code is used.
- Keep the theory compact: a few precise sentences, not an architecture essay.
- State uncertainty instead of hiding it.

### 2. Judge Similarity Before Placement

Naur's key modification question is not "where can I add this?" but "what existing world-facing capability is this most like?"

- Put behavior beside the closest existing domain concept.
- Use existing names, data shapes, validators, repositories, services, routes, UI patterns, and tests when they already encode the idea.
- Do not duplicate a domain concept under a new name.
- If the demand does not fit any existing facility, say why before creating one.

### 3. Keep Changes Surgical

- Make the smallest coherent change that preserves the theory.
- Touch only files required by the request.
- Match local style even if you would design it differently from scratch.
- Do not reformat, rename, reorganize, or modernize adjacent code as a side effect.
- Remove only dead code introduced by your change unless cleanup was requested.

### 4. Avoid Speculative Flexibility

Future flexibility is not free. Every option, config knob, adapter, interface, or abstraction must be designed, implemented, tested, and explained.

- No abstractions for one caller.
- No unused hooks, queues, providers, registries, plugins, or settings.
- No broad "just in case" error handling.
- Add flexibility only when the present theory already needs it or the local pattern clearly requires it.

### 5. Preserve Invariants, Not Just Tests

- Identify the invariant before changing behavior.
- Do not patch around a broken invariant with a special case.
- If several implementations pass the same narrow test, choose the one that keeps the design story easiest to explain.
- Add names, comments, or tests only when they carry theory that would otherwise be hidden.

### 6. Verify The Theory

- **Bug fix:** reproduce the violated invariant, then show it holds.
- **Feature or generated code:** verify the user-visible path and one meaningful edge case when practical.
- **Refactor:** verify behavior stayed the same.
- **Review:** report concrete risks, regressions, and missing tests with file references.

If verification contradicts the theory, rebuild the theory before adding another patch.

## Program Life Signals

Treat a program as "alive" when its theory can still be recovered and extended. Treat it as high-risk or "dead" when only text remains.

Stop and gather more context if:

- the change needs special cases that do not match existing names or boundaries,
- two areas encode the same domain concept differently,
- the obvious fix is a broad rewrite or speculative abstraction,
- the narrow test passes but the design story becomes harder to explain,
- the code's purpose cannot be mapped back to the real-world activity,
- the next step requires a product, domain, legal, security, or data decision the code cannot answer.

If the existing text is too far from any recoverable theory, say so. A rewrite may be cheaper than reviving dead code, but only after that risk is explicit.

## Review Checklist

When reviewing code, look for:

- code that satisfies a prompt but not the domain invariant,
- misplaced behavior that belongs in an existing facility,
- duplicated domain concepts under different names,
- speculative flexibility not justified by current requirements,
- tests that prove syntax or status codes but not the real-world behavior,
- docs that claim a theory the code does not implement.

## Response Shape

For non-trivial work, summarize briefly:

```text
Theory: [world rule -> program location]
Changed: [what changed]
Verified: [checks run]
Risk: [meaningful residual risk, if any]
```

For review-only work, lead with findings and file references. If there are no findings, say so plainly and note remaining test gaps or residual risk.
