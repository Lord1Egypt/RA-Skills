## Description:

Hotspot Aggregator helps agents gather trending topics from Weibo, Baidu, Zhihu, and Douyin, generate daily Markdown reports, and check keyword subscriptions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onlyloveher](https://clawhub.ai/user/onlyloveher)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content, marketing, media operations, and public-opinion monitoring teams use this skill to monitor Chinese-language trending topics, prepare daily hotspot reports, and track subscribed keywords.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores untrusted online trend content and generated reports in persistent local memory.

Mitigation: Treat generated Markdown and JSON as untrusted content, review it before reuse, and periodically delete or rotate files under /root/clawd/memory/hotspots.

Risk: Real API mode sends outbound requests to social platforms and a third-party Douyin aggregator.

Mitigation: Keep USE_REAL_API disabled unless outbound access to those services is approved, and configure proxy or network controls before enabling it.

Risk: Broad triggers or scheduled report generation can fetch and persist trend data automatically.

Mitigation: Narrow triggers, add confirmation before automated runs when appropriate, and avoid overly frequent scheduled fetches.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/onlyloveher/skills/hotspot-aggregator-zhouli)
- [Publisher profile](https://clawhub.ai/user/onlyloveher)
- [Skill homepage metadata](https://clawhub.com/skills/hotspot-aggregator)
- [Weibo hot search endpoint](https://weibo.com/ajax/side/hotSearch)
- [Baidu top search endpoint](https://top.baidu.com/api/board?platform=wise&tab=realtime)
- [Zhihu hot list endpoint](https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total)
- [Douyin third-party hotspot aggregator endpoint](https://api.oioweb.cn/api/toutiao/douyinHot)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration]

**Output Format:** [Markdown reports, JSON hotspot datasets, configuration updates, and terminal text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes reports and fetched data under /root/clawd/memory/hotspots; real outbound API calls are gated by USE_REAL_API.]

## Skill Version(s):

1.0.0 (source: server evidence, SKILL.md frontmatter, package.json, skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
