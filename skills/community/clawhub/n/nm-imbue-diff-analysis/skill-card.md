## Description:

Analyzes changesets with risk scoring, categorization by type and impact, and release note preparation

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to compare a baseline with a changeset, group changes by structure and purpose, assess risks, and prepare summaries for code review, release notes, or planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incomplete baseline or repository context can lead to missed or misleading change assessments.

Mitigation: State the comparison baseline and intended consumer, then review the summary and risk levels against the source changes.

## Reference(s):

- [Project homepage](https://github.com/athola/claude-night-market/tree/master/plugins/imbue)
- [ClawHub release page](https://clawhub.ai/athola/skills/nm-imbue-diff-analysis)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Structured Markdown summaries with categorized changes, risk assessments, and release notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content depends on the supplied baseline and changeset.]

## Skill Version(s):

1.10.4 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
