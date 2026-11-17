## Description:

Configures GitHub Actions CI/CD workflows for testing, linting, and deployment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to set up or update GitHub Actions workflows for testing, linting, type checking, builds, and deployment in Python, Rust, and TypeScript projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workflow setup may replace existing CI configuration without warning.

Mitigation: Review proposed changes to CI files and keep a recoverable copy before using them.

Risk: The security scan was partial because several local references could not be resolved, so not every referenced item was assessed.

Mitigation: Resolve and inspect referenced materials before use; do not treat the scan as a complete assessment.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-attune-workflow-setup)
- [Project homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/attune)

## Skill Output:

**Output Type(s):** [Configuration files, Shell commands, Guidance]

**Output Format:** [GitHub Actions YAML workflow files with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Workflow files and setup guidance vary by detected project language.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
