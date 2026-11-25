## Description:

用于快手数据分析、快手视频详情、快手作品数据、互动指标、内容调研和快手内容分析。覆盖 Kuaishou / Kwai，来自GuaiKei社媒数据助手。提供快手关键词搜索、快手博主作品获取、快手视频评论获取等功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, and analysts use this skill to search public Kuaishou videos, review a creator's public posts and profile metrics, or examine video comments for topic research, competitor review, and audience insights. It requires a GuaiKei API token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan reports a benign verdict with medium confidence: only 20 of 32 components were fully scanned, and tool-misuse analysis was degraded.

Mitigation: Review the skill before installation, including scripts that were not fully interpreted, if you need stronger assurance.

## Reference(s):

- [GuaiKei service and token access](https://www.guaikei.com)
- [ClawHub release page](https://clawhub.ai/why20261/skills/kuaishou-detail-guaikei)
- [Command options](artifact/references/options.md)
- [Release changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, text]

**Output Format:** [Structured JSON containing public video search results, creator profile and post data, or video comments.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the requested query and available public data. A GUAIKEI_API_TOKEN is required; requests are sent to GuaiKei.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
