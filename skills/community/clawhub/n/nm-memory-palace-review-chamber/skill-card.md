## Description:

Captures and retrieves PR-review findings in memory palaces to preserve architectural decisions, patterns, and standards for future reference.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill after code reviews to identify durable findings, organize them as decisions, patterns, standards, or lessons, and retrieve related review knowledge during future work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The described GitHub review and posting capability may be broader than the skill's stated knowledge-capture purpose.

Mitigation: Review requested actions and repository permissions before use, and check review content before it is posted.

Risk: The security assessment covered 75% of components; one module was partly analyzed and a local path reference was unresolved.

Mitigation: Inspect the partly analyzed module and resolve the local path before relying on the assessment.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-memory-palace-review-chamber)
- [Memory Palace plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/memory-palace)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Guidance]

**Output Format:** [Structured review knowledge entries, Markdown summaries, and optional JSON exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content depends on the supplied review findings and project memory-palace context.]

## Skill Version(s):

1.10.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
