## Description:

OpenSpec guides agents through spec-driven development with the OpenSpec CLI for feature work, migrations, refactors, and structured change management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcorrego](https://clawhub.ai/user/jcorrego)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill to plan, implement, validate, and archive structured software changes through OpenSpec proposals, specs, designs, and task lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented global `@latest` npm install can change behavior between installations.

Mitigation: Use a pinned, project-local OpenSpec dependency before running the workflow in a project.

Risk: The skill can direct broad workspace changes, including generated `openspec/` and `.claude/` files.

Mitigation: Review generated files before committing and require confirmation before archive or other mutating workflow steps.

## Reference(s):

- [Schema Reference](references/schemas.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration examples, and generated OpenSpec artifact content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update OpenSpec project files such as proposals, specs, designs, tasks, schemas, and generated Claude integration files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
