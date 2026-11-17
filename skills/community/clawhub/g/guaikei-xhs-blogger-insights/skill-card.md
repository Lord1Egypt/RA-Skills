## Description:

获取小红书博主公开作品及单篇笔记的点赞、评论、收藏和评论数据，用于评估公开互动质量、筛选 KOL、监控竞品和支持内容决策。

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, brand marketing teams, analysts, MCN teams, and agents use this skill to query public Xiaohongshu notes, creator posts, and comments for trend research, competitor monitoring, KOL screening, and engagement-quality assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Xiaohongshu queries and URLs are sent to the Guaikei API.

Mitigation: Use only when data sharing with that service is acceptable and within the user's authorization scope.

Risk: The API token is sent in request URLs and may appear in infrastructure or diagnostic logs.

Mitigation: Use a dedicated, revocable token and rotate it if URLs or logs may have exposed it.

Risk: Queried URLs and returned data are saved locally in plaintext.

Mitigation: Run from a non-shared, non-synced directory and review or delete logs regularly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-xhs-blogger-insights)
- [Guaikei API website](https://www.guaikei.com)
- [Options reference](references/options.md)
- [Changelog](references/changelog.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and structured JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0+ and GUAIKEI_API_TOKEN; commands may write plaintext JSON results under logs/.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata reports 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
