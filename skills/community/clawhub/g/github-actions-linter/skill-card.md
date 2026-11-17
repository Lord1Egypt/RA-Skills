## Description:

Lint and validate GitHub Actions workflow YAML files for common mistakes, security issues, deprecated actions, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to lint, validate, and audit GitHub Actions workflow files for syntax, structure, security, deprecated action, and best-practice issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The linter has accuracy gaps and may miss or overstate some GitHub Actions issues.

Mitigation: Use results as review support rather than as the sole security gate, and manually review multiline run blocks, third-party action pinning, and job-level permissions.

Risk: Scanning a broad directory can produce noisy findings outside the intended workflow review scope.

Mitigation: Point the skill at specific workflow files or the intended .github/workflows directory when practical.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/github-actions-linter)
- [Publisher profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [text, JSON, markdown, shell commands, guidance]

**Output Format:** [Text, JSON, or Markdown lint findings with severity, rule, location, message, and summary counts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled command can return exit code 1 when errors are found, or when warnings are found in strict mode.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
