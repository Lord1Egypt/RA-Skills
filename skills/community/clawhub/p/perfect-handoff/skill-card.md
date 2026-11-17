## Description:

Reconciles project knowledge, writes a compact continuation handoff, and provides a ready-to-paste prompt for a new session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcjl](https://clawhub.ai/user/0xcjl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and project maintainers use this skill to reconcile project documentation, capture verified work and open questions in a compact handoff, and prepare a new session to resume safely. It also supports read-only restoration from an existing handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project documentation could be changed or summarized inaccurately during closeout.

Mitigation: Run only at a trusted project root, authorize documentation edits explicitly, and review the resulting handoff against project files before relying on it in a fresh session.

## Reference(s):

- [Perfect Handoff on ClawHub](https://clawhub.ai/0xcjl/skills/perfect-handoff)
- [Project knowledge closeout](references/closeout.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Compact Markdown handoff document and paste-ready text prompt]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Handoff has a 6,000-character maximum; restore-only mode reports project state without writing files.]

## Skill Version(s):

1.0.1 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
