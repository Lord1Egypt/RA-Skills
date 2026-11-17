## Description:

Configures pre-commit hooks for linting, type checking, formatting, and testing

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to set up or improve pre-commit quality checks in new projects, existing codebases, and monorepos. It provides patterns for local hooks and CI checks covering formatting, linting, type checking, tests, and project-specific validation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The instructions include staging and commit guidance that could affect unintended project changes.

Mitigation: Review suggested commands, stage only intended files, and inspect the staged changes before committing.

Risk: The CI example uploads coverage data to Codecov.

Mitigation: Check what coverage data and related information your CI sends to Codecov before enabling the upload.

Risk: The security scan was partial because some referenced files were unavailable, so the described workflows were not fully verified.

Mitigation: Review the unavailable referenced materials and confirm relevant workflow behavior before relying on it.

## Reference(s):

- [Attune project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune)

## Skill Output:

**Output Type(s):** [Configuration instructions, Code, Shell commands]

**Output Format:** [Markdown with YAML, TOML, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
