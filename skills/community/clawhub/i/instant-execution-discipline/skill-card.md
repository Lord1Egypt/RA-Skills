## Description:

Revenue-focused execution operating system for agents: converts "do it now" requests into immediate tool actions, enforces strict start/progress/finish SLAs, and prevents kickoff-only false completions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rui131](https://clawhub.ai/user/rui131)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to make agents begin execution-heavy work immediately, maintain progress visibility, and report completion with evidence. It is best suited for conversion-sensitive publishing, release, distribution, cron, and post-release workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill pushes agents to start tool, subagent, or cron execution immediately, which can reduce review time before changes are made.

Mitigation: Add explicit confirmation gates for publishing, release, cron, Discord reporting, and other business workflows before deployment.

Risk: The postmortem rule can encourage permanent memory, mission, or skill-rule changes after delays.

Mitigation: Disable automatic self-modification and require human review before changing persistent agent rules or memory.

Risk: KPI logging may write workflow details to memory or Obsidian daily notes.

Mitigation: Decide in advance what KPI data may be persisted and redact sensitive business, customer, or channel details.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text, Configuration]

**Output Format:** [Markdown guidance with status-message templates, completion-report fields, and KPI logging instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes timing SLAs for start, progress, and completion messages, plus optional KPI logging for revenue and operations workflows.]

## Skill Version(s):

0.1.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
