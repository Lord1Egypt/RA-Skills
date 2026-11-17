## Description:

OpenSpec guides agents through spec-driven development for non-trivial project changes, including proposing, validating, implementing, and archiving change artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juanclaw](https://clawhub.ai/user/juanclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to scope and manage non-trivial changes with OpenSpec proposals, requirements, designs, task lists, validation, and archival workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create or update planning and specification files under openspec/.

Mitigation: Review proposed OpenSpec artifacts before committing them.

Risk: The skill can archive completed changes, which moves change content into the archived OpenSpec structure.

Mitigation: Confirm tasks are complete and run OpenSpec validation before archiving.

Risk: Generated proposals, requirements, designs, or task lists may be incomplete or misaligned with the requested change.

Mitigation: Review the OpenSpec documents for accuracy and scope before implementation.

## Reference(s):

- [OpenSpec workflow patterns](references/workflow.md)
- [OpenSpec ClawHub release](https://clawhub.ai/juanclaw/skills/openspec-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline tool calls, shell commands, and file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update OpenSpec proposal, specification, design, task, and archive files under openspec/.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
