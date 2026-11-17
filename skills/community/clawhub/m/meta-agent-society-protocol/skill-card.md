## Description:

meta-agent-society-protocol helps agents structure multi-agent task assignment and conflict resolution workflows with added self-verification, reflection, and local learning notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to model agents and tasks, allocate work, resolve competing proposals, and run auditable multi-agent workflows with verification and reflection steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may store and reuse local user or usage notes across sessions.

Mitigation: Require explicit approval before any learning write and avoid storing raw user content or sensitive preferences.

Risk: The skill describes automatic updates to its own instructions after repeated errors or usage.

Mitigation: Do not allow automatic edits to SKILL.md; require human review for any proposed instruction changes.

## Reference(s):

- [Distillation Report](artifact/distillation_report.md)
- [ClawHub Skill Page](https://clawhub.ai/qq435912743/skills/meta-agent-society-protocol)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local learned_patterns.json notes when learning commands are run.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
