## Description:

基于快手的实时数据，通过自然语言检索快手上的达人。支持按关键词、点赞数等方向筛选，并查看达人的作品及作品表现数据、互动数据、评论内容等，分析达人画像、内容特点、活跃表现和近期作品等，帮助用户快速发现和判断适合合作的达人。支持三大能力：(1) 关键词搜索视频，可按点赞数、发布时间、视频时长筛选排序；(2) 达人作品抓取，按主页链接获取公开作品列表；(3) 视频评论分析，按视频链接获取评论内容与互动数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

内容创作者、品牌营销人员、市场分析师和达人经纪团队可用它搜索快手公开视频、查看创作者作品与互动数据、分析评论，从而辅助选题研究、竞品观察和达人合作筛选。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms or links are sent to the third-party GuaiKei service, and returned timestamps use Beijing time.

Mitigation: Avoid queries containing sensitive information and account for the Beijing time zone when interpreting results.

Risk: The security scan was incomplete: 12 of 32 components were only partially inspected, so confidence is medium.

Mitigation: Review the partially inspected executable files before installation or execution.

## Reference(s):

- [完整选项参数说明](references/options.md)
- [更新日志](references/changelog.md)
- [快手达人发现与洞察服务](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [Structured JSON results with concise agent-facing summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns public video search results, creator profile and post metrics, or video comments; available result counts depend on the token plan.]

## Skill Version(s):

1.1.2 (source: frontmatter, changelog, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
