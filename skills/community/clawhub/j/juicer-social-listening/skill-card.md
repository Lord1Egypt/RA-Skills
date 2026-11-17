## Description:

Social listening for any topic, product category or industry using Juicer. Pulls recent posts from Reddit, TikTok, X, YouTube, Instagram, Bluesky and more, then summarises what people say, the recurring questions and complaints and the posts worth reading, with links. Use for "what are people saying about X", "trend research", "audience research", "content ideas from real conversations", "find real quotes for an article".

This skill is ready for commercial/non-commercial use.

## Publisher:

[juicer](https://clawhub.ai/user/juicer)

### License/Terms of Use:

MIT-0

## Use Case:

External researchers, marketers, product teams, and content creators can use this skill to review recent public conversations about a topic. It organizes relevant posts into themes, questions, complaints, and notable examples with links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to Juicer and searches consume credits.

Mitigation: Show the proposed searches and credit estimate before running, check the available balance, and enable recurring reports only when requested.

Risk: Recent post results are best effort and do not represent a complete archive or every post on a network.

Mitigation: State which networks and terms were searched, disclose empty or timed-out sources, and describe results as posts found rather than exhaustive coverage.

## Reference(s):

- [Juicer MCP server documentation and permissions](https://developers.juicer.io/mcp-server)
- [Juicer developer access](https://www.juicer.io/developer)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Text]

**Output Format:** [Markdown digest with linked posts and short quoted excerpts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Organizes findings into themes, questions, complaints, and notable posts; reports search coverage and credit use.]

## Skill Version(s):

1.0.1 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
