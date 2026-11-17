## Description:

快手(Kuaishou)关键词搜索获取快手实时搜索数据｜当用户需要做快手内容研究、快手选题、热点观察、竞品内容对比、趋势判断或素材整理时使用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking creators, marketers, and analysts use this agent to research public Kuaishou videos, creator posts, and comments for topic discovery, trend monitoring, competitor comparisons, and comment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, video links, and creator IDs are transmitted to the GUAIKEI service; the security guidance notes that disclosure of this transmission may be unclear.

Mitigation: Use only public Kuaishou data, and avoid submitting sensitive keywords, links, or IDs unless you accept that the GUAIKEI service will receive them.

Risk: The security scan was partial: 20 of 32 components were fully scanned and 12 were partially inspected.

Mitigation: Review the skill and its uninspected components before installation or use in a sensitive environment.

## Reference(s):

- [GUAIKEI service and token access](https://www.guaikei.com)
- [ClawHub release page](https://clawhub.ai/why20261/skills/kuaishou-content-research-skill)
- [Usage options](artifact/references/options.md)
- [Changelog](artifact/references/changelog.md)

## Skill Output:

**Output Type(s):** [JSON data, Analysis]

**Output Format:** [Structured JSON envelope containing Kuaishou search results, creator posts or profile data, or video comments.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Covers public Kuaishou data. Request limits depend on the token plan: monthly limits are 30 search results, 50 posts, and 60 comments; pay-as-you-go requests allow up to 10,000.]

## Skill Version(s):

1.1.1 (source: SKILL.md frontmatter, package.json, changelog released 2026-11-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
