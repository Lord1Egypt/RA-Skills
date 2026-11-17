## Description:

Research the last 30 days across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, GitHub, and grounded web search. Returns a ranked, clustered brief with citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and agent users use Last30days to gather recent social, market, code-hosting, and web signals for trend scans, competitor comparisons, launch reactions, and person or company profiles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Topics and prompts may be sent to AISA and public source APIs.

Mitigation: Use the skill only when that data sharing is acceptable for the task, and avoid submitting sensitive topics or prompts.

Risk: Project-local configuration can redirect Xiaohongshu network requests through XIAOHONGSHU_API_BASE.

Mitigation: Set sensitive keys and service endpoints in a user-controlled environment or user-owned config, and avoid --search=xhs from untrusted repositories.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/last30days)
- [AIsa](https://aisa.one)
- [Agent Skills specification](https://agentskills.io/specification)
- [AIsa model guide](https://aisa.one/docs/guides/models)
- [AIsa API reference](https://aisa.one/docs/api-reference)
- [AIsa OpenAI Chat API](https://aisa.one/docs/api-reference/chat/createchatcompletion)
- [AIsa Twitter Advanced Search API](https://aisa.one/docs/api-reference/twitter/get_twitter-tweet-advanced-search)
- [AIsa YouTube Search API](https://aisa.one/docs/api-reference/search/get_youtube-search)
- [AIsa Tavily Search API](https://aisa.one/docs/api-reference/search/post_tavily-search)
- [AIsa Polymarket Markets API](https://aisa.one/docs/api-reference/prediction-market/get_polymarket-markets)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown brief by default, with optional JSON containing the query plan, ranked candidates, clusters, per-source items, provider runtime, and source-level errors.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fail-soft across sources; requires Python 3.12+, bash, and AISA_API_KEY.]

## Skill Version(s):

1.0.4 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
