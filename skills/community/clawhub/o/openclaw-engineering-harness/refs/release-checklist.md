# Release Checklist

Before marking the task as `deliver` and exporting the skill, complete the following items:

- [ ] **Input Verified**: Ensure all required inputs (goal, scope, constraints, rollback) are present in the task description.
- [ ] **Implementation Verified**: The change must be isolated and functionally complete according to the scope.
- [ ] **Tests Executed**: The validation plan must be executed and all critical paths passed.
- [ ] **Rollback Confirmed**: A viable rollback mechanism exists if the change proves faulty.
- [ ] **Documentation Aligned**: Any changes to functionality are reflected in the `refs/` markdown files.
- [ ] **Constraints Checked**: Run `run_constraints.py` to ensure the skill complies with all boundaries (no host text copy, standard library only).
- [ ] **Artifact Audited**: Run `export.py` and verify that the output directory contains no forbidden signatures (paths, URLs).
- [ ] **Memory Updated**: Ask the user "What did we learn from this task?" and write the answer to `.claude/openclaw-memory.json`.
- [ ] **Manifest Verified**: Ensure the generated `manifest.json` correctly reflects the exported files.
