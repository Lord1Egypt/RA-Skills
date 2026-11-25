## Description:

快手公开数据只读技能：关键词搜视频、博主作品与粉丝数据、视频评论，输出 JSON，不登录不发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[um-why](https://clawhub.ai/user/um-why)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketing teams, and analysts use this skill to explore public Kuaishou videos, creator posts, and comments for topic research, competitor monitoring, and creator assessment. It returns structured data for the agent to summarize and compare.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Query keywords or links are sent to guaikei.com, so confidential information could be disclosed.

Mitigation: Use public, non-sensitive keywords and links; do not submit confidential information.

Risk: The security review had medium confidence and partial coverage; 13 components were not fully interpreted.

Mitigation: Treat the clean verdict as limited assurance and review the skill before installation if broader coverage is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/um-why/skills/kuaishou-data-miner)
- [Guaikei data service and token access](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [JSON data, Analysis]

**Output Format:** [JSON response envelope containing video search results, creator data and posts, or video comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result fields and metric types vary by command; the agent can summarize or compare returned public data.]

## Skill Version(s):

1.1.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
