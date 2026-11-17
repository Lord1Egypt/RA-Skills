## Description:

Expert code review of current git changes with a senior engineer lens. Detects SOLID violations, security risks, and proposes actionable improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yorickshan](https://clawhub.ai/user/yorickshan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review current git changes for SOLID, architecture, security, reliability, performance, error handling, and boundary-condition issues. It produces a review-first report in Simplified Chinese and waits for explicit confirmation before implementing changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill forces review reports and follow-up prompts to Simplified Chinese.

Mitigation: Use this skill only when Simplified Chinese output fits the review workflow.

Risk: Code review findings may be incomplete or need project-specific validation.

Mitigation: Review suggested findings before acting and run the relevant tests, security checks, and deployment validation for the changed code.

## Reference(s):

- [Code Quality Checklist](references/code-quality-checklist.md)
- [Removal and Iteration Plan Template](references/removal-plan.md)
- [Security and Reliability Checklist](references/security-checklist.md)
- [SOLID Smell Prompts](references/solid-checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/yorickshan/skills/itfe-code-review)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown review report in Simplified Chinese with optional inline code-comment blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review-only by default; implementation requires explicit user confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
