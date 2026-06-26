## Description: <br>
Hotspot Aggregator aggregates trending topics from Weibo, Baidu, Zhihu, and Douyin, generates daily hotspot reports, and supports keyword subscriptions for content and market monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content creators, marketers, and analysts use this skill to collect trending-topic data, generate daily Markdown hotspot reports, and monitor subscribed keywords across major Chinese social and search platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases may activate hotspot monitoring in more conversations than intended. <br>
Mitigation: Narrow activation phrases where possible and run collection or report scripts only through reviewed commands or schedules. <br>
Risk: Scheduled network-based trend monitoring can persist reports and keyword matches locally. <br>
Mitigation: Review cron setup before installation, define retention or deletion expectations for /root/clawd/memory/hotspots, and avoid monitoring sensitive people, brands, or topics unless that persistence is intentional. <br>
Risk: Real API mode sends requests to external social, search, and third-party endpoints and may use a proxy. <br>
Mitigation: Review endpoint and proxy settings before setting USE_REAL_API=true, and account for platform access limits and terms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/onlyloveher/hotspot-aggregator) <br>
- [Weibo hot search endpoint](https://weibo.com/ajax/side/hotSearch) <br>
- [Baidu realtime board endpoint](https://top.baidu.com/api/board?platform=wise&tab=realtime) <br>
- [Zhihu hot list endpoint](https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total) <br>
- [Douyin hot API endpoint](https://api.oioweb.cn/api/toutiao/douyinHot) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown reports, JSON data files, and terminal text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes hotspot data and reports under /root/clawd/memory/hotspots and stores keyword subscriptions in config.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, package.json, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
