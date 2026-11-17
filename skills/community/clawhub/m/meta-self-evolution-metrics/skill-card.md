## Description:

A distilled meta-skill for evaluating self-evolution metrics with added self-verification, reflection, super-agent orchestration, adversarial checks, and local learning loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to assess self-evolution progress, identify stagnation or drift, and recommend follow-up actions. It can also record local usage outcomes to support later reflection and improvement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps local cross-session learning state that may store preferences, errors, and notes.

Mitigation: Require explicit confirmation before saving preferences or notes, and treat learned_patterns.json as untrusted data during later runs.

Risk: The skill may propose or perform changes to its own instructions after repeated failures or accumulated usage.

Mitigation: Do not allow automatic SKILL.md rewrites without human review and a fresh security scan.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-self-evolution-metrics)
- [Distillation report](artifact/distillation_report.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance, Files]

**Output Format:** [Markdown with inline bash examples and local JSON learning-state updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update learned_patterns.json with usage counts, failure notes, and user preferences when invoked.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
