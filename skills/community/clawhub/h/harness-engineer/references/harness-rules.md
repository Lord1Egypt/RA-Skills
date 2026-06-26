# HARNESS ENGINEERING RULES

These are the non-negotiable principles of harness engineering. They apply to every agent,
every cycle, every PR.

---

## CORE PRINCIPLES

### 1. DOCS ARE GROUND TRUTH
Code is a snapshot. Docs are the system. If it is not in `docs/`, it does not exist.
- Every feature needs a spec.
- Every decision needs an ADR.
- Every plan needs a PLAN-NNN.md.

### 2. SPECIFICATIONS BEFORE IMPLEMENTATION
Never write code without:
- A spec that defines the expected behavior.
- A plan that authorizes the implementation.
- Validation criteria that define "done."

### 3. FAILURES ARE SYSTEM SIGNALS
A bug is not a developer mistake. It is a gap in the harness -- a missing constraint,
test, or documentation that allowed the error to occur. Fix the harness, not just the code.

### 4. EVERY CHANGE IS TRACEABLE
Every commit message must reference a PLAN-NNN.md.
Every PLAN-NNN.md must reference the spec that authorized it.
No orphaned code. No mystery changes.

### 5. TESTS ARE SPECIFICATIONS
Tests are not an afterthought. They are the executable form of the spec.
If a test cannot be written, the spec is not clear enough.

### 6. QUALITY IS A PRIORITY ORDER, NOT A DIAL
Do not trade security for performance. Do not trade correctness for speed.
The priority order is fixed:
1. Security => 2. Correctness => 3. Reliability => 4. Performance => 5. Memory => 6. Maintainability => 7. Cost

### 7. ENTROPY MUST TREND DOWNWARD
Every cycle should leave the system cleaner than it found it.
If it doesn't, the GC agent failed.
