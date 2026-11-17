## Description:

Meta Metacognitive Monitoring helps agents decide when to proceed, seek help, degrade, defer, or flag overconfidence, adding self-verification, reflection, and a learner-backed memory loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill as a metacognitive guardrail for long-running agent workflows, helping an agent calibrate confidence, request help, choose conservative execution, and record lessons from prior decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist learned preferences and decision notes across sessions.

Mitigation: Use it only where persisted state is expected, inspect and clear learned state regularly, and avoid recording credentials, private prompts, or sensitive workflow details.

Risk: The skill text proposes automatically rewriting its own SKILL.md after repeated overconfidence alerts.

Mitigation: Require explicit user review and approval before any skill instruction file is changed.

Risk: Automatically reused preferences can alter future agent behavior without a visible approval step.

Mitigation: Surface stored preferences before applying them and provide a clear way to disable or reset learned behavior.

## Reference(s):

- [Distillation report](artifact/distillation_report.md)
- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-metacognitive-monitoring)

## Skill Output:

**Output Type(s):** [guidance, text, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local learned-pattern state when the bundled learner script is used.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
