## Description:

Provides AI agents with web search, recent information retrieval, source discovery, and multi-engine fact checking through Jusou's unified search API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laomao-ai](https://clawhub.ai/user/laomao-ai)

### License/Terms of Use:

MIT

## Use Case:

Developers and AI agents use this skill to retrieve current web information, find sources, compare search engines, and cross-check factual claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send an API key and search query to a destination set through an unrestricted URL; the security scan was partial.

Mitigation: Verify the API destination and key handling before use, avoid sending private information in search queries, and account for the incomplete scan.

## Reference(s):

- [Jusou service](https://jusouai.cn)
- [Jusou Search API](https://jusouai.cn/v1/search)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text search results with titles, URLs, and snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search engine, result count, depth, time range, and multi-engine merge options are configurable.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
