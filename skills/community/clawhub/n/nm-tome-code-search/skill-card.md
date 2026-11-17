## Description:

Searches GitHub for existing implementations, libraries, or patterns

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill during research or standalone searches to find existing GitHub implementations, libraries, and code patterns relevant to a topic.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Topic-derived search queries may be sent to external search services and could expose private project details.

Mitigation: Review queries before searching and remove private names, code, or other sensitive details; use generic topic terms where possible.

## Reference(s):

- [Tome plugin page linked by the skill](https://github.com/athola/claude-night-market/tree/master/plugins/tome)
- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-tome-code-search)

## Skill Output:

**Output Type(s):** [Text, Structured data]

**Output Format:** [Ranked findings with repository metadata and relevance scores]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are sorted by relevance; if no results are found, the skill reports that explicitly.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
