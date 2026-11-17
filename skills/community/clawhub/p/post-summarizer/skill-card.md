## Description:

全网新闻/文章阅读总结助手。支持从主流新闻网站（钛媒体、36氪、虎嗅、华尔街见闻、腾讯新闻、新浪财经、Reuters、BBC、NYT 等）读取最新文章并深度总结。当用户说"帮我看XX新闻"、"总结这篇"、"最新XX资讯"、"搜索XX关键词新闻"、"对比这几篇文章"等类似需求时触发。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shaohaojie1](https://clawhub.ai/user/shaohaojie1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch, summarize, and compare public news articles from specified sources, keyword searches, or provided URLs. It is designed for Simplified Chinese news briefings, article summaries, and cross-article comparison reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad news prompts may cause the agent to fetch several external public sources.

Mitigation: Keep browsing scoped to the user's requested source, URL, or keyword set, and summarize only retrieved content.

Risk: News summaries can become misleading if source retrieval fails or article timing is unclear.

Mitigation: Include source and time fields when available, retry with nearby sources after fetch failures, and state when no reliable result was found.

Risk: The skill is configured to answer in Simplified Chinese, which may not match every deployment's language expectations.

Mitigation: Confirm that Simplified Chinese output is appropriate for the intended users before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shaohaojie1/skills/post-summarizer)
- [Publisher profile](https://clawhub.ai/user/shaohaojie1)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Simplified Chinese Markdown summaries, comparison reports, and news briefings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include source and time fields when available and are grounded in fetched or searched public article content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
