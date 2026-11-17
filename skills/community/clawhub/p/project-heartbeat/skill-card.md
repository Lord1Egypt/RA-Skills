## Description:

Design controlled continuation loops for long-running projects. Use when a task is too large for one session, benefits from periodic wake-ups, and needs explicit continue conditions, stop boundaries, pending-decision handling, progress logging, and resume rules. Ideal for workspace refactors, long skill development, research tracks, and other cumulative engineering work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daowuu](https://clawhub.ai/user/daowuu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design controlled wake-up loops for long-running project work, including explicit continuation criteria, stop boundaries, pending-decision handling, progress logging, and resume behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Heartbeat runs may continue work in a project directory or delivery channel the user did not intend.

Mitigation: Review cron and delivery setup manually before enabling it, and scope heartbeat runs to project directories the agent is intended to read and update.

Risk: Continuation language can overstate progress when no durable project artifact changes.

Mitigation: Apply the skill's minimum artifact rule: a cycle counts as progress only when it updates a durable artifact such as state, backlog, pending decisions, or heartbeat logs.

## Reference(s):

- [Project Heartbeat on ClawHub](https://clawhub.ai/daowuu/skills/project-heartbeat)
- [Project Heartbeat Homepage](https://clawhub.ai/daowuu/project-heartbeat)
- [Boundaries](references/boundaries.md)
- [Continuation Integrity](references/continuation-integrity.md)
- [Deferred Backlog](references/deferred-backlog.md)
- [Examples](references/examples.md)
- [Heartbeat Log Template](references/heartbeat-log-template.md)
- [Pending Decisions Template](references/pending-decisions-template.md)
- [Summary + Handoff](references/summary-handoff.md)
- [TODO / Deferred Ideas](references/todo.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with plain-text helper script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional local helper scripts for fit checks and heartbeat plan rendering.]

## Skill Version(s):

0.4.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
