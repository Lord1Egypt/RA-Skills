## Description:

Provides a distilled cross-engine memory workflow with self-verification, reflection, and a lightweight learner for cross-session pattern tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add a structured memory, reflection, and self-check loop around cross-engine workflows. It is intended for agents that need to record task patterns, user preferences, and failure notes across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores cross-session user data for preferences, task notes, and failure patterns.

Mitigation: Use it only when a local memory layer is intended, avoid storing secrets or sensitive content, and provide a way to inspect and delete learned_patterns.json.

Risk: The skill instructs the agent to rewrite its own SKILL.md after repeated errors.

Mitigation: Remove or disable the self-write rule before deployment, and require human review for any proposed instruction changes.

Risk: Automatically saved preferences or task notes may capture user data without enough consent.

Mitigation: Require explicit consent before saving preferences or task notes and document what is retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-memory-cross-engine)
- [Distillation report](artifact/distillation_report.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and Python script guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local learned_patterns.json memory records when the learner script is used.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
