## Description: <br>
热点聚合监控 aggregates trending topics from Weibo, Baidu, Zhihu, and Douyin, generates daily hotspot reports, and supports keyword subscriptions for monitoring and content workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[onlyloveher](https://clawhub.ai/user/onlyloveher) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content operators, market analysts, and developers use this skill to collect public trending-topic data, generate daily Markdown hotspot reports, and monitor configured keywords across supported Chinese social and search platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live hotspot collection can make outbound requests to public platform or aggregation APIs when USE_REAL_API is enabled. <br>
Mitigation: Enable USE_REAL_API only when live network collection is intended, and review any configured PROXY before execution. <br>
Risk: Reports and fetched hotspot data are stored locally under /root/clawd/memory/hotspots, and keyword subscriptions are stored in config.json. <br>
Mitigation: Remove stored hotspot files and clear config.json keywords when reports or subscriptions are no longer needed. <br>
Risk: A cron entry can create recurring collection and report generation. <br>
Mitigation: Add scheduled execution only when recurring reports are desired, and review the schedule for acceptable frequency. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/onlyloveher/hotspot-aggregator-clawd) <br>
- [Publisher Profile](https://clawhub.ai/user/onlyloveher) <br>
- [Weibo Hot Search Endpoint](https://weibo.com/ajax/side/hotSearch) <br>
- [Baidu Hot Board API](https://top.baidu.com/api/board?platform=wise&tab=realtime) <br>
- [Zhihu Hot List API](https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total) <br>
- [Douyin Hot Aggregation API](https://api.oioweb.cn/api/toutiao/douyinHot) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON hotspot data, and shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports and fetched data under /root/clawd/memory/hotspots and stores keyword subscriptions in config.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence, SKILL.md frontmatter, package.json, skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
