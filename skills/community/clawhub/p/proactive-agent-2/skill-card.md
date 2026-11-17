## Description:

Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ranthemaster](https://clawhub.ai/user/ranthemaster)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to give an AI agent persistent memory habits, proactive check-ins, recovery from context loss, and self-improvement guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory practices may capture secrets, sensitive personal details, or private conversation context.

Mitigation: Limit what the agent may write, avoid storing secrets or sensitive personal data, and review memory files before reuse or sharing.

Risk: Durable reminders or AGENTS.md triggers can create cross-session behavior with limited user control.

Mitigation: Skip cron-style reminders and persistent trigger installation unless explicitly desired by the user.

Risk: Proactive behavior can lead the agent to take unnecessary or consequential actions.

Mitigation: Require confirmation before tool use beyond local note updates, especially for installs, deletion, external communication, or security changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ranthemaster/skills/proactive-agent-2)
- [ClawHub publisher profile](https://clawhub.ai/user/ranthemaster)
- [Creator profile referenced by artifact](https://x.com/halthelobster)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with file templates, checklists, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs the agent to create and update local memory files and optional durable triggers.]

## Skill Version(s):

0.1.0 (source: server release metadata; source skill frontmatter reports 3.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
