## Description:

Long Running Agent helps AI agents manage multi-step projects across sessions by creating and maintaining project briefs, changelogs, progress records, failed-attempt notes, and next actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sleepingzzzz](https://clawhub.ai/user/sleepingzzzz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to create, resume, inspect, update, and pause long-running AI-assisted projects. It is intended for workflows that need persistent local project state across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persists project plans, progress, failed attempts, and session notes in local files that can influence future agent work.

Mitigation: Keep project state in trusted directories and review PROJECT.md and CHANGELOG.md before asking an agent to continue work.

Risk: The initialization script can overwrite existing PROJECT.md and CHANGELOG.md files at writable destinations.

Mitigation: Use trusted project names and --path values, and check the destination before initializing a project.

Risk: Mutable project notes can carry stale or misleading context into later sessions.

Mitigation: Review progress records, failed-attempt notes, and next actions during each orientation step.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sleepingzzzz/skills/long-running-agent)
- [Anthropic Long-Running Tasks](https://www.anthropic.com/research/long-running-tasks)
- [smsharma/clax Reference Implementation](https://github.com/smsharma/clax)
- [Best Practices](references/best-practices.md)
- [Changelog Template](references/changelog-template.md)
- [Project Template](references/project-template.md)
- [Ralph Loop](references/ralph-loop.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated project files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local PROJECT.md, CHANGELOG.md, tests directories, and project state under tasks; OpenClaw metadata requires git.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
