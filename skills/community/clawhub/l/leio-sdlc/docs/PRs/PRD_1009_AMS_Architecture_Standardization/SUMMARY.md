status: open

# PR-1009-1: De-duplicate qmt_client.py and Fix Imports

## 1. Objective
Clean up duplicate files and establish a single source of truth for `qmt_client.py` within the `AMS` project.

## 2. Scope & Implementation Details
- Delete redundant `AMS/qmt_client.py`.
- Keep the `AMS/scripts/qmt_client.py` version.
- Modify `AMS/tests/test_qmt_client.py` to import `QMTClient` correctly.
- Update `pilot_stock_radar.py` imports.

## 3. TDD & Acceptance Criteria
- `pytest AMS/tests/test_qmt_client.py` passes successfully.
- `ls AMS/qmt_client.py` returns `No such file or directory`.

---

status: open

# PR-1009-2: Add Architecture Documentation (BEST_PRACTICES.md)

## 1. Objective
Generate `BEST_PRACTICES.md` at the root of `AMS/`.

## 2. Scope & Implementation Details
- Create `AMS/BEST_PRACTICES.md`.
- Document `scripts/` vs `tests/` directories.
- Define standard import module paths.
- Forbid root file dumping.

## 3. TDD & Acceptance Criteria
- `AMS/BEST_PRACTICES.md` is populated.