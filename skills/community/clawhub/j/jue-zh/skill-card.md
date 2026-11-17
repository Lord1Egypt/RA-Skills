## Description:

A Chinese-language agent self-review workflow that activates after failures, repeated attempts, user dissatisfaction, or unverified completion claims to guide evidence-based diagnosis and next actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kscz0000](https://clawhub.ai/user/kscz0000)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to make an agent pause after repeated failure patterns, inspect assumptions, verify evidence with tools, and report concrete next steps. It is especially suited to troubleshooting, code review, planning, research, and multi-agent handoff situations where unverified assumptions or repeated approaches can block progress.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may activate the self-review workflow during common requests to rethink, try another approach, check best practices, or review code.

Mitigation: Use the skill when persistent, evidence-driven failure analysis is desired, and scope activation to task failure, repeated attempts, unverified completion, or explicit review prompts.

Risk: The workflow may spend extra effort using tools before asking the user for clarification.

Mitigation: Set a clear investigation budget for time-sensitive work and require concise evidence summaries before extended follow-up actions.

## Reference(s):

- [Three Poisons](references/three-poisons.md)
- [Seven Jue](references/seven-jue.md)
- [Five Steps](references/five-steps.md)
- [Agent Team Integration](references/agent-team.md)
- [ClawHub Skill Page](https://clawhub.ai/kscz0000/skills/jue-zh)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown diagnostic reports with concise action steps and optional command evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include structured self-review fields such as failure pattern, verified facts, excluded causes, current hypothesis, and next action.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
