## Description:

Memory Four Types helps an OpenClaw agent classify, store, and index long-term memory as user, feedback, project, and reference records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rickhuang28](https://clawhub.ai/user/rickhuang28)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to maintain structured workspace memory, including user preferences, operational feedback, project context, and external references.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages persistent storage of personal details and conversation-derived memory, which can retain private information without adequate consent or deletion controls.

Mitigation: Require explicit consent before saving user details, avoid raw conversation logs, redact private data, and define review, deletion, and retention rules for the memory directory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/rickhuang28/skills/memory-four-types)
- [Memory Index Template](templates/MEMORY-index.md)
- [User Memory Template](templates/user-example.md)
- [Feedback Memory Template](templates/feedback-example.md)
- [Project Memory Template](templates/project-example.md)
- [Reference Memory Template](templates/reference-example.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with example commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent memory file structures and indexing conventions for agent workspaces.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
