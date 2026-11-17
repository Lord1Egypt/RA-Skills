## Description:

当用户需要做快手选题、快手内容选题、短视频选题策划、快手视频爆款角度拆解、内容方向规划或选题素材整理时使用；面向内容运营、品牌调研和创作者，提供快手关键词搜索、博主作品获取和视频评论获取功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[why20261](https://clawhub.ai/user/why20261)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators, brand researchers, creators, and analysts use this skill to collect public Kuaishou search results, creator posts, and video comments for topic research, competitor monitoring, KOL screening, trend analysis, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kuaishou search terms, profile URLs, video URLs, and token-authenticated requests are sent to guaikei.com.

Mitigation: Use the skill only when the organization approves that third-party API use, and avoid sensitive campaign or client research terms.

Risk: Returned JSON data may be saved locally in logs.

Mitigation: Review local retention requirements, limit sensitive inputs, and remove generated logs when they are no longer needed.

Risk: The skill is limited to public Kuaishou data and can fail on missing tokens, invalid links, empty results, rate limits, or upstream service errors.

Mitigation: Validate inputs before execution, handle non-success JSON statuses explicitly, and do not treat empty or error responses as analysis findings.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/why20261/skills/kuaishou-topic-analysis-v1)
- [Server-resolved GitHub source](https://github.com/why20261/kuaishou-topic-analysis-v1)
- [Guaikei API service](https://www.guaikei.com)
- [完整选项参数说明](references/options.md)
- [更新日志](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Node.js shell commands; executed scripts return structured JSON and may save JSON result logs locally.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN and network access to guaikei.com; supports keyword, profile or user_id, video URL or video ID, sort, time, duration, and limit parameters.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact package metadata and changelog list 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
