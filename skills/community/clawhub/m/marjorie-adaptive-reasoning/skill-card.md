## Description:

Automatically assesses task complexity before each response and adjusts the agent's reasoning level when deeper deliberation would improve response quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marjoriebroad](https://clawhub.ai/user/marjoriebroad)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to have an agent classify request complexity and decide when deeper reasoning is appropriate before responding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may silently change the agent's reasoning mode across broad conversations without clear user control.

Mitigation: Install only where automatic reasoning-mode changes are acceptable; prefer deployments that make activation visible and user-controlled.

Risk: Automatic activation on every message can add latency or cost on tasks where speed matters more than depth.

Mitigation: Use the documented non-escalation and auto-downgrade criteria for quick, simple, conversational, or time-sensitive requests.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marjoriebroad/skills/marjorie-adaptive-reasoning)
- [Publisher profile: marjoriebroad](https://clawhub.ai/user/marjoriebroad)

## Skill Output:

**Output Type(s):** [guidance, text, shell commands, configuration]

**Output Format:** [Markdown guidance with decision tables and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May append reasoning-mode indicators to responses when the skill activates deeper reasoning.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
