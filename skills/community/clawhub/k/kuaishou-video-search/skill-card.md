## Description:

快手高赞视频搜索工具。支持关键词获取快手实时高赞视频数据，助力创作者发现热门趋势、获取创作灵感。支持三大能力：(1) 关键词搜索视频，可按点赞数、发布时间、视频时长筛选排序；(2) 达人作品抓取，按主页链接获取公开作品列表；(3) 视频评论分析，按视频链接获取评论内容与互动数据。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

内容创作者、品牌营销人员和市场分析师可用关键词发现快手热门视频、查看公开博主作品和视频评论，以支持选题、竞品研究与舆情分析。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search keywords and video or profile links are sent to the third-party service at guaikei.com.

Mitigation: Tell the user what will be sent before running; use only public links and avoid sensitive search terms.

Risk: The security evidence reports a benign verdict with medium confidence after partial inspection of the scripts.

Mitigation: Review the skill source and publisher before installation, and consider the scan's stated confidence when deciding whether to use it.

## Reference(s):

- [快手数据服务](https://www.guaikei.com)
- [ClawHub skill page](https://clawhub.ai/why20261/skills/kuaishou-video-search)
- [完整选项参数说明](references/options.md)
- [更新日志](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON response envelope containing public video, creator, or comment data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result counts depend on token plan; timestamps use Beijing time.]

## Skill Version(s):

1.1.1 (source: frontmatter, changelog released 2026-11-04, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
