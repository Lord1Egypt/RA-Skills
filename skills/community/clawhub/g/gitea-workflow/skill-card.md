## Description:

Gitea Workflow defines a Gitea issue and pull-request driven collaboration pattern for multi-role agents, including implementer and coordinator responsibilities, notification conventions, and cron-based loop control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project leads, and agent operators use this skill to coordinate multi-agent work through Gitea issues and pull requests while keeping routine discussion in issue comments and limiting chat notifications to completion, blockers, and phase changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring OpenClaw cron jobs can wake agents repeatedly and act on the wrong target if cron names, roles, repositories, or group destinations are misconfigured.

Mitigation: Enable the loop only after verifying each cron target, role, repository, and group destination, and use the status command to confirm the active schedule.

Risk: Gitea personal access tokens are used by individual agents at runtime and could expose repository access if stored too broadly.

Mitigation: Use a least-privilege Gitea token and keep it in a local 600-permission file or secret store managed by the individual agent.

## Reference(s):

- [cron-setup](references/cron-setup.md)
- [ClawHub skill page](https://clawhub.ai/axelhu/skills/gitea-workflow)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and YAML cron examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes role-specific workflow steps, notification templates, loop control commands, and cron configuration examples.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
