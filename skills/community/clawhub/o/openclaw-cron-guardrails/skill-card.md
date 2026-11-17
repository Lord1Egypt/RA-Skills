## Description:

Create, review, repair, or route OpenClaw cron jobs and scheduled agent actions with safe defaults for delivery, sessions, timeouts, and natural-language scheduling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jackal092927](https://clawhub.ai/user/jackal092927)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn scheduled-action requests into safer OpenClaw cron patterns, commands, and JSON payloads. It is especially relevant for reminders, recurring workers, visible channel delivery, session or thread pushes, and cron repair workflows where routing, timezone, or timeout mistakes could cause failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent scheduled agent actions, including current-session or current-thread prompt injection, can continue operating after the initial request and may affect the wrong context if scope is unclear.

Mitigation: Require clear scope for session or thread jobs, keep workflows in dry-run until reviewed, and verify the resulting job target before enabling repeated execution.

Risk: The skill includes an unsafe shell-based apply path for creating cron jobs.

Mitigation: Review rendered commands before use, require explicit confirmation before --apply, and avoid passing untrusted natural-language input into apply workflows.

Risk: External channel delivery and webhooks can send scheduled output to unintended or untrusted destinations.

Mitigation: Use explicit trusted delivery channels and targets, avoid implicit last-channel routing, and treat webhooks as privileged destinations.

Risk: Cron edit or run operations can change or execute existing persistent jobs.

Mitigation: Inspect the existing job and recent runs first, change one dimension at a time, and confirm the updated timezone, delivery target, payload kind, and timeout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jackal092927/skills/openclaw-cron-guardrails)
- [Intent Routing for Natural-Language Cron Requests](references/intent-routing.md)
- [OpenClaw Cron Safe Patterns](references/patterns.md)
- [OpenClaw Cron Pitfalls](references/pitfalls.md)
- [Diagnostics and Repair](references/diagnostics.md)
- [Integration Modes](references/integration-modes.md)
- [Cron Spec Examples](references/spec-examples.md)
- [Target Helpers](references/target-helpers.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce dry-run cron specifications, rendered OpenClaw commands, validation findings, repair guidance, and configuration advice; apply actions require explicit confirmation.]

## Skill Version(s):

0.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
