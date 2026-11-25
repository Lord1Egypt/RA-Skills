## Description:

一站式快手运营工具，融合选题灵感、数据分析模块。支持爆款标题、热点选题、粉丝分析等，覆盖快手运营数据获取场景。当用户要搜索快手视频/抓取博主作品/拉取视频评论时使用，输出结构化数据，用于爆款选题、竞品监控、KOL 筛选、评论舆情与趋势洞察。支持三大能力：(1) 关键词搜索视频，可按点赞数、发布时间、视频时长筛选排序；(2) 达人作品抓取，按主页链接获取公开作品列表；(3) 视频评论分析，按视频链接获取评论内容与互动数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

快手运营人员、内容创作者和市场分析师可用关键词搜索公开视频、查看博主公开作品与互动数据，并读取视频评论，辅助选题、竞品观察和舆情分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and video or profile links are sent to the third-party service at guaikei.com.

Mitigation: Avoid confidential queries and links; submit only information you are comfortable sharing with that service.

## Reference(s):

- [Options and parameter guide](references/options.md)
- [Changelog](references/changelog.md)
- [Service and token setup](https://www.guaikei.com)
- [ClawHub release page](https://clawhub.ai/why20261/skills/kuaishou-yunying-zhushou)

## Skill Output:

**Output Type(s):** [JSON data, Shell commands]

**Output Format:** [Structured JSON results and CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results cover public Kuaishou content; per-plan request limits apply.]

## Skill Version(s):

1.1.2 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
