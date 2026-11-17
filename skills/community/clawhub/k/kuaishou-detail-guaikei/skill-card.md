## Description:

用于快手数据分析、快手视频详情、快手作品数据、互动指标、内容调研和快手内容分析。覆盖 Kuaishou / Kwai，来自GuaiKei社媒数据助手。提供快手关键词搜索、快手博主作品获取、快手视频评论获取等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, and analysts use this skill to retrieve public Kuaishou videos, creator posts, and comments for topic research, competitor review, and discussion analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and video or profile links are sent to GuaiKei with the API token; live service retention was not verified.

Mitigation: Avoid sensitive queries and links, and review GuaiKei's pricing and privacy terms before use.

Risk: When optional logging is enabled, queries and results are saved in local temporary-directory logs.

Mitigation: Keep logging disabled unless needed, then restrict access to and remove the saved logs after use.

## Reference(s):

- [Command options](references/options.md)
- [Release changelog](references/changelog.md)
- [GuaiKei service and access](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON]

**Output Format:** [JSON envelope with Kuaishou video search, creator-post, or comment results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Engagement counts may be numbers or strings depending on the command; compare fields using the supplied schemas.]

## Skill Version(s):

1.1.1 (source: frontmatter, package.json, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
