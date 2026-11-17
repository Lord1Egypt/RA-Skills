# Pull Request

Thank you for contributing to MAGI Strategic Advisor. Please complete the
sections below before requesting review.

## Change Description

<!-- What does this pull request change, and why? -->

## Type of Change

- [ ] feat: new feature or capability (MINOR version bump)
- [ ] fix: bug fix or documentation correction (PATCH version bump)
- [ ] docs: documentation only
- [ ] chore: tooling, CI, or repository maintenance
- [ ] BREAKING CHANGE: incompatible behavior change (MAJOR version bump)

## Affected Layers

- [ ] SKILL.md (routing index)
- [ ] references/ (runtime knowledge)
- [ ] prompts/ (user-facing artifacts)
- [ ] scripts/ (executable tools)
- [ ] Root governance files
- [ ] .github/ (platform configuration)

## Validation Performed

- [ ] `make validate` (or `python scripts/validate-project.py`) passes
- [ ] `python -m compileall -q scripts` passes
- [ ] Manually exercised the changed scripts or reviewed the changed documents

## Hard Constraints (from README FOR AI.md)

- [ ] All content is in English
- [ ] No emoji characters anywhere in the repository
- [ ] SKILL.md remains below 120 lines (if touched)
- [ ] Code templates remain only in `references/method-patterns.md`
- [ ] CHANGELOG.md updated under the correct version heading

## Breaking Changes

<!-- Describe any incompatible change and the migration path, or write "None". -->

## Additional Notes

<!-- Review hints, follow-up work, or linked issues. -->
