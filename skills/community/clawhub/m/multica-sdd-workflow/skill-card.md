## Description:

Guides agents through an SDD-first Multica workflow for feature work, including specification documents, squad and issue setup, dependency planning, progress monitoring, documentation updates, and git commits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[denghuayuan](https://clawhub.ai/user/denghuayuan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to plan and execute feature work with specification-driven development and Multica issue coordination. It is intended for projects that want SDD records, TDD sequencing, task dependencies, review loops, and completion records kept in sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can change Multica project state, repository files, git history, and issue status.

Mitigation: Require human approval before mutation commands, issue assignment or updates, document edits, and git commits.

Risk: The workflow reads operational values and commands from .multica/squad.md, including IDs, work directories, and test/typecheck commands.

Mitigation: Treat .multica/squad.md as security-sensitive and verify every ID, path, and command before use.

Risk: Configured test and typecheck commands may execute repository-provided commands.

Mitigation: Inspect the configured commands in the target repository and run them only in a trusted workspace.

## Reference(s):

- [Skill artifact](artifact/SKILL.md)
- [Issue templates](artifact/issue-templates.md)
- [SDD document templates](artifact/sdd-templates.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Markdown guidance with shell command snippets, issue descriptions, and SDD document templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces repository-oriented workflow guidance and command snippets; command execution and mutations should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and release changelog state 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
