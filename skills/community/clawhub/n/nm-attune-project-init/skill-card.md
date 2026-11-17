## Description:

Scaffolds new projects with git, CI/CD workflows, pre-commit hooks, and build config.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to initialize new Python, Rust, or TypeScript projects, or update existing project tooling. It gathers project settings and guides creation of source structure, configuration, Git setup, CI workflows, and pre-commit hooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The broad Rust trigger may start the project setup workflow for unrelated Rust questions.

Mitigation: Review the trigger scope and inspect the referenced initialization script before installing; consider whether setup actions are appropriate for the Rust questions it may match.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-attune-project-init)
- [Declared project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/attune)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Interactive Markdown guidance with shell commands and project scaffold files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Project-specific values determine the language and files to create; existing files are reviewed before overwrite.]

## Skill Version(s):

1.10.3 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
