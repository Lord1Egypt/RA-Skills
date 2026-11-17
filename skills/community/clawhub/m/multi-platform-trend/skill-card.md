## Description:

Fetches public trending topics from Zhihu, Weibo, Baidu, and Bilibili and returns structured trend data for content planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and agents use this skill to retrieve current Chinese-platform trending topics, filter them by platform or keyword, and prepare topic candidates for follow-on analysis or drafting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs a local Python script that makes outbound requests to Zhihu, Weibo, Baidu, and Bilibili.

Mitigation: Install and run it only in environments where those public trend lookups are acceptable, and apply normal outbound network controls.

Risk: Broad trigger phrases may cause the skill to run more often than intended.

Mitigation: Review and narrow the trigger phrases or require confirmation before fetching trends in sensitive workflows.

Risk: Trend heat values are estimates and source availability can vary by platform.

Mitigation: Treat fetched rankings as directional signals and verify important topics against the source platform before publication decisions.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/freedompixels/skills/multi-platform-trend)
- [Publisher profile](https://clawhub.ai/user/freedompixels)
- [Zhihu hot-list API endpoint](https://api.zhihu.com/topstory/hot-lists/total)
- [Weibo hot search endpoint](https://weibo.com/ajax/side/hotSearch)
- [Baidu realtime board endpoint](https://top.baidu.com/api/board?platform=wise&tab=realtime)
- [Bilibili ranking endpoint](https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Markdown-facing instructions with optional JSON trend records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trend records include title, platform, heat, heat_display, url, category, and excerpt when available.]

## Skill Version(s):

1.2.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
