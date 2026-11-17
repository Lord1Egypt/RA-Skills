## Description:

Validates SQL syntax of pending database migration files before execution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ink5725](https://clawhub.ai/user/ink5725)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scan SQL migration directories, identify applied and pending migrations, and produce a JSON validation report for change control or CI/CD gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The validator executes migration SQL rather than only parsing it, which can cause filesystem-backed database side effects.

Mitigation: Review before installing or running in CI or against shared repositories; use a tightly isolated environment with disposable files, or require a non-executing SQL parser or strict SQLite authorizer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ink5725/skills/migration-validator)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [JSON validation report with migration status and validation errors]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes validation timestamp, discovered migrations, applied migrations, pending migrations, validation errors, and completion status.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
