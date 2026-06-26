# CODE SIMPLIFICATION CHECKLIST

Guidance for simplifying code during review and refactoring.
Complements references/mechanical-enforcement.md (which enforces rules automatically).

---

## FIVE PRINCIPLES

### 1. Preserve Behavior Exactly
Don't change what the code does -- only how it expresses it.
All inputs, outputs, side effects, error behavior, and edge cases must remain
identical. If you're not sure a simplification preserves behavior, don't make it.

### 2. Follow Project Conventions
Simplification means making code more consistent with the codebase, not imposing
external preferences. Before simplifying:
- Read CLAUDE.md / project conventions
- Study how neighboring code handles similar patterns
- Match the project's style for imports, declarations, naming, errors, types

### 3. Prefer Clarity Over Cleverness
Explicit code is better than compact code when the compact version requires a
mental pause to parse.

### 4. Maintain Balance
Watch for over-simplification traps:
- Inlining too aggressively (removing a helper that gave a concept a name)
- Combining unrelated logic (two simple functions merged into one complex function)
- Removing "unnecessary" abstraction that exists for extensibility or testability
- Optimizing for line count (fewer lines != simpler)

### 5. Scope to What Changed
Default to simplifying recently modified code. Avoid drive-by refactors of
unrelated code unless explicitly asked. Unscoped simplification creates noise
in diffs and risks unintended regressions.

---

## SIMPLIFICATION PATTERNS

### Structural Complexity

| Pattern | Signal | Simplification |
|---------|--------|----------------|
| Deep nesting (3+ levels) | Hard to follow control flow | Extract conditions into guard clauses or helpers |
| Long functions (50+ lines) | Multiple responsibilities | Split into focused functions with descriptive names |
| Nested ternaries | Requires mental stack to parse | Replace with if/else chains, switch, or lookup objects |
| Boolean parameter flags | `doThing(true, false, true)` | Replace with options objects or separate functions |
| Repeated conditionals | Same `if` check in multiple places | Extract to a well-named predicate function |

### Naming and Readability

| Pattern | Signal | Simplification |
|---------|--------|----------------|
| Generic names | `data`, `result`, `temp`, `val` | Rename to describe content: `userProfile`, `validationErrors` |
| Abbreviated names | `usr`, `cfg`, `btn` | Use full words unless universal (`id`, `url`, `api`) |
| Misleading names | Function named `get` that mutates | Rename to reflect actual behavior |
| Comments explaining "what" | `// increment counter` above `count++` | Delete -- code is clear enough |
| Comments explaining "why" | `// Retry because API is flaky under load` | Keep -- carries intent code can't express |

### Redundancy

| Pattern | Signal | Simplification |
|---------|--------|----------------|
| Duplicated logic | Same 5+ lines in multiple places | Extract to a shared function |
| Dead code | Unreachable branches, unused variables | Remove (after confirming truly dead) |
| Unnecessary abstractions | Wrapper that adds no value | Inline the wrapper, call underlying directly |
| Over-engineered patterns | Factory-for-a-factory | Replace with simple direct approach |
| Redundant type assertions | Casting to a type already inferred | Remove the assertion |

---

## CHESTERTON'S FENCE

Before changing or removing anything, understand why it exists. If you see a fence
across a road and don't understand why it's there, don't tear it down. First
understand the reason, then decide if the reason still applies.

Before simplifying, answer:
- What is this code's responsibility?
- What calls it? What does it call?
- What are the edge cases and error paths?
- Are there tests that define the expected behavior?
- Why might it have been written this way?
- Check git blame: what was the original context?

If you can't answer these, you're not ready to simplify. Read more context first.

---

## THE RULE OF 500

If a refactoring would touch more than 500 lines, invest in automation (codemods,
sed scripts, AST transforms) rather than making changes by hand. Manual edits at
that scale are error-prone and exhausting to review.

---

## SIMPLIFICATION CHECKLIST

After each simplification:
- [ ] All existing tests pass without modification
- [ ] Build succeeds with no new warnings
- [ ] Linter/formatter passes
- [ ] Each simplification is a reviewable, incremental change
- [ ] The diff is clean -- no unrelated changes mixed in
- [ ] Simplified code follows project conventions
- [ ] No error handling was removed or weakened
- [ ] No dead code left behind
