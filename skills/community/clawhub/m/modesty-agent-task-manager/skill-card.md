## Description:

Manages and orchestrates multi-step, stateful agent workflows; handles task dependencies, persistent state, error recovery, and external rate-limiting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[modestyrichards](https://clawhub.ai/user/modestyrichards)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to define, run, resume, and coordinate multi-step agent workflows with task dependencies, local state, API-backed reasoning, notifications, and cooldown handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user and workflow content to an external SkillBoss API endpoint.

Mitigation: Use non-sensitive task text, scope SKILLBOSS_API_KEY permissions, and run only in controlled environments.

Risk: Workflow data can trigger outbound notifications.

Mitigation: Restrict recipients and channels to trusted destinations and review workflows before enabling notification actions.

Risk: The cooldown wrapper can execute local commands from task inputs or generated workflows.

Mitigation: Review or replace the command wrapper before deployment and avoid passing untrusted command strings.

Risk: Task state is written locally and may persist workflow data.

Mitigation: Keep sensitive data out of task definitions and protect or clean local state files after use.

## Reference(s):

- [Task Structure Schema](references/task_schema.md)
- [SkillBoss API Hub pilot endpoint](https://api.heybossai.com/v1/pilot)
- [ClawHub skill page](https://clawhub.ai/modestyrichards/skills/modesty-agent-task-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON task definitions, Python and shell commands, local state files, and workflow execution results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; may call an external API, write local task state, and send outbound notifications.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
