## Description:

Analyzes code change impact with risk scoring and affected-node mapping. Use before merging to understand what a change touches and what lacks test coverage

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reviewers use this skill before merging to map code changes to affected nodes, rank impact risk, and identify affected functions without test coverage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill checks an agent configuration directory while looking for an optional tool; the available security review is marked partial.

Mitigation: Review that check before running the skill and treat the security evidence as incomplete.

## Reference(s):

- [Pensive plugin page](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON]

**Output Format:** [Markdown risk table and structured findings JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include affected nodes, file locations, source anchors, test coverage status, overall risk, and suggested actions.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
