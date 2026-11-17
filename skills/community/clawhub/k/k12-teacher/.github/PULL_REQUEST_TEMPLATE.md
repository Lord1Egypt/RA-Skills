# Pull Request

## Description

Summarize the change, including motivation and context. Link related issues (for example, "Fixes #123").

## Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Test case update
- [ ] Refactoring (no functional changes)
- [ ] CI/CD changes

## Testing

- [ ] Ran `./scripts/validate-structure.sh` and all quality gates passed
- [ ] Updated or added cases in `tests/test-cases.md` where applicable
- [ ] Manually verified the changed behavior

## Constraint Compliance

- [ ] No emoji characters introduced (C-01)
- [ ] All content in English (C-02)
- [ ] SKILL.md remains under 200 lines if modified (C-03)
- [ ] Code templates only in `references/method-patterns.md` (C-04)
- [ ] No agent-autoinvoke markers in `prompts/` (C-05)
- [ ] Inputs, outputs, boundaries, and failure modes defined for changed modules (C-06)
- [ ] No cross-file circular dependencies (C-07)
- [ ] Single responsibility per file (C-08)
- [ ] Files under 300 lines unless justified (C-09)
- [ ] Templates parameterized, no hardcoded values (C-10)

## Documentation

- [ ] README.md updated if the file tree or structure changed
- [ ] CHANGELOG.md entry added under [Unreleased]
- [ ] User-facing changes described in this pull request

## Impact and Rollback

State the affected modules and any breaking-change or rollback notes. Delete this section if not applicable.
