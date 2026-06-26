## Description: <br>
中文AI科技日报自动采集与推送，从The Verge、Wired、TechCrunch等英文源抓取最新AI资讯，自动翻译整理为中文，按分类推送到飞书、Telegram、Discord等渠道。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiadong0723](https://clawhub.ai/user/jiadong0723) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use this skill to collect recent English-language AI news, translate and classify it into a Chinese daily briefing, and optionally send the digest to configured chat channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A scheduled run could post a digest to the wrong Feishu, Telegram, or Discord destination. <br>
Mitigation: Run the skill manually once, confirm whether it previews or sends, and verify the exact destination before enabling a schedule. <br>
Risk: Chat-channel or search credentials could have broader access than the skill needs. <br>
Mitigation: Use narrowly scoped API keys and keep any scheduled job easy to find, rotate, and disable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jiadong0723/jiadong-ai-news-zh) <br>
- [The Verge AI](https://www.theverge.com/ai-artificial-intelligence) <br>
- [Wired AI RSS](https://www.wired.com/feed/tag/ai/latest/rss) <br>
- [TechCrunch RSS](https://techcrunch.com/feed/) <br>
- [Anthropic News](https://www.anthropic.com/news) <br>
- [MIT Technology Review RSS](https://www.technologyreview.com/feed/) <br>
- [Google AI Blog](https://blog.google/technology/ai/) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, configuration, guidance] <br>
**Output Format:** [Markdown Chinese daily briefing with source links, category labels, concise summaries, and an optional trend insight.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 8-12 prioritized news items and can support scheduled delivery to Feishu, Telegram, or Discord when those destinations are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
