## Description:

Scaffolds new projects with git, CI/CD workflows, pre-commit hooks, and build config.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to initialize or update Python, Rust, and TypeScript projects with version control, CI/CD, pre-commit hooks, build configuration, and project journals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious, citing behavior that may not match its project-scaffolding purpose and a concern that template output could be written outside the project. Its analysis was partial because referenced local paths were missing.

Mitigation: Review the intended destination and planned file paths before execution, confirm the write scope, and inspect generated files afterward.

## Reference(s):

- [Attune plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/attune)
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-attune-project-init)

## Skill Output:

**Output Type(s):** [Configuration files, Shell commands, Guidance]

**Output Format:** [Markdown instructions with shell commands and project configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scaffolds files in the selected project directory, collects language and project metadata, and asks before overwriting existing configuration.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
