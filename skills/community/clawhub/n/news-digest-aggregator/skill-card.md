## Description: <br>
Daily automated news digest that fetches RSS feeds, summarizes articles, and delivers formatted digests to Discord, Slack, or Feishu on a schedule. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cp3d1455926-svg](https://clawhub.ai/user/cp3d1455926-svg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operations teams use this skill to configure scheduled RSS aggregation and publish daily news digest text to Discord, Slack, or Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script automatically installs unpinned Python packages at runtime. <br>
Mitigation: Review the script before installation and preinstall pinned dependencies in a virtual environment. <br>
Risk: Webhook delivery can expose digest content to configured messaging channels. <br>
Mitigation: Use dedicated low-privilege webhooks and avoid sensitive or private RSS sources unless approved. <br>
Risk: Cron scheduling can continue posting after automatic delivery is no longer wanted. <br>
Mitigation: Test manually before adding cron and remove the cron entry when scheduled posting should stop. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cp3d1455926-svg/news-digest-aggregator) <br>
- [RSS Source Configuration](references/sources.json) <br>
- [TechCrunch RSS Feed](https://techcrunch.com/feed/) <br>
- [The Verge RSS Feed](https://www.theverge.com/rss/index.xml) <br>
- [Reuters Technology Feed](https://www.reutersagency.com/feed/?taxonomy=markets&post_type=reuters-best) <br>
- [Hacker News RSS Feed](https://news.ycombinator.com/rss) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown digest text with configuration JSON and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Digest content is grouped by source category and can be sent through Discord, Slack, or Feishu webhooks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
