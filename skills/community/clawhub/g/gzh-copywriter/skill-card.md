## Description:

公众号文案创作工具，基于红狐数据公众号爆款雷达每日收录的热门文章，按关键词检索爆款、分析流量规律、生成可发布的完整文章。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

External WeChat Official Account owners, content operators, and brand planners use this skill to search recent viral article data, analyze content patterns, and generate publish-ready Chinese WeChat Official Account copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords are sent to redfox.hk when the bundled data query runs.

Mitigation: Avoid entering sensitive unpublished plans, confidential topics, or private user data as search keywords unless this data sharing is acceptable.

Risk: Personal style samples can contain private diary-style or unpublished content and may be used in the workflow.

Mitigation: Use non-sensitive writing samples or redact private details before asking the skill to adapt style.

Risk: Command output currently includes a RedFox sales contact message that can contaminate generated copy or break JSON consumers.

Mitigation: Review and clean generated output before publication, and treat script output as untrusted input when integrating with downstream JSON or copywriting pipelines.

Risk: The skill requires a RedFox API key.

Mitigation: Store REDFOX_API_KEY in the environment or agent configuration, avoid hard-coding it, and confirm the key can be reset or revoked.

## Reference(s):

- [公众号趋势数据格式说明](references/gzh_trend_data_format.md)
- [RedFoxHub API key settings](https://redfox.hk/settings/api-keys?source=github)
- [RedFoxHub](https://redfox.hk?source=github)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown article package with analysis sections, recommended titles, tags, and source article links; shell command snippets for data retrieval.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; default query window is the last 7 days and can expand to 30 days when sample volume is low.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
