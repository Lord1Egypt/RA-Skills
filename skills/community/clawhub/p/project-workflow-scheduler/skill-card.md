## Description:

Break a project, objective, or task list into safe, bounded one-time OpenClaw cron work blocks with dependencies, risk classification, and strong isolated agentTurn payloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebclawops](https://clawhub.ai/user/sebclawops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and project leads use this skill to convert multi-step work into supervised one-time OpenClaw cron blocks with clear dependencies, risk classification, payloads, and review checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Future scheduled work may run without the parent session's live context.

Mitigation: Use bounded isolated agentTurn payloads that include the exact scope, prior state, inputs to inspect, expected output, forbidden actions, and blocker reporting instructions.

Risk: Unsafe actions could be scheduled unattended if project blocks are not reviewed carefully.

Mitigation: Classify every block and schedule only work that is safe, auditable, low risk, reversible, and explicitly approved when approval is needed.

Risk: Destructive changes, purchases, public or customer-facing sends, and credential-dependent flows could create operational or trust risk.

Mitigation: Keep those activities behind explicit review and approval, and use the skill for bounded audits, recaps, cleanup proposals, prep tasks, and checkpoints.

## Reference(s):

- [Project Workflow Scheduler examples](artifact/references/examples.md)
- [ClawHub skill page](https://clawhub.ai/sebclawops/skills/project-workflow-scheduler)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown with structured schedule proposals and cron payload text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes assumptions, dependencies, risks, and documentation update suggestions when relevant.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
