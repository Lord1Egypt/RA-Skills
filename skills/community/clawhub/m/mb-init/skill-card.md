## Description:

Initializes a memory bank for a new or existing project by creating the standard directory structure, core Markdown files, and an optional first task file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[space-cadet](https://clawhub.ai/user/space-cadet)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to bootstrap project-local memory-bank documentation for task tracking before starting work on a new or existing project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates project-local memory-bank documentation and includes a git commit step.

Mitigation: Confirm the absolute project root, review the planned files, and treat the git commit step as optional until the generated documentation has been inspected.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/space-cadet/skills/mb-init)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash command blocks and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates project-local memory-bank documentation and may include an optional git commit command.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
