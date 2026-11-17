## Description:

当用户需要搜索抖音关键词（视频/图文/用户）、获取博主作品列表、抓取视频评论或查询实时热榜时，使用本技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Content researchers, marketers, and analysts use this skill to collect structured public Douyin search results, creator posts, video comments, and hot-ranking data for topic research, competitor analysis, sentiment exploration, and trend tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends GUAIKEI_API_TOKEN values in URL query parameters.

Mitigation: Use only a scoped, revocable token and rotate it after testing or suspected exposure; the publisher should move token transmission to a safer authentication channel.

Risk: Search terms, creator URLs, video URLs, and comments-related requests are sent to guaikei.com.

Mitigation: Avoid submitting confidential research terms or private business-sensitive URLs, and disclose the external API dependency to users before deployment.

Risk: Generated logs may preserve local datasets containing personal data from Douyin public content.

Mitigation: Store logs in an approved location, apply retention limits, and review exported data before sharing outside the team.

Risk: Authentication failures may display undeclared promotional or contact text.

Mitigation: Review runtime error output before installing broadly and require neutral error messaging in publisher updates.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/engheng-art/skills/guaikei-douyin-thorough-data-miner)
- [Publisher Profile](https://clawhub.ai/user/engheng-art)
- [Complete Options](references/options.md)
- [Changelog](references/changelog.md)
- [Guaikei Token and Help Site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [shell commands, JSON, files, guidance]

**Output Format:** [JSON on stdout with logs and status messages on stderr; JSON log files may be written under logs/.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >=16.14 and a GUAIKEI_API_TOKEN; single command runs can request up to 10000 records.]

## Skill Version(s):

1.0.0 (source: package.json, changelog, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
