## Description:

Provides a GitHub project development workflow assistant for automated configuration, code review, dependency checks, and CI/CD integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to standardize GitHub project workflows, review code quality, check dependencies, and prepare CI/CD-related guidance or configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for broad development powers, including reading files, running commands, and writing repository changes.

Mitigation: Use it only in trusted repositories, keep command execution and file-changing actions behind explicit approval, and review generated changes before applying them.

Risk: The skill may require API keys or other credentials for workflow assistance.

Mitigation: Limit credentials to the minimum required scope, avoid exposing broad API keys, and keep secrets out of generated files and version control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/github-dev-standard)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON examples, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose repository file changes or command execution steps that should be reviewed before use.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
