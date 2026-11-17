## Description:

Research the last 30 days across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, GitHub, and grounded web search, returning a ranked, clustered brief with citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baofeng-tech](https://clawhub.ai/user/baofeng-tech)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and agents use this skill to scan recent public social, market, code, and web evidence for products, companies, people, launches, trends, and competitor comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics and retrieved snippets may be sent to AISA and selected external services.

Mitigation: Use the skill only when sharing those topics and snippets with the configured services is acceptable.

Risk: Local project configuration can steer some network behavior, including optional custom endpoints.

Mitigation: Run the skill from trusted workspaces, keep credentials in trusted process environment variables, and enable Xiaohongshu or custom endpoints only when you control and trust the endpoint.

Risk: Untrusted search and social snippets can influence planning and ranking.

Mitigation: Review cited sources and ranked findings before relying on the brief for decisions or downstream automation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baofeng-tech/skills/last30days-aisa-api)
- [AIsa homepage](https://aisa.one)
- [AIsa models guide](https://aisa.one/docs/guides/models)
- [AIsa API reference](https://aisa.one/docs/api-reference)
- [AIsa chat completion API](https://aisa.one/docs/api-reference/chat/createchatcompletion)
- [AIsa Twitter advanced search API](https://aisa.one/docs/api-reference/twitter/get_twitter-tweet-advanced-search)
- [AIsa YouTube search API](https://aisa.one/docs/api-reference/search/get_youtube-search)
- [AIsa Tavily search API](https://aisa.one/docs/api-reference/search/post_tavily-search)
- [AIsa Polymarket markets API](https://aisa.one/docs/api-reference/prediction-market/get_polymarket-markets)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown brief by default, with optional JSON or compact/context text output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include a query plan, ranked candidates, clusters, items by source, provider runtime, source-level errors, dates, engagement, and URLs.]

## Skill Version(s):

1.0.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
