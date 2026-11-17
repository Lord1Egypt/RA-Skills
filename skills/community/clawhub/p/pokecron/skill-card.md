## Description:

PokeCron is a power-user reminder scheduler that creates persisted OS-native timers for reminders, recurring nudges, deferred agent tasks, reply-aware escalation, quiet hours, and trusted command hooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plaer1](https://clawhub.ai/user/plaer1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and power users use PokeCron to turn time-based requests into durable OS-scheduled reminders or deferred agent tasks, including recurring check-ins, wakeups, and follow-up loops. It can also help migrate heartbeat-style polling to scheduled tasks when the user explicitly opts in.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create persistent user-level scheduled jobs.

Mitigation: Review scheduled reminders before installation and use the management commands to inspect or remove reminders when they are no longer needed.

Risk: Command hooks can execute local programs under the user's account.

Mitigation: Avoid command hooks unless the target scripts are trusted and intentionally configured by the user.

Risk: The migration helper can change OpenClaw heartbeat configuration when run with --apply.

Mitigation: Use the migration helper in dry-run mode first and only apply changes when the user explicitly wants heartbeat polling disabled.

Risk: Vector-tone matching can send reminder or intent text to an Ollama endpoint when enabled.

Mitigation: Keep the endpoint on loopback unless the user explicitly opts into a remote endpoint with POKE_ALLOW_REMOTE_OLLAMA=1.

## Reference(s):

- [PokeCron ClawHub listing](https://clawhub.ai/plaer1/skills/pokecron)
- [SKILL.md](artifact/SKILL.md)
- [Scheduling guide](artifact/sub-skills/scheduling.md)
- [Escalation and followups guide](artifact/sub-skills/escalation.md)
- [Stages and command hooks guide](artifact/sub-skills/stages.md)
- [Migration guide](artifact/sub-skills/migration.md)
- [Management guide](artifact/sub-skills/management.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node and may create user-level scheduler entries when generated commands are applied.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
