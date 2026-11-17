## Description:

IceCube Heartbeat guides agents to use idle heartbeat polls for system checks, memory governance, improvement detection, evolution checks, and proactive maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ares521521-design](https://clawhub.ai/user/ares521521-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure OpenClaw heartbeat behavior so idle agents can check pending work, maintain memory files, detect repeated failure patterns, and surface useful proactive alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended heartbeat runs may make persistent or externally visible changes such as commits, pushes, memory edits, or skill installation.

Mitigation: Disable automatic commits, pushes, MEMORY.md edits, and skill installation unless a user explicitly approves each action.

Risk: Optional proactive checks may inspect personal or work data sources such as email, calendar, and weather context.

Mitigation: Keep those integrations opt-in and limit heartbeat access to the minimum data needed for the configured check.

Risk: Idle-time self-improvement routines may promote incorrect lessons or stale task conclusions into long-term memory.

Mitigation: Review generated status reports and memory promotions before applying them to persistent agent memory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ares521521-design/skills/icecube-heartbeat)

## Skill Output:

**Output Type(s):** [markdown, configuration, guidance]

**Output Format:** [Markdown with configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes suggested heartbeat prompts, supporting file templates, response rules, and state tracking guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
