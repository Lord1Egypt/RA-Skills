## Description:

OpenClaw TODO List helps an agent maintain concise local TODO and DONE markdown files for explicit tasks, in-progress work, and completed work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an agent a lightweight local task-tracking workflow. The skill records clear tasks in TODO.md, moves active work into an in-progress section, and archives completed tasks in DONE.md.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt an agent to update local TODO and DONE files proactively as work starts, progresses, or completes.

Mitigation: Review task-file edits before relying on them, especially when multiple agents or users share the same workspace.

Risk: The artifact instructions and examples are Chinese-language oriented.

Mitigation: Confirm that task labels, owner names, and status notes are understandable to the intended workspace users.

## Reference(s):

- [TODO List Detailed Specification](artifact/references/spec.md)
- [TODO and DONE Examples](artifact/references/example-todo.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown task entries and concise guidance, sometimes with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local TODO.md and DONE.md task records under memory/todo when applied by an agent.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
