## Description:

A distilled meta-skill for adversarial robustness tasks that adds self-verification, reflection, super-agent orchestration, and persistent learning around robustness evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and evaluators use this skill to probe adversarial input robustness, add self-checking and reflection steps to robustness workflows, and record learned patterns across evaluations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for persistent learning behavior that may retain sensitive prompts, evaluation details, or user preferences in learned_patterns.json.

Mitigation: Limit memory writes to explicit user-approved, non-sensitive summaries and review or delete retained state before sharing or reuse.

Risk: The skill describes self-modification behavior, including proposed updates to SKILL.md, that could introduce incorrect or misleading guidance.

Mitigation: Generate any skill changes as reviewed patches and scan them before installation or execution.

Risk: The robustness checks are positioned as an input-perturbation aid and do not replace domain safety review.

Mitigation: Use the outputs as preliminary robustness guidance and validate decisions against domain-specific safety, security, and policy requirements.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-adversarial-robustness)
- [Distillation report](artifact/distillation_report.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and optional JSON learner state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May record learned robustness patterns in learned_patterns.json when explicitly invoked.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
