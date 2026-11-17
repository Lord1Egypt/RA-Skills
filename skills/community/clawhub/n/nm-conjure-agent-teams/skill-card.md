## Description:

Coordinates Claude Code agent teams through filesystem-based task and messaging workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using Claude Code use this skill to coordinate parallel agent work, assign tasks and dependencies, exchange messages, and monitor team health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Deleting a lock file while related processes are active can allow conflicting access to shared state.

Mitigation: Confirm all related processes have stopped before deleting a lock file, and review the referenced components because the security assessment is incomplete.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-conjure-agent-teams)
- [Project page listed in Clawdis metadata](https://github.com/athola/claude-night-market/tree/master/plugins/conjure)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes task, team, messaging, and health-monitoring procedures.]

## Skill Version(s):

1.10.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
