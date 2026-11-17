## Description:

Search public Kuaishou videos by keyword and retrieve public creator posts or video comments as structured JSON for content research, topic selection, trend monitoring, and competitor analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

External content creators, marketers, and analysts can search public Kuaishou videos and review public creator posts or comments to research topics, monitor trends, compare competitors, and organize content ideas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and video or profile links are sent to the third-party GUAIKEI service; comment and creator-data retrieval capabilities are broader than the skill's short stated purpose suggests.

Mitigation: Review the search, comment, and creator retrieval modes before use, and send only public-data queries you are comfortable sharing with GUAIKEI.

## Reference(s):

- [Command options](references/options.md)
- [Release changelog](references/changelog.md)
- [GUAIKEI service and token access](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [Structured JSON response containing search results, creator profile and post data, or video comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result size depends on the requested limit and token plan; monthly token limits are 30 search results, 50 creator posts, and 60 comments.]

## Skill Version(s):

1.1.1 (source: frontmatter, package.json, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
