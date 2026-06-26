status: open

# PR-1009-2: Add Architecture Documentation (BEST_PRACTICES.md)

## 1. Objective
Generate documentation at the root of `AMS/` outlining the correct directory structure and import standards to prevent future architecture degradation.

## 2. Scope & Implementation Details
- Create `AMS/BEST_PRACTICES.md`.
- Document the purpose of the `scripts/` vs `tests/` directories.
- Outline the standard way to import internal modules (e.g., `from scripts.module import Class`).
- Add a strict rule preventing files from being dumped in the root of `AMS/` without justification.

## 3. TDD & Acceptance Criteria
- `AMS/BEST_PRACTICES.md` exists and contains clear structural rules, import standards, and the root-dumping restriction.
- No new code is broken by this documentation addition.