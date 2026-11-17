# Contributing to k12-teacher

Thank you for your interest in contributing to the k12-teacher skill. This document provides guidelines for human and AI contributors to ensure consistency and quality.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Branch Naming Convention](#branch-naming-convention)
- [Commit Message Format](#commit-message-format)
- [Pull Request Process](#pull-request-process)
- [Pull Request Template](#pull-request-template)
- [Review Checklist](#review-checklist)
- [Testing Requirements](#testing-requirements)
- [Style Guidelines](#style-guidelines)
- [License](#license)

## Code of Conduct

This project and all participants are expected to uphold the [Code of Conduct](CODE_OF_CONDUCT.md). We are committed to providing a welcoming and inclusive environment. Participants who violate these standards may be removed from the project.

Please report unacceptable behavior by opening a GitHub issue or contacting the project maintainers directly.

## Getting Started

1. Fork the repository on GitHub.
2. Clone your fork locally:
   ```
   git clone https://github.com/<username>/k12-teacher.git
   cd k12-teacher
   ```
3. Create a new branch following the branch naming convention (see below).
4. Make your changes.
5. Run the validation script: `./scripts/validate-structure.sh`
6. Commit your changes following the commit message format (see below).
7. Push to your fork and submit a pull request.

## Branch Naming Convention

All branches must follow the `prefix/type` naming convention:

| Prefix | Description | Example |
|---|---|---|
| feat/ | New feature or capability | feat/add-socratic-pattern |
| fix/ | Bug fix or correction | fix/correct-tier-mapping |
| docs/ | Documentation changes | docs/update-contributing-guide |
| refactor/ | Code refactoring without behavior change | refactor/deduplicate-validation-logic |
| test/ | Adding or updating tests | test/add-boundary-violation-cases |

Additional prefixes: `ci/` (CI/CD changes), `chore/` (maintenance tasks), `revert/` (reverting commits).

Branch naming rules:
- Use lowercase letters, numbers, and hyphens only (kebab-case)
- Include a brief, descriptive name after the prefix
- Never use the main branch for development -- always create a feature branch

## Commit Message Format

This project follows the Conventional Commits specification. Every commit message must conform to:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Type

Must be one of: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `ci`, `chore`, `revert`.

### Scope

Recommended scope indicating the affected module: `method-patterns`, `skill`, `prompts`, `tests`, `scripts`, `kb`, `structure`.

### Rules

- Use imperative mood (e.g., "add" not "added" or "adds")
- Do not capitalize the first letter
- No period at the end
- Limit description to 72 characters maximum
- Body should explain what and why, not how

### Examples

```
feat(method-patterns): add scaffolded problem-solving pattern

Add a scaffolded problem-solving pattern with configurable
scaffold depth levels (1-4). Includes pseudocode for scaffold
construction and gradual removal.

Closes #42
```

```
fix(prompts): correct tier assignment logic in implement-method prompt

The Diagnose phase was assigning Tier 2 instead of Tier 1 for
learners with basic familiarity. Updated the decision table.
```

## Pull Request Process

### Before Submitting

- Ensure your branch is up to date with main
- Run `./scripts/validate-structure.sh` and verify all checks pass
- Review your own changes before submitting
- Ensure all files comply with constraints C-01 through C-10

### Pull Request Template

Every pull request must use the following template:

```
## Description

Provide a summary of the changes. Include motivation and context.

### Related Issue

Link to any related issues (e.g., "Fixes #123").

### Type of Change

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to change)
- [ ] Documentation update
- [ ] Test case update
- [ ] Refactoring (no functional changes)
- [ ] CI/CD changes
- [ ] Other (please describe):

### Testing

- [ ] Ran `./scripts/validate-structure.sh` successfully
- [ ] Reviewed test-cases.md for relevant test cases
- [ ] Manually verified the changes
- [ ] Other (please describe):

### Checklist

- [ ] My code follows the project's style guidelines
- [ ] I have performed a self-review of my code
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] New and existing tests pass locally with my changes
```

### Review Process

All pull requests require review from at least one maintainer before merging. Reviews check code quality, correctness, test coverage, documentation accuracy, and constraint compliance.

### Merging

- All CI checks must pass before merging
- Resolve all review comments before merging
- Use squash merge for documentation-only changes
- Use merge commit for feature/fix changes

## Review Checklist

Maintainers and reviewers should verify:

### Structural Checks

- [ ] PR title and description follow Conventional Commits format
- [ ] Branch name follows prefix/type convention
- [ ] All required files exist and are non-empty
- [ ] No new files violate single responsibility principle (C-08)
- [ ] No file exceeds 300 lines without justification (C-09)

### Constraint Compliance

- [ ] No emoji characters in any modified or new files (C-01)
- [ ] All content is in English (C-02)
- [ ] SKILL.md remains under 200 lines if modified (C-03)
- [ ] Code templates only in references/method-patterns.md (C-04)
- [ ] prompts/ files contain no agent-autoinvoke markers (C-05)
- [ ] All modules have defined input, output, boundary, failure mode (C-06)
- [ ] No cross-file circular dependencies (C-07)
- [ ] All templates parameterized, no hardcoded values (C-10)

### Content Quality

- [ ] Changes align with project purpose statement (Section 2)
- [ ] Five-tier capability model consistently applied
- [ ] Five-phase workflow (Diagnose-Select-Deliver-Assess-Remediate) correctly implemented
- [ ] Boundary conditions and escalation rules (Section 12) respected

### Testing

- [ ] `./scripts/validate-structure.sh` passes all quality gates (G-01 through G-10)
- [ ] Relevant test cases in tests/test-cases.md are updated or added
- [ ] Edge cases and boundary violations are covered

### Documentation

- [ ] README.md updated if file tree or structure changes
- [ ] CHANGELOG.md entry included
- [ ] User-facing changes documented in PR description

## Testing Requirements

All contributions affecting functionality must include appropriate test coverage.

### Test Case Structure

Every test case in `tests/test-cases.md` must include:

- **Test Case ID**: Unique identifier (e.g., TC-XXX)
- **Input Scenario**: Grade level, subject, topic, learner profile
- **Expected Behavior**: Which tier activates, which template fires
- **Expected Output Shape**: Structural requirements of the output
- **Edge Cases**: Multi-grade, special needs, advanced learner, language barrier
- **Boundary Violations**: Requests outside K-12 scope, non-academic advice requests

### Test Categories

1. **Core Functionality**: Normal teaching scenarios across all tiers (Tier 0 through Tier 4)
2. **Edge Cases**: Multi-grade classrooms, special needs learners, advanced learners, language barriers
3. **Boundary Violations**: Requests outside K-12 scope, medical/psychological/legal advice, certification generation, child safety violations, exam cheating
4. **Harness Engineering Compliance**: Missing inputs, idempotency checks, cross-file reference integrity

### Running Tests

Run the full validation suite before submitting:

```
./scripts/validate-structure.sh
```

This script checks all 10 quality gates (G-01 through G-10).

### Adding New Test Cases

1. Add test cases to `tests/test-cases.md` covering the new behavior
2. Include both positive tests (expected success) and negative tests (expected refusal/escalation)
3. Ensure edge cases specific to the change are covered
4. Run the validation script to confirm all gates pass

## Style Guidelines

### General Principles

- Use clear, concise, professional language
- Write in active voice
- Use imperative mood for instructions
- Avoid jargon where simple terms suffice
- Keep paragraphs short (3-5 sentences maximum)

### Markdown Formatting

- Use H1 for titles, H2 for sections, H3 for subsections
- Use tables for structured data
- Use code blocks for commands and file paths
- Use bullet lists for enumerated items
- Link to related documents using relative paths

### File-Specific Guidelines

- **Markdown files**: Consistent heading hierarchy; document title at top
- **Shell scripts**: Header comment block with purpose, usage, exit codes; use `set -euo pipefail`
- **All files**: End with newline; use UTF-8 encoding

## License

By contributing to this project, you agree that your contributions will be licensed under the GNU General Public License Version 3 (GPLv3), as specified in the LICENSE file.

---

Thank you for contributing to k12-teacher. Your efforts help improve K-12 education through structured, accessible AI-powered instruction.
