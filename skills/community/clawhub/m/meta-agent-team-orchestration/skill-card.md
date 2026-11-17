## Description:

A distilled meta-agent orchestration skill that layers self-verification, reflection, super-agent workflow integration, and persistent learning on top of the agent-team-orchestration workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to coordinate multi-agent work with planning, execution, verification, reflection, and memory loops. It is intended for orchestration tasks where outputs should include traceable summaries, verification steps, known issues, and next actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages self-evolving orchestration and persistent free-form learning notes, which can retain sensitive or untrusted task context.

Mitigation: Review or bound the learning file behavior before use, and avoid using the skill with secrets or untrusted instructions unless persistence is disabled or controlled.

Risk: The skill relies on self-verification and reflection loops that may overstate reliability if not independently reviewed.

Mitigation: Require human review, tests, static checks, or acceptance criteria before acting on orchestration outputs in sensitive workflows.

## Reference(s):

- [Distillation report](artifact/distillation_report.md)
- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-agent-team-orchestration)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with task records, verification commands, acceptance criteria, and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May record local learning notes through its learner script when used by an agent.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
