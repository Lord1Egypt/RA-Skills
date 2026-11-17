## Description:

Search and read news articles, sources, and headlines through News API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People and agents use this skill to search articles, retrieve current headlines, and list available news sources through a connected News API account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup runs a changing remote installer without verification or user approval.

Mitigation: Use a separately reviewed, pinned CLI installation and require approval before running installers.

## Reference(s):

- [News API documentation](https://newsapi.org/docs)
- [News API](https://newsapi.org)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [News API skill on ClawHub](https://clawhub.ai/oomol/skills/oo-news-api)

## Skill Output:

**Output Type(s):** [API data, JSON, Shell commands]

**Output Format:** [News results returned as JSON; actions are invoked with shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the connected News API account; requests may consume credit.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
