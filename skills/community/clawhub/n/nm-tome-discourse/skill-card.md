## Description:

Scans HN, Lobsters, Reddit, and tech blogs for community experience reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical decision makers use this skill to gather practitioner experiences and opinions about a technology or approach from Hacker News, Lobsters, Reddit, and tech blogs. It is intended for community experience reports rather than academic research or code examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries sent to third-party services could reveal private details from the request.

Mitigation: Review search terms before sending them and omit private or sensitive details.

Risk: A local path-like reference was unresolved, leaving the security review partial.

Mitigation: Resolve and inspect the referenced path, then review the skill before relying on it.

## Reference(s):

- [Night Market Tome plugin page](https://github.com/athola/claude-night-market/tree/master/plugins/tome)

## Skill Output:

**Output Type(s):** [Analysis, Text]

**Output Format:** [Community discussion findings with source-channel attribution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries at least two community channels per invocation; if all searches fail, reports the failure rather than returning fabricated or empty findings.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
