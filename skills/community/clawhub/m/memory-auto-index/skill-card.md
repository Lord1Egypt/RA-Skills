## Description:

Automatically adds index entries for MEMORY.md and memory/ files, including tag classification, key decision tracking, and duplicate entry prevention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mengnessly](https://clawhub.ai/user/mengnessly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep persistent memory indexes synchronized with memory files, classify entries by tags, and surface important decisions in a consistent Markdown index.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic trigger examples can execute shell commands built from memory-derived strings.

Mitigation: Use safe argument-vector process APIs, avoid shell interpolation, and validate subjects, tags, dates, and paths before execution.

Risk: The skill updates persistent memory indexes, which can make incorrect or unwanted entries durable.

Mitigation: Limit writes to MEMORY.md and memory/ paths, review generated diffs before committing them, and keep backups or version control for memory files.

Risk: The artifact describes referenced scripts that are not included in the release artifact.

Mitigation: Inspect or supply the referenced scripts before installation, and do not run missing or locally substituted scripts without review.

## Reference(s):

- [Memory Auto Index on ClawHub](https://clawhub.ai/mengnessly/skills/memory-auto-index)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown guidance with shell command examples and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces memory index conventions, trigger guidance, and maintenance commands for MEMORY.md and memory/ files.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
