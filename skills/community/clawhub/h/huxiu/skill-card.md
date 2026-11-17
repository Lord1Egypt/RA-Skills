## Description:

Retrieves Huxiu's latest articles across technology, business, finance, and other topics and presents their published details without inventing missing information.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huxiu](https://clawhub.ai/user/huxiu)

### License/Terms of Use:

MIT-0

## Use Case:

Readers and researchers use this skill to check Huxiu's newest articles and follow links to recent reporting and commentary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fetching articles contacts Huxiu's API over the network.

Mitigation: Authorize external network access under the environment's policy before requesting the feed.

Risk: Article details may be missing or the feed may fail.

Mitigation: Report failures and omit unavailable details rather than inventing them.

## Reference(s):

- [Huxiu News on ClawHub](https://clawhub.ai/huxiu/skills/huxiu)
- [Huxiu latest articles feed](https://api-ms-mcp.huxiu.com/skills/latestArticles)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Article list with titles, dates, authors, links, and available snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source order and reports missing or failed results without fabrication]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
