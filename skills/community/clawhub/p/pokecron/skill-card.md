## Description: <br>
PokeCron helps agents create and manage local reminder schedules, recurring nudges, deferred tasks, reply-aware escalation, quiet hours, and optional command hooks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[plaer1](https://clawhub.ai/user/plaer1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to turn time-based requests into persisted local reminders, scheduled agent tasks, reply-driven followups, and managed reminder state. It is most useful when an agent needs durable wakeups without a long-running daemon. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates user-level OS timers and can run delayed local command hooks. <br>
Mitigation: Install only when that behavior is intentional, and review active reminders and hook commands before relying on them. <br>
Risk: Stored commitments may be injected into later agent prompts more broadly than documented. <br>
Mitigation: Avoid storing sensitive commitments until the scope-filtering issue is fixed. <br>
Risk: Runtime state, history, hook logs, and opt-in hook environment values may contain sensitive operational details. <br>
Mitigation: Review active reminders, .runtime logs, and any --hook-env values during setup and maintenance. <br>
Risk: Optional vector-tone matching can send tone or intent text to OLLAMA_URL when enabled. <br>
Mitigation: Keep vector-tone endpoints loopback-only unless a trusted remote endpoint is intentionally enabled with POKE_ALLOW_REMOTE_OLLAMA=1. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/plaer1/pokecron) <br>
- [Scheduling guide](sub-skills/scheduling.md) <br>
- [Escalation and followups guide](sub-skills/escalation.md) <br>
- [Reply handling guide](sub-skills/replies.md) <br>
- [Quiet hours guide](sub-skills/quiet-hours.md) <br>
- [Management guide](sub-skills/management.md) <br>
- [Heartbeat migration guide](sub-skills/migration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dry-run recommendations, reminder management commands, and safety checks for hooks or migration steps.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence; artifact frontmatter and package.json report 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
