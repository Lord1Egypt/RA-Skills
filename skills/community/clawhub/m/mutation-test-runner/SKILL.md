---
name: mutation-test-runner
description: Run mutation testing to measure real test suite effectiveness. Inject code mutations (flip conditions, remove calls, change returns), run tests against mutants, and report mutation score — the truest measure of test quality beyond line coverage.
---

# Mutation Test Runner

Line coverage lies. 80% coverage with weak assertions catches nothing. Mutation testing injects real bugs into your code and checks whether your tests catch them — giving you a genuine measure of test suite quality.

Use when: "how good are our tests really", "mutation testing", "test suite quality", "are these tests actually catching bugs", "mutation score", or when line coverage is high but bugs still slip through.

## Commands

### 1. `run` — Execute Mutation Testing

#### Step 1: Detect Language and Test Framework

```bash
# Detect project language
ls package.json 2>/dev/null && echo "NODE"
ls pom.xml build.gradle 2>/dev/null && echo "JAVA"
ls setup.py pyproject.toml 2>/dev/null && echo "PYTHON"
ls go.mod 2>/dev/null && echo "GO"
ls Cargo.toml 2>/dev/null && echo "RUST"
```

#### Step 2: Install and Run Mutation Tool

**JavaScript/TypeScript (Stryker):**
```bash
npx stryker init 2>/dev/null || npm install --save-dev @stryker-mutator/core
npx stryker run --reporters clear-text,html 2>&1
```

If Stryker unavailable, manual mutation approach:
```bash
# Find test files
rg -l "describe\(|test\(|it\(" --type ts --type js -g '!node_modules' 2>/dev/null

# Find source files with tests
rg -l "export (function|class|const)" --type ts --type js \
  -g '!node_modules' -g '!*.test.*' -g '!*.spec.*' 2>/dev/null
```

**Python (mutmut):**
```bash
pip install mutmut 2>/dev/null
mutmut run --paths-to-mutate=src/ 2>&1
mutmut results 2>&1
```

**Java (PIT):**
```bash
# Maven
mvn org.pitest:pitest-maven:mutationCoverage 2>&1
# Gradle
./gradlew pitest 2>&1
```

**Go (gremlins):**
```bash
go install github.com/go-gremlins/gremlins/cmd/gremlins@latest
gremlins unleash 2>&1
```

#### Step 3: If No Tool Available — Manual Mutation

For any language, apply these mutation operators manually to critical files:

| Operator | Original | Mutant | What it tests |
|----------|----------|--------|---------------|
| Negate conditional | `if (x > 0)` | `if (x <= 0)` | Boundary checks |
| Remove call | `validate(input)` | `// removed` | Side effect coverage |
| Change return | `return true` | `return false` | Return value assertions |
| Flip boolean | `enabled = true` | `enabled = false` | Flag-dependent logic |
| Boundary | `i < arr.length` | `i <= arr.length` | Off-by-one coverage |
| Remove throw | `throw new Error()` | `// removed` | Error handling tests |
| Null return | `return result` | `return null` | Null safety tests |

For each mutation:
1. Apply the mutation to source code
2. Run the test suite
3. If tests PASS → mutation survived (test gap found!)
4. If tests FAIL → mutation killed (tests are effective)
5. Revert the mutation

```bash
# Example: mutate a function and run tests
cp src/validator.js src/validator.js.bak
# Apply mutation (e.g., flip a condition)
sed -i 's/if (age >= 18)/if (age < 18)/' src/validator.js
npm test 2>&1
RESULT=$?
# Restore original
mv src/validator.js.bak src/validator.js
if [ $RESULT -eq 0 ]; then
  echo "⚠️  SURVIVED: flipping age check — no test catches this!"
else
  echo "✅ KILLED: tests caught the flipped condition"
fi
```

#### Step 4: Analyze Results

```markdown
# Mutation Testing Report

## Summary
- **Mutation score:** 72% (target: 80%+)
- **Total mutants:** 145
- **Killed:** 104 (tests caught the bug)
- **Survived:** 38 (test gaps!)
- **Timed out:** 3 (infinite loops — likely caught)

## Survived Mutants (test gaps)
### Critical (business logic)
1. `src/billing/calculator.js:47` — Changing `>=` to `>` not caught
   → Missing boundary test for exact threshold value

2. `src/auth/validator.js:23` — Removing `validateToken()` call not caught
   → No test verifies token validation actually runs

3. `src/api/handler.js:91` — Changing `return 403` to `return 200` not caught
   → Authorization test doesn't check response status code

### Recommendations
1. Add test: `expect(calculate(100)).toBe(...)` for exact boundary
2. Add test: verify `validateToken` is called (spy/mock)
3. Fix auth test: assert response.status === 403

## File-Level Mutation Scores
| File | Mutants | Killed | Score | Priority |
|------|---------|--------|-------|----------|
| src/billing/calculator.js | 23 | 12 | 52% | 🔴 Critical |
| src/auth/validator.js | 18 | 14 | 78% | 🟡 Medium |
| src/api/handler.js | 31 | 28 | 90% | 🟢 Good |
```

### 2. `suggest` — Generate Tests for Surviving Mutants

For each surviving mutant, generate the specific test that would kill it:

```javascript
// Surviving mutant: src/billing/calculator.js:47
// Mutation: changed >= to >
// Generated test:
test('calculates discount at exact threshold', () => {
  // The boundary value that the mutation changes behavior for
  expect(calculateDiscount(100)).toBe(10); // exactly at threshold
  expect(calculateDiscount(99)).toBe(0);   // just below
  expect(calculateDiscount(101)).toBe(10); // just above
});
```

### 3. `baseline` — Establish Mutation Score Baseline

Run mutation testing and save results as a baseline for tracking improvement over time. Set a minimum mutation score gate for CI.
