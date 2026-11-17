## Description:

Grit helps OpenClaw persist through blocked tasks by escalating tools and tactics methodically while following workspace SOPs and safety rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rocketship4545-a11y](https://clawhub.ai/user/rocketship4545-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Grit when a task is blocked by flaky UI, brittle automation, or weak default tooling and they want the agent to keep trying materially different tactics until it solves the task or reaches a genuine external blocker.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can auto-trigger broadly and encourages aggressive escalation, including installing tools or using authenticated sessions.

Mitigation: Install only where that behavior is intended, review workspace SOPs, and require explicit approval before installing software or skills, using authenticated browser sessions, or switching to direct API or CLI actions.

## Reference(s):

- [Escalation Ladder](references/escalation-ladder.md)
- [Grit ClawHub Release](https://clawhub.ai/rocketship4545-a11y/skills/grit)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown guidance with short progress updates and inline commands or code when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include proposed tool changes, installation steps, or blocker reports subject to user approval and workspace SOPs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
