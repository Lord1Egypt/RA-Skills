## Description:

Manage state machines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill for state-related workflows, machine task automation, and state machine operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill references an external state_machine.py script that was not included in the inspected artifact.

Mitigation: Use the skill only with a trusted copy of the referenced script and review it before execution.

Risk: The skill requires MACHINE_API_KEY, and exposed credentials could be misused.

Mitigation: Store MACHINE_API_KEY as a secret and avoid placing it in source files, logs, chat messages, or shell history.

Risk: The activation guidance is sparse, so users may misunderstand which external machine API or environment the skill targets.

Mitigation: Confirm the intended external API and runtime requirements before installing or using the skill.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-state-machine)
- [Publisher Profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The documented command returns JSON results and requires MACHINE_API_KEY to be configured.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
