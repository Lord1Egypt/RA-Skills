## Description:

Get real-time trending topics and hot searches from major Chinese social media platforms including Weibo, Zhihu, Baidu, Douyin, Toutiao, and Bilibili.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neverchenx](https://clawhub.ai/user/neverchenx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch and summarize current trend lists from major Chinese social media, search, news, and video platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill makes third-party network requests to fetch live trend data.

Mitigation: Invoke it only for supported Chinese trend platforms and disclose or review third-party API use where needed.

Risk: Trend responses can be stale, unavailable, or shaped by upstream platform and API behavior.

Mitigation: Handle network errors, check response timestamps, and cache or retry results before presenting them as current.

## Reference(s):

- [60s API Documentation](https://docs.60s-api.viki.moe)
- [60s GitHub Repository](https://github.com/vikiboss/60s)
- [ClawHub Skill Page](https://clawhub.ai/neverchenx/skills/hot-topics)
- [Publisher Profile](https://clawhub.ai/user/neverchenx)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, markdown]

**Output Format:** [Markdown with Python and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON API response examples and concise trend summaries.]

## Skill Version(s):

1.1.0 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
