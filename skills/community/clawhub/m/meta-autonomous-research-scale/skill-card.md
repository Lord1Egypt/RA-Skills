## Description:

A model-distilled research meta-skill that adds self-verification, reflection, super-agent orchestration, and persistent learning on top of autonomous-research-scale workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers can use this skill to decompose research topics, coordinate parallel hypothesis work, synthesize findings, and record learning patterns across repeated use. Review is needed before deployment because the artifact claims self-verification and self-evolution behavior that is not fully implemented in the supplied files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to keep persistent learning data, which could capture sensitive task content or user preferences.

Mitigation: Review learner behavior before installation, avoid storing sensitive content, and restrict or clear local memory files as needed.

Risk: The skill describes automatic self-evolution and possible instruction rewrites, which could change behavior without adequate review.

Mitigation: Do not allow automatic SKILL.md rewrites; require human review and security scanning for any instruction changes.

Risk: The artifact claims self-verification, orchestration, and self-evolution safeguards that are not fully supplied in the artifact.

Mitigation: Treat those capabilities as unimplemented unless the referenced tools are separately supplied, reviewed, and tested.

## Reference(s):

- [Distillation report](artifact/distillation_report.md)
- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-autonomous-research-scale)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with optional shell commands and JSON learner records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write learned usage patterns to a local JSON memory file when the learner script is invoked.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
