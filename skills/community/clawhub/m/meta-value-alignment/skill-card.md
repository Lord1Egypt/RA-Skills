## Description:

Meta Value Alignment is a distilled value-alignment skill that adds self-verification, reflection, orchestration hooks, and iterative learning guidance for agent outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to guide value-alignment tasks through self-verification, reflection, and reusable preference-memory workflows. It is intended to support more traceable agent responses and pre-release alignment screening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist user-influenced preferences or task notes into local memory.

Mitigation: Review and reset learned_patterns.json regularly, and do not store sensitive user preferences or task content in notes.

Risk: The skill describes future self-modification of its own instructions without clear approval or scope controls.

Mitigation: Require human review before any SKILL.md modification and keep any instruction changes explicit, scoped, and reversible.

Risk: The security verdict is suspicious because the self-evolving behavior lacks clear reset and approval controls.

Mitigation: Install only when local memory and self-evolution behavior are acceptable for the deployment environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-value-alignment)
- [Publisher profile](https://clawhub.ai/user/qq435912743)
- [Distillation report](artifact/distillation_report.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update local learned_patterns.json state when the learner script is run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
