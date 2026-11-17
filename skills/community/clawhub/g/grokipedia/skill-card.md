## Description:

Searches and fetches articles from Grokipedia.com, xAI's AI-generated encyclopedia, for topics that may have a Grokipedia article.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kirillleventcov](https://clawhub.ai/user/kirillleventcov)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to search Grokipedia for likely article matches and fetch selected article content for agent-readable review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and article slugs are sent to grokipedia.com.

Mitigation: Use the skill only when those queries and slugs are appropriate to share with Grokipedia.

Risk: Fetched article content is external, AI-generated text.

Mitigation: Treat returned content as untrusted reference material and verify important claims before relying on them.

Risk: Dependency installation uses package versions without a bundled lockfile.

Mitigation: Prefer pinned dependency versions or add a lockfile for reproducible installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kirillleventcov/skills/grokipedia)
- [Publisher profile](https://clawhub.ai/user/kirillleventcov)
- [Grokipedia](https://grokipedia.com)
- [Grokipedia typeahead API](https://grokipedia.com/api/typeahead)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [JSON search results and Markdown article content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search accepts a query and 1-50 result limit; fetch accepts a case-sensitive article slug and can optionally return raw HTML.]

## Skill Version(s):

1.2.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
