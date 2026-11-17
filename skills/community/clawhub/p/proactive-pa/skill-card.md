## Description:

Proactive Personal Assistant behavior patterns help an agent anticipate needs, run heartbeat checks, configure cron-based proactive checks, and surface actionable insights autonomously.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure a personal-assistant agent to monitor messages, calendar events, cron health, and urgent email signals, then surface actionable alerts and next steps. The artifact is marked deprecated and says the behavior was moved into broader assistant guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prompt an agent to monitor private services and send alerts to a hard-coded WhatsApp recipient.

Mitigation: Install only in the intended private environment, remove hard-coded phone and group destinations, and require user confirmation before any outbound message.

Risk: The skill can encourage persistent cron jobs, memory writes, Git pushes, and publishing actions without adequate user control.

Mitigation: Require confirmation for cron creation, memory writes, Git pushes, publishing, and outbound messages, and provide clear ways to list, disable, and expire scheduled jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/netanel-abergel/skills/proactive-pa)
- [DEPRECATED.md](artifact/DEPRECATED.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes autonomous monitoring patterns, cron setup examples, alerting templates, and personal-assistant guardrails.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
