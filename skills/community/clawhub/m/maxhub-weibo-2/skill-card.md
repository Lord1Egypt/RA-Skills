## Description:

Queries Weibo posts, user data, search results, trending topics, comments, and videos through MaxHub APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiewxx](https://clawhub.ai/user/xiewxx)

### License/Terms of Use:

MIT-0

## Use Case:

External users such as media teams, brands, and analysts can query and summarize Weibo content, user data, search results, and trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The authoritative security summary flags a mismatch between the stated Weibo query purpose and observed behavior, and says some instructions may route requests outside that scope; the scan is partial.

Mitigation: Review the request destinations and referenced endpoint paths against trusted provider documentation before execution. Do not provide API keys or platform cookies to destinations you have not verified.

## Reference(s):

- [Server-resolved source repository](https://github.com/XieWxx/maxhub-weibo)
- [ClawHub release page](https://clawhub.ai/xiewxx/skills/maxhub-weibo-2)
- [MaxHub API provider](https://www.aconfig.cn)
- [Post and comment API references](artifact/references/api-post.md)
- [User API references](artifact/references/api-user.md)
- [Search API references](artifact/references/api-search.md)
- [Trending API references](artifact/references/api-trending.md)
- [Video and feed API references](artifact/references/api-video-feed.md)
- [Parameter mappings](artifact/references/param-mappings.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown summaries and tables; configuration guidance may include shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summarizes results returned by Weibo queries.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
