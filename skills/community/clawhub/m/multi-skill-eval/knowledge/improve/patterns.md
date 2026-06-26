# Improvement Strategies (Proven Playbooks)

## Strategy 1: Reference Manual Slim-Down
**Problem**: >200 lines of educational content, agent skips most of it
**Solution**: Delete 70%+ redundant content, replace with behavioral mandates
**When to use**: SKILL.md reads like a textbook, not a skill

**Steps**:
1. Identify which paragraphs describe WHAT the agent should do vs WHY
2. Delete all "why" and "background" content (keep <30% of original)
3. Add MUST/ALWAYS/NEVER directives
4. Add quick-mode routing for simple cases

**Example transformation**:
Before: "The agent should first analyze the database schema, considering the relationships between tables, then carefully examine the indexes, taking into account the query patterns..."
After: "MUST analyze schema before querying. ALWAYS check index coverage for WHERE clauses."

## Strategy 2: Library-to-Instructions
**Problem**: SKILL.md contains Python/JS class definitions instead of behavioral instructions
**Solution**: Convert code to step-by-step behavioral guidance
**When to use**: Skill is a "library" with classes and methods

**Steps**:
1. Identify each function/class purpose
2. Rewrite as: "When [trigger], do [step 1] → [step 2] → [step 3]"
3. Remove implementation details
4. Keep only the behavioral contract

## Strategy 3: Phantom Tooling Replacement
**Problem**: SKILL.md references scripts/binaries that don't exist in the package
**Solution**: Replace tool references with equivalent inline instructions
**When to use**: Phantom tooling detected during eval

**Steps**:
1. List all referenced but missing tools
2. For each: write equivalent step-by-step instructions
3. Replace tool call with inline instructions
4. Add graceful fallback for missing dependencies

## Strategy 4: Overhead Routing
**Problem**: High time/token cost with marginal quality gain
**Solution**: Add fast-path routing for simple cases
**When to use**: Quality delta ≈ 0 but cost delta >2x

**Steps**:
1. Identify which use cases are simple (can be handled by baseline)
2. Add conditional: "If [simple case], skip full workflow"
3. Add lightweight alternative for simple cases
4. Keep full workflow only for complex cases

## Strategy 5: Assertion-Aligned Rewrite
**Problem**: Skill fails specific assertions that represent real regressions
**Solution**: Rewrite specifically to pass the failed assertions
**When to use**: Score < 7 due to specific, fixable failures

**Steps**:
1. List all failed assertions with their root cause
2. For each failure: identify which part of SKILL.md causes it
3. Rewrite that section to satisfy the assertion
4. Re-run assertions — if still failing, dig deeper into root cause

## Anti-Pattern Recovery

| Anti-Pattern | Detection | Fix |
|--------------|-----------|-----|
| Reference Manual | Body >200 lines, no behavioral verbs | Delete 70%+, add MUST/ALWAYS |
| Library-as-Skill | Code in SKILL.md | Convert to instructions |
| Phantom Tooling | Missing scripts | Replace with inline instructions |
| Framework Inflation | Cost >2x, delta ≈ 0 | Add quick-mode routing |
| Unsubstantiated Claims | "7.8x faster" without evidence | Remove or add evidence |