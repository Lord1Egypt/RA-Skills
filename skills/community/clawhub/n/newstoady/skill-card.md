## Description: <br>
NewsToday aggregates, deduplicates, and summarizes current news into bilingual morning briefings, evening recaps, RSS-based digests, topic tracking, and optional breaking-news push alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiajiaoy](https://clawhub.ai/user/jiajiaoy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use NewsToday to generate concise, source-attributed news briefings, track topics, and manage optional scheduled news notifications across supported messaging channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Current-news fetching and broad trigger phrases can produce incomplete, stale, or misleading briefings when sources disagree or breaking events are still developing. <br>
Mitigation: Review source attribution, cross-check important stories before acting, and treat breaking-news summaries as provisional. <br>
Risk: Optional push delivery through Telegram, Feishu, Slack, or Discord can expose user IDs, preferred topics, and alert content to third-party messaging channels. <br>
Mitigation: Use push mode only with channels and user IDs you control, and avoid sensitive tracked topics when third-party retention is a concern. <br>
Risk: Scheduled morning, evening, and breaking-news notifications can continue after they are no longer wanted. <br>
Mitigation: Use the provided push status and off commands to audit and disable scheduled notifications. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jiajiaoy/newstoady) <br>
- [Publisher Profile](https://clawhub.ai/user/jiajiaoy) <br>
- [OpenClaw](https://openclaw.ai) <br>
- [Sina News RSS](https://rss.sina.com.cn/news/china/focus15.xml) <br>
- [The Paper RSS](https://www.thepaper.cn/rss_promotion.jsp) <br>
- [36Kr RSS](https://36kr.com/feed) <br>
- [BBC Chinese RSS](https://feeds.bbci.co.uk/zhongwen/simp/rss.xml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text prompts with optional shell commands and scheduler configuration records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese and English output; scheduled push mode can emit OpenClaw cron add/remove records.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release evidence, _meta.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
