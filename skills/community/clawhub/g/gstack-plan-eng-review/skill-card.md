## Description:

Eng manager-mode plan review that helps lock in an execution plan by reviewing architecture, data flow, diagrams, edge cases, test coverage, and performance before implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loocor](https://clawhub.ai/user/loocor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review implementation plans before coding, with structured attention to architecture, existing code reuse, test coverage, failure modes, and operational risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may create a test-plan file or ask to update TODO tracking during a review.

Mitigation: Decline write-oriented options when a read-only plan review is required.

Risk: Opinionated planning guidance could be incorrect or mismatched to repository constraints.

Mitigation: Review recommendations against the actual codebase, design docs, and team requirements before implementation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/loocor/skills/gstack-plan-eng-review)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with structured review sections and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce a test-plan Markdown file and may ask before updating TODO tracking.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
