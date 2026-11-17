## Description:

Guide for creating effective skills. This skill should be used when users want to create a new skill (or update an existing skill) that extends Claude's capabilities with specialized knowledge, workflows, or tool integrations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lbbniu](https://clawhub.ai/user/lbbniu)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and skill authors use this skill to create, update, validate, and package agent skills with clear instructions, appropriate bundled resources, and concise output patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts that create or package skills may write outside the intended folder or package unintended local files if used with untrusted paths.

Mitigation: Run the scripts only with trusted skill names and folders, inspect generated diffs and packages before publishing, and avoid packaging untrusted directories until path-containment and symlink checks are added.

## Reference(s):

- [Output Patterns](references/output-patterns.md)
- [Workflow Patterns](references/workflows.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline code blocks and generated skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or package skill directories and files when its helper scripts are run.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
