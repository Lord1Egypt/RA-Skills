## Description:

Executes implementation plans with progress tracking, checkpoint validation, and quality gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill after planning to implement tasks in dependency order, track progress, and check work against acceptance criteria, tests, and quality gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External delegation may expose project information without checking destination approval or giving a user-facing privacy warning.

Mitigation: Before delegating, review whether the destination is approved, consider what project information will be shared, and inform the user.

Risk: The security report notes instruction-scope concerns and partial scan coverage, so unresolved references and other behavior may not have been fully assessed.

Mitigation: Review referenced materials and the skill's behavior before use, and restrict delegated access to the project information needed for the task.

## Reference(s):

- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/attune)
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-attune-project-execution)

## Skill Output:

**Output Type(s):** [Code, Markdown, Configuration, Shell commands]

**Output Format:** [Code changes, Markdown checklists and progress reports, shell commands, and JSON execution-state data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the implementation plan and project; execution-state data may record task status and progress metrics.]

## Skill Version(s):

1.10.3 (source: SKILL.md frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
