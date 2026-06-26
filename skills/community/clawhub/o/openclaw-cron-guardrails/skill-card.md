## Description: <br>
OpenClaw Cron Guardrails helps agents create, review, repair, and route OpenClaw cron jobs with explicit schedule, session, delivery, and verification defaults. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackal092927](https://clawhub.ai/user/jackal092927) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to turn reminder, recurring task, visible delivery, and cron repair requests into safer OpenClaw cron patterns. It emphasizes explicit delivery targets, session routing, timezones, timeout choices, and post-change verification for scheduled agent actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled jobs can create or edit recurring agent actions that may run without the user watching each execution. <br>
Mitigation: Review every generated cron job before applying it, then verify the job list, recent runs, payload kind, timezone, delivery target, and timeout after creation or edit. <br>
Risk: Session or thread prompt-injection patterns can repeatedly push an active agent context. <br>
Mitigation: Use these patterns only when that behavior is intentional, bind the session or thread explicitly, and avoid converting them into generic visible delivery. <br>
Risk: Webhook or visible delivery can send output to the wrong destination or expose sensitive content if routing is ambiguous. <br>
Mitigation: Use trusted endpoints, avoid sensitive output, and require explicit channel, target, and account details for visible delivery in multi-channel setups. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jackal092927/openclaw-cron-guardrails) <br>
- [Publisher profile](https://clawhub.ai/user/jackal092927) <br>
- [Intent routing](references/intent-routing.md) <br>
- [Safe patterns](references/patterns.md) <br>
- [Diagnostics and repair](references/diagnostics.md) <br>
- [Public examples](references/public-examples.md) <br>
- [Integration modes](references/integration-modes.md) <br>
- [Target helpers](references/target-helpers.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON examples and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce dry-run cron specifications, validation results, rendered OpenClaw cron commands, or repair guidance before any apply step.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
