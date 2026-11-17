## Description:

Garry Tan's gstack-inspired multi-perspective code review for OpenClaw that analyzes git diffs, runs project checks, and returns actionable feedback from product, engineering, and QA viewpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[klesenchang](https://clawhub.ai/user/klesenchang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review uncommitted changes, branches, pull requests, or specified files through product, architecture, and QA lenses. It helps structure findings, test status, build and lint results, and concrete action items for code review decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run repository test, lint, type-check, and build commands that execute code from the project under review.

Mitigation: Use static review for untrusted changes, or run checks in a disposable sandbox with no credentials and restricted network access.

## Reference(s):

- [gstack](https://github.com/garrytan/gstack)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown review report with inline shell commands and action items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Review output is organized by CEO/Product, Engineering, and QA perspectives with summary, check status, verdicts, and prioritized action items.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence, artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
