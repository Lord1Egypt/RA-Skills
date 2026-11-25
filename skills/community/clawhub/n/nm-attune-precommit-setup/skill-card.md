## Description:

Configures pre-commit hooks for linting, type checking, formatting, and testing

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to configure pre-commit quality checks for linting, type checking, tests, and project-specific validation. It also provides examples for coordinating local checks with CI, including monorepo workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill demonstrates `git add .`, which can stage files beyond the intended change.

Mitigation: Stage specific paths where practical and review `git status` and the staged diff before committing.

Risk: The sample CI workflow uploads coverage data to Codecov; the scan flags this external upload as unqualified.

Mitigation: Check that sending coverage data to Codecov is acceptable for the project before enabling the upload.

Risk: ClawScan reports incomplete coverage because several referenced paths could not be resolved.

Mitigation: Treat the scan as incomplete and inspect the referenced configuration and workflow paths before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-attune-precommit-setup)
- [Attune plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune)

## Skill Output:

**Output Type(s):** [Configuration, Shell commands, Code, Guidance]

**Output Format:** [Markdown with YAML, TOML, Python, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Setup instructions and reusable examples for pre-commit hooks and CI checks.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
