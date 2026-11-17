## Description:

Assesses architecture decisions, ADR compliance, and coupling

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review system design changes, refactoring, and dependency restructuring. It helps assess ADR compliance, module interactions, design principles, and architecture risks before changes are merged.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports behavior beyond architecture review, and scanner coverage is partial because three local references were missing.

Mitigation: Review the listed configuration dependencies and any available local references, then limit repository and data access to what the architecture review needs.

## Reference(s):

- [FPF Framework](https://github.com/ailev/FPF)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [Structured Markdown architecture review with optional JSON findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are expected to include file locations and supporting code anchors.]

## Skill Version(s):

1.10.3 (source: SKILL.md frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
