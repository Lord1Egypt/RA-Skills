# MECHANICAL ENFORCEMENT

Architecture and quality rules enforced as linter checks, not just documentation.

## PRINCIPLE

Documentation rots. Linter rules persist. When a quality rule matters enough to
write down, it matters enough to enforce mechanically.

## HOW IT WORKS

1. Encode architectural rules as custom linter checks.
2. Linter error messages ARE instructions — they inject remediation guidance
   directly into agent context when violations are detected.
3. Pre-commit hooks run all linters before any commit.

## EXAMPLE LINTER RULES

### Dependency Direction Enforcement
Rule: code may only import from permitted layers (e.g., UI → Runtime → Service → Repo → Types).
Violation message: "Import of 'X' from 'Y' violates dependency direction. permitted: Z → W → V → U → T. Move 'X' to an allowed layer or restructure the dependency."

### File Size Limit
Rule: no file exceeds 500 lines (configurable).
Violation message: "File exceeds 500-line limit (current: N). Split into smaller modules following single-responsibility principle."

### Structured Logging
Rule: all logging must use the structured logger, never console.log/string concatenation.
Violation message: "Unstructured log call found. Use logger.info/error/warn with structured fields."

### Naming Conventions
Rule: schemas use PascalCase, utilities use camelCase, constants use SCREAMING_SNAKE_CASE.
Violation message: "Naming violation: 'X' should use Y convention in Z context."

### Test Coverage Floor
Rule: no file may be committed with <90% coverage on changed lines.
Violation message: "Coverage below 90% on changed lines in X. Add tests for uncovered paths."

## ESCALATION PATH

1. Doc rule (in references/) → agent may ignore
2. Doc rule + human emphasis → promote to linter rule
3. Linter rule → enforced on every commit via pre-commit hook
4. Repeated linter violations → Prevention Rule in references/constraints.md

## AGENT-GENERATED LINTERS

Custom linters are themselves maintained by agents:
- When a new architectural rule is needed, agent creates the linter
- Linter includes clear error messages that teach the agent how to fix violations
- Linters are tested alongside application code
