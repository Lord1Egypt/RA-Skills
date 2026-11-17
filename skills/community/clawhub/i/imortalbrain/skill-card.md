## Description:

Immortal Brain is a proactive OpenClaw agent for autonomous task intake, research, planning, execution tracking, persistent memory, and progress reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ovidiuproca](https://clawhub.ai/user/ovidiuproca)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to manage active tasks through an autonomous workflow that researches related work, creates plans, tracks progress, and maintains memory/profile files. It is intended for users who deliberately want a persistent background task and memory manager.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run as a persistent autonomous background task and continue after user silence.

Mitigation: Enable it only when persistent automation is intended, and disable or narrow auto-approval before use.

Risk: The skill stores task, memory, profile, and backup data that may contain sensitive user or workspace context.

Mitigation: Review and purge memory, profile, and backup files regularly, and avoid adding secrets or sensitive personal data.

Risk: Optional Telegram notifications may send workspace-derived content outside the local environment.

Mitigation: Keep Telegram disabled for sensitive work or restrict notifications to status-only summaries.

Risk: Optional scheduler setup can make the agent continue running beyond the current session.

Mitigation: Avoid the Windows Task Scheduler option unless explicit removal and monitoring steps are in place.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ovidiuproca/skills/imortalbrain)
- [Conceptual Guide](artifact/references/conceptual_guide.md)
- [Heartbeat Info](artifact/references/heartbeat_info.md)
- [Setup Guide](artifact/references/setup_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON status/progress output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update local task, memory, profile, backup, progress, and heartbeat state files.]

## Skill Version(s):

5.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
