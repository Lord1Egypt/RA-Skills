## Description:

快手(Kuaishou)关键词搜索获取快手实时搜索数据｜当用户需要做快手内容研究、快手选题、热点观察、竞品内容对比、趋势判断或素材整理时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT

## Use Case:

快手内容创作者、运营人员和市场分析师可用它搜索公开视频、查看博主公开作品和获取视频评论，为选题、热点观察、竞品对比和舆情研究整理数据。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries and links are sent to the GUAIKEI service when the skill runs.

Mitigation: Submit public Kuaishou content only, and avoid sensitive query text or private links.

Risk: ClawScan reports a benign verdict with medium confidence; analysis was partial, with 20 of 32 components fully scanned.

Mitigation: Review the current release and its network behavior before relying on the scan verdict.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/kuaishou-content-research-skill)
- [GUAIKEI service](https://www.guaikei.com)
- [Command options](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON data]

**Output Format:** [Structured JSON containing public Kuaishou video, comment, or creator data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on GUAIKEI API access and available public data; token plans may limit result counts.]

## Skill Version(s):

1.1.2 (source: artifact/SKILL.md frontmatter, artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
