## Description:

Analyzes changesets with risk scoring, categorization by type and impact, and release note preparation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reviewers use this skill to establish a comparison baseline, categorize changes, assess their risks, and prepare summaries for code reviews, release notes, or planning. It covers git diffs and other changesets such as configuration, API, schema, and document revisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The linked external repository was outside the security scan's scope.

Mitigation: Review and scan the linked repository before installing or enabling components from the full plugin.

## Reference(s):

- [ClawHub release](https://clawhub.ai/athola/skills/nm-imbue-diff-analysis)
- [Project homepage (declared in skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/imbue)
- [sem entity-level diff tool](https://github.com/Ataraxy-Labs/sem)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Structured change analysis and summaries in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include the baseline, change categories, risk levels, review focus, dependencies, and scope counts when available.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
