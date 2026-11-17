## Description:

Meta Academic Tutor is an academic tutoring skill distilled from academic-tutor that guides learners with a Socratic three-part response structure plus self-verification, reflection, and local learning memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Students and academic learners use this skill to work through coursework, problem-solving, and writing-related learning tasks without receiving direct answer substitution. It is intended to keep responses in a question, hint, and next-step tutoring structure while respecting academic integrity boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores user-derived profile and preference data locally without clear consent, deletion, or data-minimization controls.

Mitigation: Require explicit user consent, document retention and deletion controls, isolate per-user data, and narrow persisted fields before broad deployment.

Risk: The artifact directs agents to rewrite the skill instructions during self-evolution, which can introduce unreviewed behavior changes.

Mitigation: Remove automatic SKILL.md self-modification or gate any proposed changes behind review, version control, and security scanning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-academic-tutor)
- [Distillation report](artifact/distillation_report.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed three-part tutoring response pattern for learner-facing guidance.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
