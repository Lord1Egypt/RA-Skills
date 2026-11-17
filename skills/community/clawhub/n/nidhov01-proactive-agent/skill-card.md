## Description:

Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve with WAL Protocol, Working Buffer, autonomous crons, and battle-tested patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidhov01](https://clawhub.ai/user/nidhov01)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to give an assistant durable local memory, proactive check-ins, onboarding routines, security habits, and self-improvement workflows. It is intended for agents that maintain workspace notes and propose useful next actions while asking for approval before external or irreversible actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages durable local notes about the user and conversations.

Mitigation: Disable or narrow automatic memory capture, review memory templates before use, and keep generated memory files out of version control.

Risk: The skill can lead agents toward broad local-reading, autonomous-checking, and self-modifying behavior.

Mitigation: Require explicit approval before granting email, calendar, browser, desktop, log, or other broad local access, and review autonomous-agent setup before enabling it.

Risk: Cron-style proactive actions may run without enough user control.

Mitigation: Review each cron or autonomous-agent configuration, prefer prompted checks for sensitive workflows, and require approval before external or irreversible actions.

## Reference(s):

- [Onboarding Flow Reference](artifact/references/onboarding-flow.md)
- [Security Patterns Reference](artifact/references/security-patterns.md)
- [Proactive Agent on ClawHub](https://clawhub.ai/nidhov01/skills/nidhov01-proactive-agent)
- [Publisher Profile](https://clawhub.ai/user/nidhov01)
- [Author Profile](https://x.com/halthelobster)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with starter Markdown files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent operating procedures, memory templates, onboarding templates, heartbeat checklists, and a local security audit script.]

## Skill Version(s):

3.1.0 (source: artifact/SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
