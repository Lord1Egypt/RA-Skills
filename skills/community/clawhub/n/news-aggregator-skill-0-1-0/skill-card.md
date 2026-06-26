## Description: <br>
Comprehensive news aggregator that fetches, filters, and deeply analyzes real-time content from 8 major sources: Hacker News, GitHub Trending, Product Hunt, 36Kr, Tencent News, WallStreetCN, V2EX, and Weibo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zy66677](https://clawhub.ai/user/zy66677) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to gather current technology, finance, product, open-source, and social-trend items from public news sources, then turn them into concise Simplified Chinese briefings and Markdown reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public news sites and linked article pages, which may expose source selections and topics to those services. <br>
Mitigation: Run it only in trusted environments and limit sources, keywords, or deep fetching when network exposure should be minimized. <br>
Risk: Generated reports may persist locally and reveal user interests or monitored topics. <br>
Mitigation: Review saved reports under reports/ and remove files that contain sensitive topics or no longer need to be retained. <br>
Risk: Smart keyword expansion and smart fill behavior can broaden a search or include older supplementary items. <br>
Mitigation: Ask for strict keywords or strict time windows when exact filtering matters, and review timestamps and source metadata before relying on a report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zy66677/news-aggregator-skill-0-1-0) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files] <br>
**Output Format:** [Markdown report with source links, plus JSON arrays from fetch_news.py when commands are run] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are saved as timestamped Markdown files under reports/; deep fetch can add extracted article content to news items.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
