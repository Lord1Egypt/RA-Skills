## Description:

Self-reflection, self-criticism, self-learning, and self-organizing memory help an agent evaluate its work, catch mistakes, and improve future performance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quenlenliu](https://clawhub.ai/user/quenlenliu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to add local, cross-session improvement memory for corrections, preferences, recurring patterns, and self-reflection. It is intended for workflows where execution quality should compound over time while keeping learned behavior visible and reviewable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill persistently changes future agent behavior through cross-session local memory and workspace steering files.

Mitigation: Review proposed AGENTS.md, SOUL.md, and HEARTBEAT.md changes before enabling the skill, and keep memory actions transparent to the user.

Risk: Local memory can become sensitive or overbroad if corrections, preferences, or project context are stored without enough care.

Mitigation: Avoid storing credentials, sensitive personal information, third-party information, or unnecessary context; use the documented audit, export, and forget flows when needed.

Risk: The optional proactivity companion can add behavior beyond this skill and may require network access.

Mitigation: Install the companion only after explicit user confirmation, and separately audit or pin its publisher and version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quenlenliu/skills/my-self-improving)
- [Publisher profile](https://clawhub.ai/user/quenlenliu)
- [Skill homepage](https://clawic.com/skills/self-improving)
- [Security boundaries](artifact/boundaries.md)
- [Setup guide](artifact/setup.md)
- [Learning mechanics](artifact/learning.md)
- [Memory operations](artifact/operations.md)
- [Heartbeat rules](artifact/heartbeat-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, file templates, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory and workspace steering guidance for agent behavior; no credentials or extra binaries are required.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
