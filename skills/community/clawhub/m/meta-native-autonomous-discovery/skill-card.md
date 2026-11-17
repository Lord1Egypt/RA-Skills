## Description:

A distilled meta-skill for native autonomous discovery that guides hypothesis generation, evidence scoring, self-verification, reflection, and iterative learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to structure autonomous discovery tasks around candidate hypotheses, discriminating observations, evidence scoring, confidence tracking, and post-run reflection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist local notes about usage, errors, and preferences, which may include sensitive task context.

Mitigation: Review or disable learned_patterns.json storage before use on sensitive work, and remove stored notes after each session when retention is not needed.

Risk: The skill asks the agent to rewrite its own instructions after repeated errors or usage.

Mitigation: Require human review before any SKILL.md change and treat suggested self-edits as proposals only.

Risk: The skill makes strong claims about self-verification, reflection, and autonomous improvement that may exceed demonstrated behavior.

Mitigation: Validate outputs against external evidence and rely on explicit confidence notes rather than assuming self-verification proves correctness.

## Reference(s):

- [Distillation report](artifact/distillation_report.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with structured hypotheses, evidence trails, confidence notes, and optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local learned_patterns.json notes when the learner script is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
