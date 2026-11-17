## Description:

Autopilot is a high-autonomy agent mode that plans, executes, reviews, and follows through on user tasks using memory-aware context fusion, proactive idea generation, editorial judgment, and scheduled automation when available.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hendr15k](https://clawhub.ai/user/hendr15k)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when they want an agent to handle work end to end, including planning, execution, status reporting, quality review, proactive recommendations, and follow-up scheduling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed for broad and persistent autonomy across memory, filesystem, cron, worklog, and profile context.

Mitigation: Install only in workspaces where that scope is acceptable, and require explicit confirmation before file changes, cron changes, or future autonomous actions.

Risk: Full-memory review can expose private or stale context if used in shared or sensitive environments.

Mitigation: Limit activation to contexts with appropriate privacy boundaries, skip private memory in shared spaces, and review memory-derived conclusions before acting on them.

Risk: Proactive execution and scheduled automation can continue work beyond the user's immediate prompt.

Mitigation: Keep autonomous follow-through visible through status updates and logs, and disable or pause autonomy when ongoing action is not desired.

## Reference(s):

- [Autopilot Autonomous Operations Reference v9](references/autonomous-operations.md)
- [Autopilot Memory Mining Reference v9.1](references/memory-mining.md)
- [Autopilot Slash Command Reference v9](references/slash-commands.md)
- [Autopilot Transparent Execution Reference v9](references/transparent-execution.md)
- [Autopilot Generative Intelligence Reference v9](references/generative-intelligence.md)
- [Autopilot Proactivity Catalog v9](references/proactivity-catalog.md)
- [Autopilot Editorial Intelligence Reference v9](references/editorial-intelligence.md)
- [Autopilot Decision Matrix v9](references/decision-matrix.md)
- [Autopilot Strategic Commissioning Reference v9](references/strategic-commissioning.md)
- [Autopilot Creative Engine Reference v8](references/creative-engine.md)
- [Autopilot Capability Building Reference v9](references/capability-building.md)
- [Autopilot Error Recovery Playbook v9](references/error-recovery.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with inline commands, code blocks, file edits, plans, status updates, and concise recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify files, maintain worklog and profile notes, propose or manage scheduled follow-ups, and continue autonomously within applicable system and privacy constraints.]

## Skill Version(s):

9.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
