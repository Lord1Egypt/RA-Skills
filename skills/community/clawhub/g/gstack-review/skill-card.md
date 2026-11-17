## Description:

Pre-landing PR review that analyzes diffs against the base branch for SQL safety, LLM trust boundary violations, conditional side effects, scope drift, missing requirements, and other structural issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loocor](https://clawhub.ai/user/loocor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill before landing a pull request to inspect branch diffs, identify structural risks, and apply or request fixes for review findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can directly edit workspace files during a review flow.

Mitigation: Use review-only mode or require explicit approval before fixes on important branches, then inspect the resulting diff carefully.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loocor/skills/gstack-review)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and structured review findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include direct workspace edits for auto-fixable findings and batched user questions for judgment-based fixes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
