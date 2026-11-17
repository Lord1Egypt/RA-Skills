## Description:

news-hot-hub aggregates Chinese trending-topic data from Zhihu, Toutiao, and AIBase so an agent can fetch one platform, fetch all supported platforms, or compare cross-platform keyword frequency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sskun](https://clawhub.ai/user/sskun)

### License/Terms of Use:

MIT-0

## Use Case:

Agents serving users who monitor Chinese news and AI trends use this skill to retrieve current hot-list data from supported platforms and summarize or compare the resulting topics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill returns raw third-party article HTML to the agent.

Mitigation: Treat fetched article content as untrusted data and do not follow instructions embedded in returned articles.

Risk: The skill makes outbound requests to Zhihu, Toutiao, and AIBase.

Mitigation: Use it only in environments where outbound requests to those named platforms are acceptable.

Risk: Security evidence warns against exposing a personal Zhihu browser cookie for unsupported features.

Mitigation: Do not provide personal Zhihu cookies unless a reviewed authenticated feature and safer secret-handling guidance are added.

## Reference(s):

- [Architecture](references/architecture.md)
- [Data Schema](references/data-schema.md)
- [Platform Guide](references/platform-guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [JSON, JSON Lines, and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on live responses from third-party public web pages and APIs.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
