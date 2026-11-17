## Description:

Reconciles project documentation and persistent agent memory against the code at the end of a development session or milestone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vincentjiang06](https://clawhub.ai/user/vincentjiang06)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill after coding milestones to bring README, project guidance, documentation, and agent memory into alignment with verified changes. It audits for stale or oversized knowledge, edits supported facts, and presents sensitive changes for approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent documentation or memory edits could preserve incorrect or outdated facts.

Mitigation: Check edits against the code and verification anchors, and review the change summary before relying on updated guidance.

Risk: Memory deletions, batch rewrites, or new agent rules could remove context or change future agent behavior.

Mitigation: Review pending proposals and approve only the intended changes; use a version-pinned installation when possible.

## Reference(s):

- [Neat on ClawHub](https://clawhub.ai/vincentjiang06/skills/neat)
- [Change-to-documentation sync matrix](artifact/references/sync-matrix.md)
- [Agent memory and configuration paths](artifact/references/agent-paths.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Shell commands, Documentation and memory edits]

**Output Format:** [Edited project knowledge files and a Markdown change summary with pending proposals and audit results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proposed memory deletions, batch rewrites, and agent-rule changes require user confirmation.]

## Skill Version(s):

1.3.0 (source: ClawHub release metadata, skill frontmatter, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
