## Description:

Coordinates Claude agent teams over a filesystem protocol. Use for parallel agents with task dependencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to coordinate Claude Code agents working on parallel tasks, manage task dependencies, and exchange team messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Manually removing lock files while agents are coordinating can disrupt shared task or message updates.

Mitigation: Before cleanup, confirm no active agent holds or needs the lock and follow the documented recovery process; do not remove an active lock file.

## Reference(s):

- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.4 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
