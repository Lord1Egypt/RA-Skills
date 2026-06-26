## Description: <br>
Makima's All-Seeing Intelligence Suite. Combines real-time AI news tracking and global news monitoring for a comprehensive strategic briefing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xhrisfu](https://clawhub.ai/user/xhrisfu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to collect recent AI and global-news signals, scrape short article snippets, and prepare source packs for briefing or synthesis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Normal output can include an unlabeled placeholder entertainment item. <br>
Mitigation: Treat entertainment entries as unverified unless the source link and article content are independently confirmed. <br>
Risk: Deep scraping can fetch article pages outside the declared source list. <br>
Mitigation: Run in an environment with outbound network allowlists and review fetched URLs before using snippets in final briefings. <br>
Risk: Scraped snippets may contain inaccurate, stale, or adversarial source text. <br>
Mitigation: Require citation checks and human review before relying on generated briefings for factual or strategic decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xhrisfu/intelligence-suite) <br>
- [OpenAI blog RSS feed](https://openai.com/blog/rss.xml) <br>
- [Microsoft AI blog feed](https://blogs.microsoft.com/ai/feed/) <br>
- [Hacker News Firebase API](https://hacker-news.firebaseio.com/v0/topstories.json) <br>
- [Reuters agency feed](https://www.reutersagency.com/feed/?best-regions=global&post_type=best) <br>
- [SCMP RSS feed](https://www.scmp.com/rss/91/feed) <br>
- [RTHK local news RSS feed](https://rthk9.rthk.hk/rthk/news/rss/e_expressnews_elocal.xml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Console text containing structured intelligence or news packs for agent synthesis.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Snippets are truncated to about 1000-1500 characters per fetched page.] <br>

## Skill Version(s): <br>
1.0.3 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
