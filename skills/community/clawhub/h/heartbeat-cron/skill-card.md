## Description:

Create and refine HEARTBEAT.md files for murmur, a CLI daemon that runs scheduled Claude prompts on a cron or interval schedule.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wyblhl](https://clawhub.ai/user/wyblhl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to design, test, and register recurring murmur heartbeats for monitoring, digests, repository maintenance, and other scheduled agent tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring agent jobs can be configured with broad filesystem, network, or permission settings.

Mitigation: Review each generated HEARTBEAT.md before registration; prefer read-only or workspace-write scopes and avoid permissions: skip or danger-full-access unless explicitly approved.

Risk: Scheduled prompts may include destructive commands or operational actions that repeat automatically.

Mitigation: Require explicit operational approval for destructive commands and keep scheduled jobs narrowly scoped to a single purpose.

Risk: Heartbeats that call APIs or delivery services may require tokens or webhook URLs.

Mitigation: Store sensitive values in .env with narrowly scoped credentials and reference them through environment variables.

## Reference(s):

- [Heartbeat examples](artifact/references/examples.md)
- [Murmur source repository](https://github.com/t0dorakis/murmur.git)
- [agent-browser](https://github.com/vercel-labs/agent-browser)
- [pi-browser](https://github.com/badlogic/pi-mono)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with YAML frontmatter and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces HEARTBEAT.md content and setup steps for murmur schedules; generated jobs should be reviewed before registration.]

## Skill Version(s):

0.4.4 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
